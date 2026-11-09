import { useEffect, useRef, useState } from "react";
import {
  ArrowLeft,
  CheckCircle2,
  ChevronRight,
  Clock3,
  FileCheck2,
  RefreshCw,
  ShieldCheck,
  UserRound,
  Volume2,
} from "lucide-react";
import { api, date, label, acknowledgmentAudio } from "../lib/api";
import type { Order, User } from "../lib/api";

export function Detail({ id, user }: { id: string; user: User }) {
  const [order, setOrder] = useState<Order | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [assignee, setAssignee] = useState("");
  const [priority, setPriority] = useState("NORMAL");
  const [note, setNote] = useState("");
  const [cancellationNote, setCancellationNote] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [duplicates, setDuplicates] = useState<Order[]>([]);
  const [ttsEnabled, setTtsEnabled] = useState(false);
  const [ttsBusy, setTtsBusy] = useState(false);
  const [ttsError, setTtsError] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const audioRef = useRef("");
  useEffect(
    () => () => {
      if (audioRef.current) URL.revokeObjectURL(audioRef.current);
    },
    [],
  );
  useEffect(() => {
    let active = true;
    api<{ tts_enabled: boolean }>("/work-orders/capabilities/audio")
      .then((x) => {
        if (active) setTtsEnabled(x.tts_enabled);
      })
      .catch(() => {});
    api<Order>("/work-orders/" + id)
      .then((x) => {
        if (active) {
          setOrder(x);
          setAssignee(x.assignee_id || "");
          setPriority(x.priority);
        }
      })
      .catch((err) => setError(err.message));
    api<Order[]>("/work-orders/" + id + "/duplicates")
      .then((x) => {
        if (active) setDuplicates(x);
      })
      .catch(() => {});
    if (user.role === "SUPERVISOR")
      api<User[]>("/users")
        .then((x) => {
          if (active) setUsers(x);
        })
        .catch((err) => setError(err.message));
    return () => {
      active = false;
    };
  }, [id, user.role]);
  async function update(action: string, body: Record<string, unknown>) {
    if (!order) return;
    setBusy(true);
    setError("");
    try {
      setOrder(
        await api<Order>("/work-orders/" + id + "/" + action, {
          method: "PATCH",
          body: JSON.stringify({ ...body, expected_version: order.version }),
        }),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Update failed.");
      if (err instanceof Error && err.message.includes("Refresh")) {
        const fresh = await api<Order>("/work-orders/" + id);
        setOrder(fresh);
      }
    } finally {
      setBusy(false);
    }
  }
  if (!order)
    return (
      <div className="empty-state" role="status">
        {error || "Loading work order…"}
      </div>
    );
  const closed = ["RESOLVED", "CANCELLED"].includes(order.status);
  const steps = ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED"];
  const step = steps.indexOf(order.status);
  return (
    <>
      <a className="back-link" href="#/orders">
        <ArrowLeft size={16} />
        Back to{" "}
        {user.role === "JUDGE"
          ? "judge dashboard"
          : user.role === "SUPERVISOR"
            ? "operations queue"
            : "my reports"}
      </a>
      <div className="page-heading detail-heading">
        <div>
          <div className="eyebrow">WORK ORDER / {order.public_code}</div>
          <h1>{order.asset_name}</h1>
          <p>
            {order.location_name} <span className="separator">/</span> Reported{" "}
            {date(order.created_at)}
          </p>
        </div>
        <span className={"status-badge large " + order.status.toLowerCase()}>
          <i />
          {label(order.status)}
        </span>
      </div>
      {error && (
        <div className="alert error" role="alert">
          {error}
        </div>
      )}
      {duplicates.length > 0 && (
        <div className="alert warning">
          {duplicates.length} other active report(s) for this asset:{" "}
          {duplicates.map((x) => (
            <a key={x.id} href={"#/orders/" + x.id}>
              {x.public_code}{" "}
            </a>
          ))}
        </div>
      )}
      <div className="workflow-track">
        {steps.map((state, i) => (
          <div key={state} className={i <= step ? "complete" : ""}>
            <span>{i < step ? <CheckCircle2 size={17} /> : i + 1}</span>
            <strong>{label(state)}</strong>
            {i < 3 && <ChevronRight size={16} />}
          </div>
        ))}
      </div>
      <div className="detail-grid">
        <div>
          <section className="panel">
            <div className="section-heading">
              <FileCheck2 size={20} />
              <h2>The reported issue</h2>
              <span className={"priority " + order.priority.toLowerCase()}>
                <i />
                {label(order.priority)} priority
              </span>
            </div>
            <p className="issue-description">{order.description}</p>
            <div className="info-grid">
              <div>
                <span>ISSUE CATEGORY</span>
                <strong>{label(order.issue_category)}</strong>
              </div>
              <div>
                <span>ASSIGNED TO</span>
                <strong>{order.assignee_name || "Awaiting assignment"}</strong>
              </div>
              <div>
                <span>REPORTER’S URGENCY CUE</span>
                <strong>{label(order.priority_suggestion)}</strong>
              </div>
              <div>
                <span>LAST UPDATED</span>
                <strong>{date(order.updated_at)}</strong>
              </div>
            </div>
          </section>
          <section className="panel timeline-panel">
            <div className="section-heading">
              <Clock3 size={20} />
              <h2>Every step, accounted for</h2>
              <span className="version">VERSION {order.version}</span>
            </div>
            <ol className="timeline">
              {order.audit?.map((event) => (
                <li key={event.id}>
                  <span className="timeline-dot">
                    <CheckCircle2 size={14} />
                  </span>
                  <div>
                    <div className="event-title">
                      <strong>{label(event.action)}</strong>
                      <time>{date(event.occurred_at)}</time>
                    </div>
                    <p>
                      {event.actor_name}
                      {event.to_state && (
                        <>
                          {" "}
                          <span>·</span> {label(event.to_state)}
                        </>
                      )}
                    </p>
                    {event.details.resolution_note && (
                      <blockquote>
                        {String(event.details.resolution_note)}
                      </blockquote>
                    )}
                    {event.details.cancellation_note && (
                      <blockquote>
                        {String(event.details.cancellation_note)}
                      </blockquote>
                    )}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        </div>
        <aside>
          <section className="panel provenance-panel">
            <div className="section-heading">
              <ShieldCheck size={20} />
              <h2>From voice to action</h2>
            </div>
            <span className="small-label">
              {order.intake?.source_type === "MANUAL_TEXT"
                ? "ORIGINAL MANUAL REPORT"
                : "ORIGINAL GNANI TRANSCRIPT"}
            </span>
            <blockquote className="original-transcript">
              {order.intake?.raw_transcript}
            </blockquote>
            {order.intake?.edited_transcript &&
              order.intake.edited_transcript !==
                order.intake.raw_transcript && (
                <>
                  <span className="small-label">REPORTER’S CORRECTION</span>
                  <p>{order.intake.edited_transcript}</p>
                </>
              )}
            <dl>
              <dt>Speech model</dt>
              <dd>
                {order.intake?.provider?.model ||
                  "Manual text — no speech recognition"}
              </dd>
              <dt>Provider request</dt>
              <dd className="mono">
                {order.intake?.provider?.request_id || "Not applicable"}
              </dd>
              <dt>Language selected</dt>
              <dd>{order.intake?.input_language_code}</dd>
            </dl>
            <div className="verified-note">
              <CheckCircle2 size={15} /> Human-confirmed before creation
            </div>
            {ttsEnabled && (
              <div className="acknowledgment">
                <button
                  className="button secondary full"
                  disabled={ttsBusy}
                  onClick={async () => {
                    setTtsBusy(true);
                    setTtsError("");
                    try {
                      const blob = await acknowledgmentAudio(order.id);
                      if (audioRef.current)
                        URL.revokeObjectURL(audioRef.current);
                      const url = URL.createObjectURL(blob);
                      audioRef.current = url;
                      setAudioUrl(url);
                    } catch (err) {
                      setTtsError(
                        err instanceof Error
                          ? err.message
                          : "Audio is unavailable. Your report remains saved.",
                      );
                    } finally {
                      setTtsBusy(false);
                    }
                  }}
                >
                  <Volume2 size={16} />
                  {ttsBusy
                    ? "Generating acknowledgment…"
                    : "Hear acknowledgment"}
                </button>
                <p className="field-help">
                  Gnani Timbre · Hindi spoken confirmation
                </p>
                {audioUrl && (
                  <audio
                    src={audioUrl}
                    controls
                    autoPlay
                    aria-label="Gnani spoken acknowledgment"
                  />
                )}
                {ttsError && (
                  <div className="alert warning" role="status">
                    {ttsError}
                  </div>
                )}
              </div>
            )}
          </section>
          {user.role === "SUPERVISOR" && !closed && (
            <section className="panel action-panel">
              <div className="section-heading">
                <UserRound size={20} />
                <h2>Move this forward</h2>
              </div>
              <label>
                Assign a worker
                <select
                  value={assignee}
                  onChange={(e) => setAssignee(e.target.value)}
                >
                  <option value="">Choose a worker</option>
                  {users.map((x) => (
                    <option key={x.id} value={x.id}>
                      {x.display_name}
                    </option>
                  ))}
                </select>
              </label>
              <button
                className="button secondary full"
                disabled={!assignee || busy}
                onClick={() => update("assignment", { assignee_id: assignee })}
              >
                Save assignment
              </button>
              <label>
                Supervisor priority
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
              <button
                className="button secondary full"
                disabled={busy || priority === order.priority}
                onClick={() => update("priority", { priority })}
              >
                Update priority
              </button>
              {order.status === "ASSIGNED" && (
                <button
                  className="button primary full"
                  disabled={busy}
                  onClick={() => update("status", { status: "IN_PROGRESS" })}
                >
                  Start work
                  <ChevronRight size={16} />
                </button>
              )}
              {order.status === "IN_PROGRESS" && (
                <>
                  <label>
                    Resolution note
                    <textarea
                      value={note}
                      onChange={(e) => setNote(e.target.value)}
                      rows={3}
                      placeholder="What was done to resolve the issue?"
                    />
                  </label>
                  <button
                    className="button primary full"
                    disabled={busy || !note.trim()}
                    onClick={() =>
                      update("status", {
                        status: "RESOLVED",
                        resolution_note: note,
                      })
                    }
                  >
                    <CheckCircle2 size={17} />
                    Mark resolved
                  </button>
                </>
              )}
              <label>
                Cancellation reason
                <textarea
                  value={cancellationNote}
                  maxLength={1000}
                  rows={2}
                  onChange={(event) => setCancellationNote(event.target.value)}
                  placeholder="Why should this work order be cancelled?"
                />
              </label>
              <button
                className="button text danger full"
                disabled={busy || !cancellationNote.trim()}
                onClick={() => {
                  if (
                    window.confirm(
                      "Cancel this work order? This action is recorded in the audit trail.",
                    )
                  )
                    update("status", {
                      status: "CANCELLED",
                      cancellation_note: cancellationNote,
                    });
                }}
              >
                Cancel work order
              </button>
            </section>
          )}
          <div className="detail-refresh">
            <RefreshCw size={14} /> Data is saved on the server. Refresh to
            verify.
          </div>
        </aside>
      </div>
    </>
  );
}
