# GitHub configuration - WBS-00.5
Local repository, CI workflow, issue templates, RTM and risk register are prepared. Remote repository and enforced branch protection **not yet verified**. GitHub CLI was not available on PATH and no CLI authentication was confirmed.

After authenticating GitHub CLI (do not paste a token into chat), from the repository root:
```powershell
gh auth login
gh repo create fieldsaarthi-ai --private --source . --remote origin --push
```
Use private visibility initially to protect review artifacts. Enable Issues. Create one issue per WBS item using `tasks/todo.md`; local task file is authoritative until tracker URLs are recorded.
Protect `main`: require pull requests, require passing `quality` check, block force pushes/deletions. For a solo project do not require another person's approval unless a reviewer is actually available. Verify protection via repository settings/API; private-repository protection may depend on account plan. Do not claim enforcement from a workflow file alone.
Global participant Git email is a placeholder (`your_email@example.com`). Local baseline commits use explicit Codex agent attribution. Set the intended participant identity before participant-authored commits; do not invent contributor attribution.
