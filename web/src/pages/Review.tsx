import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Check,
  ShieldCheck,
  Sparkles,
  AlertTriangle,
} from "lucide-react";
import { api, label } from "../lib/api";
import type { Asset, Intake, Location, Order } from "../lib/api";
import { navigate } from "../lib/navigation";

export function Review({
  intake,
  onBack,
}: {
  intake: Intake;
  onBack: () => void;
}) {
  const [locations, setLocations] = useState<Location[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [location, setLocation] = useState(
    intake.suggested_fields.location_id || "",
  );
  const [asset, setAsset] = useState(intake.suggested_fields.asset_id || "");
  const [issue, setIssue] = useState(intake.suggested_fields.issue_category);
  const [priority, setPriority] = useState(
    intake.suggested_fields.priority_suggestion,
  );
  const [description, setDescription] = useState(intake.raw_transcript);
  const [edited, setEdited] = useState(
    intake.edited_transcript || intake.raw_transcript,
  );
  const [confirmed, setConfirmed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [key, setKey] = useState(() => crypto.randomUUID());
  useEffect(() => {
    Promise.all([api<Location[]>("/locations"), api<Asset[]>("/assets")])
      .then(([l, a]) => {
        setLocations(l);
        setAssets(a);
      })
      .catch((err) => setError(err.message));
  }, []);

  const missing = !location || !asset || description.trim().length < 5;
  const descriptionTooLong = description.trim().length > 2000;
  return (
    <>
      <button className="back-link" onClick={onBack}>
        <ArrowLeft size={16} />
        Back to recording
      </button>
      <div className="page-heading">
        <div>
          <div className="eyebrow">VOICE REPORTING / 02</div>
          <h1>Your words. The right next step.</h1>
          <p>
            Check what we heard, correct anything that needs it, then make it a
            work order.
          </p>
        </div>
        <span className="outline-tag">
          <ShieldCheck size={14} /> Review before creating
        </span>
      </div>
      {intake.emergency_warning && (
        <div className="alert warning">
          <AlertTriangle size={19} />
          Possible safety risk. Follow your organization’s emergency protocol
          for immediate danger. This report does not dispatch emergency help.
        </div>
      )}
      {!!intake.possible_duplicates && (
        <div className="alert warning">
          You have {intake.possible_duplicates} open report(s) for this asset.
          Check your reports before creating another.
        </div>
      )}
      <div className="review-grid">
        <section className="panel">
          <div className="card-title">
            <span className="step-number">
              <Check size={17} />
            </span>
            <div>
              <h2>
                {intake.source_type === "MANUAL_TEXT"
                  ? "Your typed report"
                  : "What Gnani heard"}
              </h2>
              <p>The original transcript is preserved with your report.</p>
            </div>
          </div>
          <blockquote
            className="transcript"
            lang={intake.input_language_code.split("-")[0]}
          >
            {intake.raw_transcript}
          </blockquote>
          <div className="provider-strip">
            <span className="live-dot" />
            <strong>
              {intake.provider?.model || "MANUAL TEXT · No speech recognition"}
            </strong>
            {intake.stt_latency_ms !== null && (
              <span>
                {(intake.stt_latency_ms / 1000).toFixed(1)}s speech request
              </span>
            )}
          </div>
          <details className="provenance">
            <summary>View speech recognition provenance</summary>
            <dl>
              <dt>Provider</dt>
              <dd>
                {intake.provider?.name || "Manual text — no provider call"}
              </dd>
              <dt>Request ID</dt>
              <dd className="mono">
                {intake.provider?.request_id || "Not applicable"}
              </dd>
              <dt>Selected language</dt>
              <dd>{intake.input_language_code}</dd>
              <dt>Audio duration</dt>
              <dd>
                {intake.audio_duration_seconds === null
                  ? "Not applicable"
                  : intake.audio_duration_seconds.toFixed(2) + "s"}
              </dd>
              <dt>Parser version</dt>
              <dd>{intake.parser_version || "Historical record"}</dd>
            </dl>
          </details>
          <label>
            Corrected transcript <span className="optional">optional</span>
            <textarea
              rows={4}
              value={edited}
              onChange={(e) => {
                setEdited(e.target.value);
                setKey(crypto.randomUUID());
                setConfirmed(false);
              }}
            />
          </label>
          <p className="field-help">
            Your corrections are stored separately. The original transcript
            stays unchanged.
          </p>
          <div className="evidence-box">
            <Sparkles size={16} />
            <div>
              <strong>Why these suggestions?</strong>
              {Object.entries(intake.field_evidence)
                .filter(([, v]) => v.length)
                .map(([field, values]) => (
                  <p key={field}>
                    <span>{label(field)}:</span> {values.join(", ")}
                  </p>
                ))}
              {!!intake.unresolved_fields.length && (
                <p>
                  Choose missing or ambiguous details:{" "}
                  {intake.unresolved_fields.map(label).join(", ")}.
                </p>
              )}
            </div>
          </div>
        </section>
        <form
          className="panel review-form"
          onChange={(e) => {
            if (!(
              e.target instanceof HTMLInputElement &&
              e.target.type === "checkbox"
            )) {
              setKey(crypto.randomUUID());
              setConfirmed(false);
            }
          }}
          onSubmit={async (e) => {
            e.preventDefault();
            if (missing || descriptionTooLong || !confirmed) return;
            setBusy(true);
            setError("");
            try {
              const order = await api<Order>("/work-orders", {
                method: "POST",
                headers: { "Idempotency-Key": key },
                body: JSON.stringify({
                  intake_id: intake.intake_id,
                  location_id: location,
                  asset_id: asset,
                  issue_category: issue,
                  description,
                  priority_suggestion: priority,
                  edited_transcript: edited,
                  confirmed: true,
                }),
              });
              navigate("/orders/" + order.id);
            } catch (err) {
              setError(
                err instanceof Error
                  ? err.message
                  : "Could not create work order.",
              );
            } finally {
              setBusy(false);
            }
          }}
        >
          <div className="card-title">
            <span className="step-number">02</span>
            <div>
              <h2>Make the details count</h2>
              <p>Suggestions need your confirmation.</p>
            </div>
          </div>
          <label>
            Location
            <select
              required
              value={location}
              onChange={(e) => {
                setLocation(e.target.value);
                setAsset("");
              }}
            >
              <option value="">Select a known location</option>
              {locations.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Equipment / asset
            <select
              required
              value={asset}
              onChange={(e) => setAsset(e.target.value)}
              disabled={!location}
            >
              <option value="">Select equipment</option>
              {assets
                .filter((a) => a.location_id === location)
                .map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.name}
                  </option>
                ))}
            </select>
          </label>
          <div className="form-row">
            <label>
              Issue category
              <select value={issue} onChange={(e) => setIssue(e.target.value)}>
                {[
                  "LEAKAGE",
                  "ELECTRICAL",
                  "MECHANICAL",
                  "CLEANING",
                  "OTHER",
                ].map((x) => (
                  <option key={x} value={x}>
                    {label(x)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Urgency suggestion
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
              >
                {["LOW", "NORMAL", "HIGH"].map((x) => (
                  <option key={x} value={x}>
                    {label(x)}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <p className="field-help">
            Your supervisor makes the final priority decision.
          </p>
          <label>
            Issue description
            <textarea
              minLength={5}
              maxLength={2000}
              aria-invalid={descriptionTooLong}
              aria-describedby={
                descriptionTooLong ? "description-length-error" : undefined
              }
              rows={4}
              required
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </label>
          {descriptionTooLong && (
            <p
              id="description-length-error"
              className="validation-note"
              role="alert"
            >
              Shorten the issue description to 2000 characters or fewer. Your
              full original report is preserved.
            </p>
          )}
          {missing && (
            <p className="validation-note">
              Choose a known location and equipment, and describe the issue
              before continuing.
            </p>
          )}
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={confirmed}
              onChange={(e) => setConfirmed(e.target.checked)}
            />
            <span>
              I’ve checked the details and want to create this work order.
            </span>
          </label>
          {error && (
            <div className="alert error" role="alert">
              {error}
            </div>
          )}
          <button
            className="button primary full"
            disabled={!confirmed || missing || descriptionTooLong || busy}
          >
            {busy ? "Creating work order…" : "Confirm & create work order"}
            <ArrowRight size={17} />
          </button>
          <span className="small-muted centered">
            One confirmation. One traceable work order.
          </span>
        </form>
      </div>
    </>
  );
}
