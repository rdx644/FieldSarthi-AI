"""Full browser regression with TEST-ONLY speech, isolated DB and no provider network.

Run after building web and installing Chromium. This is never live Gnani evidence.
"""

import argparse
import json
import os
import sys
import threading
import time
import wave
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "api"))
load_dotenv(ROOT / ".env")
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
os.environ["PUBLIC_JUDGE_DEMO_ENABLED"] = "true"


def main():
    import httpx
    import uvicorn
    from alembic.config import Config
    from playwright.sync_api import expect, sync_playwright
    from sqlalchemy import text

    from alembic import command
    from app.db.models import Order
    from app.db.session import SessionLocal, engine
    from app.integrations.gnani import Transcription
    from app.main import app
    from app.routers import intakes
    from app.seed import seed

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", default="chrome")
    args = parser.parse_args()
    target = ROOT / "docs/evidence/browser-regression"
    target.mkdir(parents=True, exist_ok=True)
    (target / "results.json").write_text(
        json.dumps(
            {
                "timestamp_utc": datetime.now(UTC).isoformat(),
                "status": "not_completed",
                "passed": False,
                "kind": "nonbillable_test_only_provider_fixture_browser_regression",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    assert engine.url.database == "fieldsaarthi_test", "Never reset a non-test database"
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
    command.upgrade(Config("alembic.ini"), "head")
    with SessionLocal() as db:
        accounts = seed(db)
    transcript = '<img src=x onerror="window.__xss=1"> Block B water pump leak urgent'
    calls = []

    async def test_only_speech(audio, language, correlation):
        calls.append(correlation)
        return Transcription(
            success=True,
            transcript=transcript,
            request_id="TEST-ONLY-" + correlation,
            model="prisma-v2.5",
            correlation_id=correlation,
            language_code=language,
            http_status=200,
            elapsed_seconds=0.01,
        )

    intakes.speech.transcribe = test_only_speech
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=8124, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    base = "http://127.0.0.1:8124"
    for _ in range(100):
        try:
            if httpx.get(base + "/health/ready").status_code == 200:
                break
        except httpx.RequestError:
            pass
        time.sleep(0.1)
    else:
        raise RuntimeError("Browser test server did not become ready")
    axe = (ROOT / "web/node_modules/axe-core/axe.min.js").read_text(encoding="utf-8")
    audits = []
    errors = []
    try:
        with TemporaryDirectory() as folder, sync_playwright() as playwright:
            source = Path(folder) / "test-only.wav"
            with wave.open(str(source), "wb") as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(16000)
                audio.writeframes(b"\0\0" * 16000)
            browser = playwright.chromium.launch(
                channel=None if args.channel == "chromium" else args.channel, headless=True
            )
            context = browser.new_context(viewport={"width": 1440, "height": 1000})
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.add_init_script("""Object.defineProperty(navigator.mediaDevices, 'getUserMedia', {
                configurable: true, writable: true,
                value: async () => { throw new DOMException('Denied in test', 'NotAllowedError'); }
            });""")

            def audit(name, screenshot=False):
                page.evaluate(axe)
                result = page.evaluate(
                    "async () => await axe.run(document, { runOnly: { type: 'tag', "
                    "values: ['wcag2a','wcag2aa','wcag21aa'] } })"
                )
                violations = [
                    {
                        "id": item["id"],
                        "impact": item["impact"],
                        "targets": [node["target"] for node in item["nodes"]],
                    }
                    for item in result["violations"]
                ]
                overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
                audits.append(
                    {
                        "view": name,
                        "width": page.viewport_size["width"],
                        "violations": violations,
                        "horizontal_overflow": overflow,
                    }
                )
                assert not violations and not overflow, audits[-1]
                if screenshot:
                    page.screenshot(path=str(target / (name + ".png")), full_page=True)

            def sign_in(account):
                page.get_by_label("Email address").fill(account["email"])
                page.get_by_label("Password", exact=True).fill(account["password"])
                page.get_by_role("button", name="Enter workspace").click()

            page.goto(base)
            page.get_by_role("heading", name="Welcome back.").wait_for()
            sign_in(accounts[0])
            page.get_by_role("button", name="Start recording").wait_for()
            page.evaluate("""() => {
                window.__originalRecorder = window.MediaRecorder;
                window.__captureCalls = 0; window.__captureStarts = 0; window.__captureStops = 0;
                navigator.mediaDevices.getUserMedia = () => {
                    window.__captureCalls++;
                    return new Promise(resolve => { window.__resolveMic = () => resolve({
                        getTracks: () => [{ stop: () => window.__captureStops++ }]
                    }); });
                };
                window.MediaRecorder = class {
                    static isTypeSupported() { return true; }
                    start() { window.__captureStarts++; this.state = 'recording'; }
                    stop() { this.state = 'inactive'; }
                };
                const button = document.querySelector('[aria-label="Start recording"]');
                button.click(); button.click();
            }""")
            assert page.evaluate("window.__captureCalls") == 1
            expect(page.get_by_role("button", name="Upload audio instead")).to_be_disabled()
            page.get_by_role("button", name="My reports", exact=False).click()
            page.get_by_role("heading", name="From reported to resolved.").wait_for()
            page.evaluate("window.__resolveMic()")
            page.wait_for_function("window.__captureStops === 1")
            assert page.evaluate("window.__captureStarts") == 0
            page.evaluate("""() => {
                window.MediaRecorder = window.__originalRecorder;
                navigator.mediaDevices.getUserMedia = async () => {
                    throw new DOMException('Denied in test', 'NotAllowedError');
                };
            }""")
            page.get_by_role("button", name="New voice report").click()
            page.get_by_role("button", name="Start recording").wait_for()
            page.evaluate("""() => {
                window.__delayedRecorders = [];
                navigator.mediaDevices.getUserMedia = async () => ({
                    getTracks: () => [{stop() {}}]
                });
                window.MediaRecorder = class {
                    constructor() {
                        this.mimeType = 'audio/webm'; window.__delayedRecorders.push(this);
                    }
                    static isTypeSupported() { return true; }
                    start() { this.state = 'recording'; }
                    stop() { this.state = 'inactive'; }
                };
            }""")
            page.get_by_role("button", name="Start recording").click()
            page.get_by_role("button", name="Stop recording").click()
            page.get_by_role("button", name="Start recording").click()
            page.get_by_role("button", name="Stop recording").wait_for()
            page.evaluate("window.__delayedRecorders[0].onstop()")
            assert page.get_by_role("button", name="Stop recording").is_visible()
            assert page.get_by_label("Discard recording").count() == 0
            page.get_by_role("button", name="Stop recording").click()
            page.evaluate("window.__delayedRecorders[1].onstop()")
            page.get_by_label("Discard recording").click()
            page.evaluate("""() => {
                window.MediaRecorder = window.__originalRecorder;
                navigator.mediaDevices.getUserMedia = async () => {
                    throw new DOMException('Denied in test', 'NotAllowedError');
                };
            }""")
            page.get_by_role("button", name="Start recording").click()
            expect(page.get_by_role("alert")).to_contain_text("Microphone access was denied")
            page.get_by_text("Type a report instead", exact=True).click()
            manual_text = "Block B pump leak " + "x" * 2100
            page.get_by_label("Typed report").fill(manual_text)
            pending_manual = []
            page.route("**/api/v1/intakes/manual", lambda route: pending_manual.append(route))
            page.get_by_role("button", name="Review typed report").click()
            expect(page.get_by_role("button", name="Start recording")).to_be_disabled()
            assert len(pending_manual) == 1
            pending_manual[0].continue_()
            page.unroute("**/api/v1/intakes/manual")
            page.get_by_role("heading", name="Your typed report").wait_for()
            expect(page.locator(".provider-strip")).to_contain_text("MANUAL TEXT")
            expect(page.locator("blockquote.transcript")).to_have_text(manual_text)
            page.get_by_role("checkbox").check()
            assert page.get_by_role("button", name="Confirm & create work order").is_disabled()
            expect(page.get_by_role("alert")).to_contain_text("Shorten the issue description")
            page.get_by_label("Issue description").fill("Block B pump leak")
            page.get_by_role("checkbox").check()
            assert page.get_by_role("button", name="Confirm & create work order").is_enabled()
            page.get_by_role("button", name="Back to recording").click()
            page.locator("input[type=file]").set_input_files(str(source))
            page.get_by_role("button", name="Transcribe report").click()
            page.get_by_role("heading", name="What Gnani heard").wait_for()
            expect(page.locator("blockquote.transcript")).to_have_text(transcript)
            assert page.locator("blockquote.transcript img").count() == 0
            assert page.evaluate("window.__xss === undefined")
            assert page.get_by_role("button", name="Confirm & create work order").is_disabled()
            page.get_by_label("Corrected transcript").fill("Reviewed Block B pump leak")
            audit("test-only-review", screenshot=True)
            page.get_by_role("checkbox").check()
            with page.expect_response(
                lambda response: response.url.endswith("/work-orders")
                and response.request.method == "POST"
            ) as saved:
                page.get_by_role("button", name="Confirm & create work order").click()
            assert saved.value.status == 201
            order = saved.value.json()
            page.get_by_role("heading", name="The reported issue").wait_for()
            replay = context.request.post(
                base + "/api/v1/work-orders",
                data=saved.value.request.post_data_json,
                headers={
                    "Origin": base,
                    "X-Requested-With": "FieldSaarthi",
                    "Idempotency-Key": saved.value.request.headers["idempotency-key"],
                },
            )
            assert replay.status == 200 and replay.json()["id"] == order["id"]
            page.reload()
            page.get_by_role("heading", name="The reported issue").wait_for()
            assert page.locator(".original-transcript img").count() == 0
            assert page.evaluate("window.__xss === undefined")
            page.get_by_label("Sign out").click()
            sign_in(accounts[2])
            page.get_by_label("Priority filter").select_option("HIGH")
            page.get_by_role("heading", name="No reports match this view.").wait_for()
            page.get_by_role("button", name="Clear filters").click()
            page.get_by_role("link", name=order["public_code"], exact=True).click()
            page.get_by_label("Assign a worker").select_option(label="Ravi Kumar")
            page.get_by_role("button", name="Save assignment").click()
            page.get_by_role("button", name="Start work").wait_for()
            page.get_by_label("Supervisor priority").select_option("HIGH")
            page.get_by_role("button", name="Update priority").click()
            expect(page.get_by_role("button", name="Update priority")).to_be_disabled()
            assert page.get_by_role("button", name="Cancel work order").is_disabled()
            page.get_by_role("button", name="Start work").click()
            page.get_by_label("Resolution note").fill("TEST-ONLY synthetic seal replacement")
            page.get_by_role("button", name="Mark resolved").click()
            expect(page.get_by_text("Resolved", exact=True).first).to_be_visible()
            page.reload()
            page.get_by_role("heading", name="The reported issue").wait_for()
            audit("test-only-resolved", screenshot=True)
            with SessionLocal() as db:
                db.get(Order, order["id"]).judge_visible = True
                db.commit()
            page.get_by_label("Sign out").click()
            page.get_by_role("button", name="Open judge demo").click()
            page.get_by_role("heading", name="Inspect the work. Follow the evidence.").wait_for()
            page.get_by_role("link", name=order["public_code"], exact=True).wait_for()
            for width in [320, 768, 1024, 1440]:
                page.set_viewport_size({"width": width, "height": 1000})
                audit("judge-queue-" + str(width), screenshot=width == 1440)
            page.get_by_role("link", name=order["public_code"], exact=True).click()
            page.get_by_role("heading", name="The reported issue").wait_for()
            assert page.get_by_role("button", name="Save assignment").count() == 0
            assert page.get_by_role("button", name="Hear acknowledgment").count() == 0
            for width in [320, 768, 1024, 1440]:
                page.set_viewport_size({"width": width, "height": 1000})
                audit("judge-detail-" + str(width))
            assert not errors
            assert len(calls) == 1
            context.close()
            browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=10)
    report = {
        "status": "passed",
        "passed": True,
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "kind": "nonbillable_test_only_provider_fixture_browser_regression",
        "live_provider_calls": 0,
        "test_provider_calls": len(calls),
        "permission_denied_guidance": True,
        "one_pending_microphone_request": True,
        "stale_stop_callback_cannot_hide_new_capture": True,
        "late_microphone_tracks_stopped_after_navigation": True,
        "manual_request_disables_capture": True,
        "manual_source_label": True,
        "long_manual_description_requires_shortening": True,
        "script_transcript_escaped": True,
        "human_confirmation_required": True,
        "idempotent_replay": True,
        "supervisor_resolution_and_refresh": True,
        "judge_read_only_dashboard": True,
        "checks": audits,
        "javascript_errors": errors,
    }
    (target / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Full fixture-provider browser regression passed; zero live provider calls.")


if __name__ == "__main__":
    main()
