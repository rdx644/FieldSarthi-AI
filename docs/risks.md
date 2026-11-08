# Risk register
| ID | Severity | Risk / status | Mitigation / owner |
|---|---|---|---|
| R-01 | Critical | Active key/scope/credits unverified; live proof unavailable | User confirms console; developer executes real smoke before frontend |
| R-02 | High | Recording format incompatible | Strict WAV validation; real voice export; later server conversion |
| R-03 | High | ASR/codemix quality unknown | Authentic short Hindi sample, exact raw transcript, human review |
| R-08 | Critical | Deadline near; frontend distracts from access | WBS-00/01 only until G1; no speculative UI |
| R-09 | Critical | Credential/audio disclosure | Ignored .env/private; cURL key through stdin; sanitized allowlisted evidence |
| R-10 | Critical | Missing eligibility or submission form | User confirmation, live form instructions, final checklist |
| R-11 | Critical | Fixtures mistaken for live model proof | Fixtures in tests only; G1 pending until authentic evidence |
| R-12 | Medium | Contribution identity unresolved | Confirm solo/team and authorship; no invented contributor credit |
| R-15 | High | Remote repo/protection not provisioned | GitHub auth required; local workflow/tracker prepared; verify remote later |

Review before each gate. Critical/high defects prevent release. Owner is developer unless participant-account action explicitly requires user.
