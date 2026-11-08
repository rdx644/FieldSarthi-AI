"""Non-billable browser, responsive layout and axe accessibility verification."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--channel", default="chrome")
    args = parser.parse_args()
    accounts = json.loads((ROOT / "private/demo-accounts.json").read_text())
    target = ROOT / "docs/evidence/browser"
    target.mkdir(parents=True, exist_ok=True)
    axe = (ROOT / "web/node_modules/axe-core/axe.min.js").read_text(encoding="utf-8")
    results = []
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel=None if args.channel == "chromium" else args.channel, headless=True
        )
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        page = context.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))

        def audit(name):
            page.wait_for_timeout(350)
            page.evaluate(axe)
            result = page.evaluate(
                'async () => await axe.run(document,{runOnly:{type:"tag",'
                'values:["wcag2a","wcag2aa","wcag21aa"]}})'
            )
            violations = [
                {
                    "id": x["id"],
                    "impact": x["impact"],
                    "description": x["description"],
                    "targets": [n["target"] for n in x["nodes"]],
                }
                for x in result["violations"]
            ]
            overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
            results.append(
                {"page": name, "violations": violations, "horizontal_overflow": overflow}
            )
            page.screenshot(path=str(target / (name + ".png")), full_page=True)

        page.goto(args.base_url)
        page.get_by_role("heading", name="Welcome back.").wait_for()
        audit("quality-login")
        worker = next(x for x in accounts if x["email"] == "worker@fieldsaarthi.demo")
        page.get_by_label("Email address").fill(worker["email"])
        page.get_by_label("Password", exact=True).fill(worker["password"])
        page.get_by_role("button", name="Enter workspace").click()
        page.get_by_role("button", name="Start recording").wait_for()
        audit("quality-worker-desktop")
        page.set_viewport_size({"width": 390, "height": 844})
        audit("quality-worker-mobile")
        page.get_by_role("button", name="Toggle navigation").click()
        page.get_by_role("button", name="My reports", exact=False).click()
        page.get_by_role("heading", name="From reported to resolved.").wait_for()
        previous_url = page.url
        page.locator(".skip-link").focus()
        page.locator(".skip-link").press("Enter")
        page.wait_for_timeout(100)
        assert page.url == previous_url, "Skip-to-content must not change the application route"
        assert page.evaluate("document.activeElement.id") == "main"
        audit("quality-queue-mobile")
        page.set_viewport_size({"width": 1440, "height": 1000})
        audit("quality-queue-desktop")
        if page.locator(".order-code").count():
            page.locator(".order-code").first.click()
            page.get_by_role("heading", name="The reported issue").wait_for()
            audit("quality-detail-desktop")
        context.close()
        browser.close()
    output = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "checks": results,
        "javascript_errors": errors,
        "live_provider_calls": 0,
    }
    (target / "accessibility.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
    assert not errors
    assert not any(x["horizontal_overflow"] or x["violations"] for x in results)


if __name__ == "__main__":
    main()
