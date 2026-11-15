# Synthetic local browser evidence — November 14, 2026

These screenshots/results are generated only from an isolated `fieldsaarthi_test`
database and a test-only speech fixture. They are not real worker reports,
provider availability measurements or hosted release evidence. The visible
HTML-looking transcript deliberately tests React escaping; it never executes.
Judge visibility of the synthetic fixture exists only in that isolated test DB.

The workflow checks permission/capture lifecycle, separate manual provenance,
human confirmation, location/equipment reset, stable server-summary scope under
filters, supervisor resolution/refresh, judge read-only access, keyboard shortcut,
empty/unavailable states and WCAG/layout at 320/768/1024/1440 widths. Live provider
calls: zero. See `results.json` for exact checks and timestamps.

Command from `api/`:

```powershell
.venv/Scripts/python.exe tests/browser/workflow_check.py --channel chrome --output-dir docs/evidence/improvement-browser
```

This command resets only `fieldsaarthi_test`; run sequentially with integration
tests. Output selection preserves dated historical browser/hosted artifacts.
