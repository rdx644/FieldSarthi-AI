import { useEffect, useRef, useState } from "react";
import {
  ArrowRight,
  AudioLines,
  Check,
  CircleHelp,
  FileAudio,
  Mic,
  RotateCcw,
  ShieldCheck,
  Square,
  Upload,
  X,
} from "lucide-react";
import { api } from "../lib/api";
import type { Intake } from "../lib/api";
import { Review } from "./Review";
import { ManualReport } from "./ManualReport";

export function Report() {
  const [language, setLanguage] = useState("hi-IN");
  const [recording, setRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [audio, setAudio] = useState<Blob | null>(null);
  const [preview, setPreview] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [intake, setIntake] = useState<Intake | null>(null);
  const [fileName, setFileName] = useState("");
  const recorder = useRef<MediaRecorder | null>(null);
  const stream = useRef<MediaStream | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const started = useRef(0);
  const stopTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const previewRef = useRef("");
  function chooseAudio(blob: Blob | null) {
    if (previewRef.current) URL.revokeObjectURL(previewRef.current);
    const url = blob ? URL.createObjectURL(blob) : "";
    previewRef.current = url;
    setAudio(blob);
    setPreview(url);
  }

  useEffect(() => {
    if (!recording) return;
    const timer = setInterval(
      () =>
        setSeconds(
          Math.min(25, Math.floor((Date.now() - started.current) / 1000)),
        ),
      250,
    );
    return () => clearInterval(timer);
  }, [recording]);
  useEffect(
    () => () => {
      if (stopTimer.current) clearTimeout(stopTimer.current);
      if (recorder.current?.state === "recording") {
        recorder.current.onstop = null;
        recorder.current.stop();
      }
      if (previewRef.current) URL.revokeObjectURL(previewRef.current);
      stream.current?.getTracks().forEach((x) => x.stop());
    },
    [],
  );
  function stop() {
    if (recorder.current?.state === "recording") recorder.current.stop();
    if (stopTimer.current) clearTimeout(stopTimer.current);
    setRecording(false);
    stream.current?.getTracks().forEach((x) => x.stop());
  }
  async function start() {
    setError("");
    chooseAudio(null);
    setSeconds(0);
    setFileName("");
    try {
      if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder)
        throw new Error(
          "Microphone recording needs a supported browser on HTTPS or localhost. You can upload an audio file instead.",
        );
      const media = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.current = media;
      const mime = [
        "audio/webm;codecs=opus",
        "audio/mp4",
        "audio/ogg;codecs=opus",
      ].find((x) => MediaRecorder.isTypeSupported(x));
      const rec = new MediaRecorder(
        media,
        mime ? { mimeType: mime } : undefined,
      );
      recorder.current = rec;
      const chunks: Blob[] = [];
      rec.ondataavailable = (e) => {
        if (e.data.size) chunks.push(e.data);
      };
      rec.onstop = () => {
        chooseAudio(new Blob(chunks, { type: rec.mimeType }));
        setRecording(false);
        media.getTracks().forEach((x) => x.stop());
      };
      rec.start();
      started.current = Date.now();
      setRecording(true);
      stopTimer.current = setTimeout(stop, 25000);
    } catch (err) {
      stream.current?.getTracks().forEach((x) => x.stop());
      setError(
        err instanceof DOMException && err.name === "NotAllowedError"
          ? "Microphone access was denied. Allow microphone access in your browser settings, or upload a recording."
          : err instanceof Error
            ? err.message
            : "Could not start recording.",
      );
    }
  }
  async function transcribe() {
    if (!audio) return;
    setBusy(true);
    setError("");
    const form = new FormData();
    form.append(
      "audio_file",
      audio,
      fileName ||
        "report." +
          (audio.type.includes("mp4")
            ? "m4a"
            : audio.type.includes("wav")
              ? "wav"
              : "webm"),
    );
    form.append("language_code", language);
    try {
      setIntake(
        await api<Intake>("/intakes/transcribe", {
          method: "POST",
          body: form,
        }),
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Transcription failed. Please retry.",
      );
    } finally {
      setBusy(false);
    }
  }
  if (intake) return <Review intake={intake} onBack={() => setIntake(null)} />;
  return (
    <>
      <div className="page-heading">
        <div>
          <div className="eyebrow">VOICE REPORTING / 01</div>
          <h1>
            A few words.
            <br className="mobile-break" /> A problem on its way to a fix.
          </h1>
          <p>
            Tell us what happened. We’ll help you turn it into a clear,
            actionable report.
          </p>
        </div>
        <span className="outline-tag">
          <ShieldCheck size={14} /> Human review required
        </span>
      </div>
      <div className="report-grid">
        <section className="recorder-card">
          <div className="card-title">
            <span className="step-number">01</span>
            <div>
              <h2>Start with your voice</h2>
              <p>Speak naturally. Your team’s next step starts here.</p>
            </div>
            <span className="audio-format">UP TO 25 SEC</span>
          </div>
          <div className="language-picker">
            <span className="small-label">I’LL BE SPEAKING IN</span>
            <div role="group" aria-label="Recording language">
              {[
                ["hi-IN", "हिन्दी", "Hindi"],
                ["en-IN", "English", "English"],
                ["ta-IN", "தமிழ்", "Tamil"],
              ].map(([code, name, accessible]) => (
                <button
                  key={code}
                  aria-label={accessible}
                  aria-pressed={language === code}
                  disabled={recording || busy}
                  className={
                    language === code ? "language selected" : "language"
                  }
                  onClick={() => setLanguage(code)}
                >
                  {name}
                  {language === code && <Check size={13} />}
                </button>
              ))}
            </div>
          </div>
          <div className={"record-stage " + (recording ? "is-recording" : "")}>
            <div className="record-rings">
              <button
                className="record-button"
                aria-label={recording ? "Stop recording" : "Start recording"}
                onClick={recording ? stop : start}
                disabled={busy}
              >
                {recording ? (
                  <Square size={27} fill="currentColor" />
                ) : (
                  <Mic size={35} />
                )}
              </button>
            </div>
            <div className="waveform" aria-hidden="true">
              {Array.from({ length: 37 }, (_, i) => (
                <span key={i} className={"bar bar-" + (i % 9)} />
              ))}
            </div>
            <h3>
              {recording
                ? "Listening. Tell us what happened."
                : audio
                  ? "Your report is ready to listen to."
                  : "Tap the mic. Tell your story."}
            </h3>
            <p>
              {recording
                ? "Tap stop when you’re done. Recording ends at 25 seconds."
                : audio
                  ? "Listen once before sending it for transcription."
                  : "Include the location, equipment and what went wrong."}
            </p>
            <div className="record-time">
              <span className={recording ? "live-dot red" : "tiny-dot"} />
              {recording
                ? "00:" + String(seconds).padStart(2, "0")
                : audio
                  ? fileName || "Recording captured"
                  : "00:00"}
              <span className="muted">/ 00:25</span>
            </div>
          </div>
          {audio && (
            <div className="audio-preview">
              <audio controls src={preview} aria-label="Your recorded report" />
              <button
                className="icon-button"
                aria-label="Discard recording"
                onClick={() => {
                  chooseAudio(null);
                  setFileName("");
                }}
                disabled={busy}
              >
                <X size={18} />
              </button>
            </div>
          )}
          {error && (
            <div className="alert error" role="alert">
              {error}
            </div>
          )}
          {busy && (
            <div className="processing" role="status">
              <AudioLines className="pulse" />
              Transcribing with Gnani Prisma… Your work order won’t be created
              until you review.
            </div>
          )}
          <div className="record-actions">
            <input
              ref={fileInput}
              type="file"
              hidden
              accept="audio/*,.webm,.m4a"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) {
                  if (file.size > 10485760) {
                    setError("Choose a recording under 10 MiB.");
                    return;
                  }
                  chooseAudio(file);
                  setFileName(file.name);
                  setError("");
                }
                e.target.value = "";
              }}
            />
            <button
              className="button text"
              onClick={() => fileInput.current?.click()}
              disabled={recording || busy}
            >
              <Upload size={16} />
              Upload audio instead
            </button>
            {audio ? (
              <button
                className="button primary"
                onClick={transcribe}
                disabled={busy || recording}
              >
                {busy ? "Transcribing…" : "Transcribe report"}
                <ArrowRight size={17} />
              </button>
            ) : (
              <span className="small-muted">
                Your microphone is only on while recording.
              </span>
            )}
          </div>
        </section>
        <aside className="report-help">
          <div className="helper-card">
            <div className="helper-icon">
              <CircleHelp size={21} />
            </div>
            <span className="small-label">A GOOD REPORT TAKES SECONDS</span>
            <h3>
              Give your team
              <br />
              the full picture.
            </h3>
            <ol className="tips">
              <li>
                <span>01</span>
                <div>
                  <strong>Where is it?</strong>
                  <p>The building, floor or working area.</p>
                </div>
              </li>
              <li>
                <span>02</span>
                <div>
                  <strong>What needs attention?</strong>
                  <p>Name the equipment or asset.</p>
                </div>
              </li>
              <li>
                <span>03</span>
                <div>
                  <strong>What’s the issue?</strong>
                  <p>Describe the fault and any urgency.</p>
                </div>
              </li>
            </ol>
            <div className="example">
              <span>FOR EXAMPLE</span>
              <p>
                “Block B second floor ka water pump leak ho raha hai, urgent
                repair chahiye.”
              </p>
            </div>
          </div>
          <div className="privacy-note">
            <FileAudio size={19} />
            <p>
              <strong>Your recording stays temporary.</strong>
              <br />
              Audio is sent to Gnani AI for transcription and discarded from
              this app after processing. Gnani processes it under its own terms.
              Your transcript and audit history stay with the report while this
              demo database is retained. Use consenting voices and synthetic
              details.
            </p>
          </div>
        </aside>
      </div>
      {!recording && !busy && (
        <ManualReport language={language} onReady={setIntake} />
      )}
      <div className="next-step">
        <div className="next-icon">
          <RotateCcw size={18} />
        </div>
        <div>
          <strong>Nothing is submitted without your say-so.</strong>
          <p>
            Next, you’ll see the transcript, check the details, and confirm the
            report.
          </p>
        </div>
        <span>
          UP NEXT <ArrowRight size={14} /> REVIEW & CONFIRM
        </span>
      </div>
    </>
  );
}
