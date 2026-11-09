import { useState } from "react";
import { api } from "../lib/api";
import type { Intake } from "../lib/api";

export function ManualReport({
  language,
  onReady,
  onBusyChange,
}: {
  language: string;
  onReady: (intake: Intake) => void;
  onBusyChange: (busy: boolean) => void;
}) {
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  return (
    <details className="panel manual-report">
      <summary>Type a report instead</summary>
      <p className="field-help">
        Accessible text alternative. This does not use Gnani speech recognition.
        It is saved as a manual report and still needs your review and
        confirmation.
      </p>
      <form
        onSubmit={async (event) => {
          event.preventDefault();
          if (text.trim().length < 5 || busy) return;
          setBusy(true);
          onBusyChange(true);
          setError("");
          try {
            onReady(
              await api<Intake>("/intakes/manual", {
                method: "POST",
                body: JSON.stringify({ text, language_code: language }),
              }),
            );
          } catch (err) {
            setError(
              err instanceof Error
                ? err.message
                : "Could not prepare your report.",
            );
          } finally {
            setBusy(false);
            onBusyChange(false);
          }
        }}
      >
        <label>
          Typed report
          <textarea
            required
            minLength={5}
            maxLength={4000}
            rows={4}
            value={text}
            onChange={(event) => setText(event.target.value)}
          />
        </label>
        {error && (
          <div className="alert error" role="alert">
            {error}
          </div>
        )}
        <button
          className="button secondary"
          disabled={busy || text.trim().length < 5}
        >
          {busy ? "Preparing review…" : "Review typed report"}
        </button>
      </form>
    </details>
  );
}
