import { useEffect, useState } from "react";
import {
  Activity,
  ArrowRight,
  AudioLines,
  ClipboardList,
  LogOut,
  ShieldCheck,
  Radio,
  Menu,
  X,
} from "lucide-react";
import { api } from "./lib/api";
import type { User } from "./lib/api";
import { Report } from "./pages/Report";
import { Orders } from "./pages/Orders";
import { Detail } from "./pages/Detail";
import "./styles.css";
import { navigate } from "./lib/navigation";

function Login({ onLogin }: { onLogin: (user: User) => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <main className="login-layout">
      <section className="login-story">
        <a className="brand" href="#/">
          <span className="brand-mark">
            <AudioLines size={24} />
          </span>
          FieldSaarthi<span className="brand-ai">AI</span>
        </a>
        <div className="story-copy">
          <div className="eyebrow">
            <span className="live-dot" /> SPEAK. VERIFY. GET IT DONE.
          </div>
          <h1>
            Every voice.
            <br />A clear <em>next step.</em>
          </h1>
          <p>
            From a fault on the floor to a fix in the field. Turn everyday voice
            reports into work your team can act on.
          </p>
          <div className="voice-card">
            <AudioLines size={32} />
            <div>
              <strong>Built for the way your team speaks</strong>
              <span>Hindi · English · Tamil</span>
            </div>
          </div>
          <div className="story-flow">
            <span>01 / Speak</span>
            <ArrowRight size={16} />
            <span>02 / Review</span>
            <ArrowRight size={16} />
            <span>03 / Resolve</span>
          </div>
        </div>
        <div className="story-footer">
          <ShieldCheck size={16} /> Genuine Gnani Prisma speech recognition{" "}
          <span>HUMAN VERIFIED, ALWAYS</span>
        </div>
      </section>
      <section className="login-form-panel">
        <div className="login-form-wrap">
          <span className="small-label">YOUR FIELD OPERATIONS WORKSPACE</span>
          <h2>Welcome back.</h2>
          <p className="muted">
            Sign in to report a fault or keep your team moving.
          </p>
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              setBusy(true);
              setError("");
              try {
                const result = await api<{ user: User }>("/auth/login", {
                  method: "POST",
                  body: JSON.stringify({ email, password }),
                });
                onLogin(result.user);
              } catch (err) {
                setError(
                  err instanceof Error ? err.message : "Unable to sign in.",
                );
              } finally {
                setBusy(false);
              }
            }}
          >
            <label>
              Email address
              <input
                type="email"
                autoComplete="username"
                placeholder="you@your-team.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
            <label>
              Password
              <input
                type="password"
                autoComplete="current-password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {error && (
              <div role="alert" className="alert error">
                {error}
              </div>
            )}
            <button className="button primary full" disabled={busy}>
              {busy ? "Signing in…" : "Enter workspace"}
              <ArrowRight size={18} />
            </button>
          </form>
          <div className="demo-note">
            <ShieldCheck size={19} />
            <p>
              <strong>A safe space to demonstrate.</strong>
              <br />
              This workspace uses synthetic people, locations and equipment. Use
              the credentials provided by your team.
            </p>
          </div>
        </div>
        <span className="login-bottom">
          FIELD INTELLIGENCE. HUMAN ACCOUNTABILITY.
        </span>
      </section>
    </main>
  );
}

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [route, setRoute] = useState(window.location.hash.slice(1) || "/");
  const [today] = useState(() =>
    new Date().toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    }),
  );
  const [mobileNav, setMobileNav] = useState(false);
  useEffect(() => {
    api<{ user: User | null }>("/auth/session")
      .then((result) => setUser(result.user))
      .catch(() => {})
      .finally(() => setLoading(false));
    const handler = () => {
      setRoute(window.location.hash.slice(1) || "/");
      setMobileNav(false);
    };
    window.addEventListener("hashchange", handler);
    return () => window.removeEventListener("hashchange", handler);
  }, []);
  if (loading)
    return (
      <div className="boot">
        <AudioLines size={35} />
        <p>Opening your workspace…</p>
      </div>
    );
  if (!user)
    return (
      <Login
        onLogin={(u) => {
          setUser(u);
          navigate(u.role === "SUPERVISOR" ? "/orders" : "/");
        }}
      />
    );
  const detailId = route.startsWith("/orders/") ? route.split("/")[2] : null;
  const operations = route.startsWith("/orders") || user.role === "SUPERVISOR";
  return (
    <div className="app-shell">
      <a
        className="skip-link"
        href="#main"
        onClick={(e) => {
          e.preventDefault();
          document.getElementById("main")?.focus();
        }}
      >
        Skip to content
      </a>
      <aside className={"sidebar " + (mobileNav ? "mobile-open" : "")}>
        <a className="brand" href="#/">
          <span className="brand-mark">
            <AudioLines size={22} />
          </span>
          FieldSaarthi<span className="brand-ai">AI</span>
        </a>
        <div className="workspace-label">
          <span className="workspace-icon">F</span>
          <div>
            <strong>Field operations</strong>
            <span>Demonstration workspace</span>
          </div>
          <span className="tiny-dot" />
        </div>
        <div className="nav-label">WORKSPACE</div>
        <nav aria-label="Main navigation">
          {user.role === "WORKER" && (
            <button
              className={!operations ? "nav-item active" : "nav-item"}
              onClick={() => navigate("/")}
            >
              <Radio size={19} />
              Report an issue<span className="nav-key">01</span>
            </button>
          )}
          <button
            className={operations ? "nav-item active" : "nav-item"}
            onClick={() => navigate("/orders")}
          >
            <ClipboardList size={19} />
            {user.role === "SUPERVISOR" ? "Operations queue" : "My reports"}
            <span className="nav-key">
              {user.role === "SUPERVISOR" ? "01" : "02"}
            </span>
          </button>
        </nav>
        <div className="sidebar-bottom">
          <div className="trust-note">
            <ShieldCheck size={21} />
            <strong>Your voice, with a trail.</strong>
            <p>
              Every report keeps the original transcript and a history of what
              happened next.
            </p>
            <span>POWERED BY GNANI PRISMA</span>
          </div>
          <div className="user-block">
            <div className="avatar">
              {user.display_name
                .split(" ")
                .map((x) => x[0])
                .join("")}
            </div>
            <div>
              <strong>{user.display_name}</strong>
              <span>
                {user.role === "SUPERVISOR"
                  ? "Operations supervisor"
                  : "Field reporter"}
              </span>
            </div>
            <button
              aria-label="Sign out"
              title="Sign out"
              className="icon-button"
              onClick={async () => {
                await api("/auth/logout", { method: "POST" });
                setUser(null);
                navigate("/");
              }}
            >
              <LogOut size={17} />
            </button>
          </div>
        </div>
      </aside>
      <div className="workspace">
        <header className="topbar">
          <button
            className="icon-button mobile-menu"
            aria-label="Toggle navigation"
            onClick={() => setMobileNav(!mobileNav)}
          >
            {mobileNav ? <X /> : <Menu />}
          </button>
          <div className="breadcrumb">
            Workspace <span>/</span>{" "}
            <strong>
              {detailId
                ? "Work order"
                : operations
                  ? "Operations"
                  : "Voice reporting"}
            </strong>
          </div>
          <div className="environment">
            <span className="live-dot" />
            SYNTHETIC DEMO DATA
          </div>
          <div className="top-date">{today}</div>
        </header>
        <main id="main" className="main-content" tabIndex={-1}>
          {detailId ? (
            <Detail id={detailId} user={user} />
          ) : operations ? (
            <Orders user={user} />
          ) : (
            <Report />
          )}
        </main>
        <footer className="workspace-footer">
          <span>
            <Activity size={13} /> FieldSaarthi AI · Voice to accountable action
          </span>
          <span>People make the final call.</span>
        </footer>
      </div>
    </div>
  );
}
