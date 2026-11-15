# Evaluate FieldSaarthi AI

Current hosted verification on November 15: application `241a063` passed the
0005 migration, actual Render rollback/restoration and six deployed Chrome
judge views. The approved sample and all 14 saved report details/audits/provider
facts are unchanged. Live team speech is restored after the owner's balance
confirmation; the judge remains read-only with paid audio disabled. See the
[current hosted release record](evidence/improvement-hosted-release.json).
No new speech request or independent accuracy measurement was made.

Historical deployment checks on 2026-11-10 IST covered application commit `6f702c2`;
the later [operational release](evidence/demo-operational-release.json) records
`85e1a5e` and rollback/restoration. The [earlier deployed checks](evidence/hosted/judge-release-verification.json)
and [desktop/mobile checks](evidence/hosted/judge-browser-verification.json) are dated
evidence, not proof of today's deployed revision.

Open **https://fieldsaarthi-ai.onrender.com** and choose **Open judge demo**.
No password is required. A free-host cold start can take a little time; leave the
page open and retry once if the service is waking up.

The judge session is read-only and displays only explicitly approved demonstration
reports. It cannot create/edit orders, use the microphone API, spend Gnani credits,
read unapproved reports or access team credentials. The team authorized publishing
the synthetic Hindi report **WO-AFF1E3EE3BD2**, including its transcript and audit.
New reports remain private unless deliberately approved for publication.

1. Inspect the approved sample. Search the work-order code and try status, priority
   and location filters. This scope is only participant-approved synthetic evidence,
   not the enterprise workload or a speech accuracy sample.
2. Open WO-AFF1E3EE3BD2. Inspect the original transcript, selected language, actual
   **Prisma v2.5** model/request ID, human-confirmed structured fields and creation
   audit. This participant report remains OPEN; no completed resolution is claimed
   for that report.
3. Compare the [genuine hosted supervisor workflow evidence](evidence/hosted/README.md)
   for a separate report that was assigned, started, resolved and retained after
   restart. The [participant microphone record](evidence/hosted/human-microphone-verification.json)
   documents the separate newly spoken sentence.
4. Review the [current verification record](evidence/judge-readiness.md),
   [architecture](architecture.md) and [requirement mapping](rtm.md).
   The original implementation roadmap and submission drafts are intentionally private.

To exercise recording and supervisor changes, use the intentionally published
[shared synthetic demo accounts](../README.md#demo-access). Sign out of the judge
session first. Activity is shared with other users of each account; use a new
synthetic report and preserve the approved judge example. Those accounts can:
record/upload a consenting short clip → call genuine Gnani → review/correct →
explicitly confirm → receive one durable order → assign/start/resolve → refresh.
The optional Timbre Hindi acknowledgment is generated only for a saved order.
A typed accessibility report is explicitly MANUAL_TEXT and is never claimed as
Gnani speech recognition.

The genuine development corpus covers Hindi, English and Hinglish: **14/15 nonempty
transcripts**, **12/15 automatic complete cases**, all **6/6 expected safety blocks**
and **3/3 explicit correction replays**. Ten hosted workflows reuse one consenting
clip and measure repeatability, not independent accuracy. Same-corpus refinement
was used; historical WER/CER and held-out results are unavailable. Tamil speech
remains unvalidated and excluded from acceptance. Automated provider fixtures are
test-only. No mock provider path exists in the deployed application.

Optional Timbre acknowledgment is disabled for the judge session to prevent paid
calls. Original provider transcript and original suggestions remain distinct from
corrected text/confirmed fields. TTS documentation reports requested and actually
returned model metadata separately; missing metadata is never inferred.

This is a synthetic challenge demo on free Render infrastructure. PostgreSQL expires
on the recorded date **2026-12-09** unless the hosting plan changes; the owner must
verify current expiry and backups. The [official challenge page](https://www.gnani.ai/internship),
checked November 14, gives **November 15, 2026 at 18:00 IST** as the final deadline.
Submission video, public post, participant attestations and the final official
form remain separate participant tasks.
