"""Opt-in actual-browser test: one genuine STT call using consented prerecorded speech.

Does not claim freshly spoken microphone input. Test the recorder separately
with Chrome's file-fed test audio, then discard it without a second paid call.
"""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    if not args.live:
        parser.error("Use --live to authorize one genuine API call")
    accounts = json.loads((ROOT / "private/demo-accounts.json").read_text())
    worker = next(x for x in accounts if x["email"] == "worker@fieldsaarthi.demo")
    supervisor = next(x for x in accounts if x["role"] == "SUPERVISOR")
    output = ROOT / "docs/evidence/browser"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--use-file-for-fake-audio-capture=" + str(ROOT / "private/sample_hi.wav"),
            ],
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 1000}, permissions=["microphone"]
        )
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(args.base_url)
        page.get_by_role("heading", name="Welcome back.").wait_for()
        page.screenshot(path=str(output / "01-login.png"), full_page=True)

        def sign_in(account):
            page.get_by_label("Email address").fill(account["email"])
            page.get_by_label("Password", exact=True).fill(account["password"])
            page.get_by_role("button", name="Enter workspace").click()

        sign_in(worker)
        page.get_by_role("button", name="Start recording").wait_for()
        page.screenshot(path=str(output / "02-worker-desktop.png"), full_page=True)
        page.get_by_role("button", name="Start recording").click()
        page.get_by_role("button", name="Stop recording").wait_for()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Stop recording").click()
        page.get_by_label("Discard recording").wait_for()
        page.get_by_label("Discard recording").click()
        page.locator("input[type=file]").set_input_files(str(ROOT / "private/sample_hi.wav"))
        with page.expect_response(
            lambda r: "/intakes/transcribe" in r.url, timeout=120000
        ) as speech:
            page.get_by_role("button", name="Transcribe report").click()
        response = speech.value
        assert response.status == 201, response.text()
        intake = response.json()
        assert intake["raw_transcript"].strip() and intake["provider"]["model"] == "prisma-v2.5"
        page.get_by_role("heading", name="Your words. The right next step.").wait_for()
        page.screenshot(path=str(output / "03-live-review.png"), full_page=True)
        page.get_by_role("checkbox").check()
        with page.expect_response(
            lambda r: "/work-orders" in r.url and r.request.method == "POST"
        ) as created:
            page.get_by_role("button", name="Confirm & create work order").click()
        assert created.value.status == 201, created.value.text()
        order = created.value.json()
        oid = order["id"]
        page.get_by_role("heading", name=order["asset_name"], exact=True).wait_for()
        page.reload()
        page.get_by_role("heading", name=order["asset_name"], exact=True).wait_for()
        page.screenshot(path=str(output / "04-persisted-order.png"), full_page=True)
        page.get_by_label("Sign out").click()
        page.get_by_role("heading", name="Welcome back.").wait_for()
        sign_in(supervisor)
        page.get_by_role("link", name=order["public_code"], exact=True).click()
        page.get_by_label("Assign a worker").select_option(label="Ravi Kumar")
        page.get_by_role("button", name="Save assignment").click()
        page.get_by_role("button", name="Start work").wait_for()
        page.get_by_role("button", name="Start work").click()
        page.get_by_label("Resolution note").wait_for()
        page.get_by_label("Resolution note").fill(
            "Synthetic demonstration: inspected pump and replaced the leaking seal."
        )
        page.get_by_role("button", name="Mark resolved").click()
        page.get_by_text("Resolved", exact=True).first.wait_for()
        page.reload()
        page.get_by_role("heading", name=order["asset_name"], exact=True).wait_for()
        page.screenshot(path=str(output / "05-supervisor-resolved.png"), full_page=True)
        page.goto(args.base_url + "/#/orders")
        page.get_by_role("link", name=order["public_code"], exact=True).wait_for()
        page.screenshot(path=str(output / "06-operations-queue.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.screenshot(path=str(output / "07-mobile-queue.png"), full_page=True)
        assert not errors, errors
        evidence = {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "base_url": args.base_url,
            "input": ("user-recorded prerecorded Hindi sample; not fresh human microphone speech"),
            "recorder": (
                "MediaRecorder start/stop verified with Chrome file-fed test audio; discarded"
            ),
            "provider": intake["provider"],
            "transcribe_http_status": response.status,
            "order_id": oid,
            "public_code": order["public_code"],
            "refresh_persistence": True,
            "supervisor_assignment_and_resolution": True,
            "javascript_errors": errors,
            "desktop_width": 1440,
            "mobile_width": 390,
        }
        (output / "live-browser-smoke.json").write_text(
            json.dumps(evidence, indent=2), encoding="utf-8"
        )
        context.close()
        browser.close()
        print(
            "Live browser workflow passed. Sanitized evidence: "
            "docs/evidence/browser/live-browser-smoke.json"
        )


if __name__ == "__main__":
    main()
