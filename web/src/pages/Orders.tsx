import { useEffect, useState } from "react";
import {
  ArrowDownRight,
  ArrowRight,
  CheckCheck,
  ClipboardList,
  Clock3,
  Plus,
  RefreshCw,
  Search,
} from "lucide-react";
import { api, date, label } from "../lib/api";
import type { Location, Queue, User } from "../lib/api";
import { navigate } from "../lib/navigation";

export function Orders({ user }: { user: User }) {
  const [queue, setQueue] = useState<Queue>({
    items: [],
    total: 0,
    page: 1,
    page_size: 20,
  });
  const [status, setStatus] = useState("");
  const [priority, setPriority] = useState("");
  const [location, setLocation] = useState("");
  const [assignee, setAssignee] = useState("");
  const [locations, setLocations] = useState<Location[]>([]);
  const [workers, setWorkers] = useState<User[]>([]);
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState("");
  const [revision, setRevision] = useState(0);
  useEffect(() => {
    let active = true;
    Promise.all([
      api<Location[]>("/locations"),
      user.role === "SUPERVISOR" ? api<User[]>("/users") : Promise.resolve([]),
    ])
      .then(([places, people]) => {
        if (active) {
          setLocations(places);
          setWorkers(people);
        }
      })
      .catch((err) => {
        if (active) setError(err.message);
      });
    return () => {
      active = false;
    };
  }, [user.role]);
  useEffect(() => {
    let active = true;
    const params = new URLSearchParams({
      page: String(page),
      page_size: "20",
      q,
    });
    if (status) params.set("status", status);
    if (priority) params.set("priority", priority);
    if (location) params.set("location_id", location);
    if (assignee) params.set("assignee_id", assignee);
    api<Queue>("/work-orders?" + params)
      .then((x) => {
        if (active) {
          setQueue(x);
          setError("");
        }
      })
      .catch((err) => {
        if (active) setError(err.message);
      })
      .finally(() => {
        if (active) setBusy(false);
      });
    return () => {
      active = false;
    };
  }, [status, priority, location, assignee, q, page, revision]);
  function filter(setter: (value: string) => void, value: string) {
    setBusy(true);
    setter(value);
    setPage(1);
  }
  const hasFilters = !!(q || status || priority || location || assignee);
  return (
    <>
      <div className="page-heading">
        <div>
          <div className="eyebrow">
            {user.role === "JUDGE"
              ? "JUDGE DEMO / VERIFIED EVIDENCE"
              : user.role === "SUPERVISOR"
                ? "OPERATIONS / LIVE QUEUE"
                : "YOUR REPORTS / ACTIVITY"}
          </div>
          <h1>
            {user.role === "JUDGE"
              ? "Inspect the work. Follow the evidence."
              : user.role === "SUPERVISOR"
                ? "Keep the field moving."
                : "From reported to resolved."}
          </h1>
          <p>
            {user.role === "JUDGE"
              ? "Approved demonstration reports, actual provider provenance and persisted history."
              : user.role === "SUPERVISOR"
                ? "Every issue has a next step. Put the right person on it."
                : "Your reports, their progress, and everything that happened along the way."}
          </p>
        </div>
        {user.role === "WORKER" && (
          <button className="button primary" onClick={() => navigate("/")}>
            <Plus size={17} />
            New voice report
          </button>
        )}
      </div>
      {user.role === "JUDGE" && (
        <div className="alert warning" role="status">
          Judge demo · read-only. Only team-approved synthetic demonstration
          reports are visible. Open a work order to inspect the actual
          transcript, Gnani request and persisted audit trail. Team accounts can
          record reports and perform supervisor actions.
        </div>
      )}
      <div className="metrics">
        <div className="metric">
          <span>REPORTS IN THIS FILTER</span>
          <div>
            <strong>{queue.total}</strong>
            <ClipboardList size={23} />
          </div>
          <small>Persisted work orders</small>
        </div>
        <div className="metric">
          <span>AWAITING ACTION · THIS PAGE</span>
          <div>
            <strong>
              {
                queue.items.filter((x) =>
                  ["OPEN", "ASSIGNED"].includes(x.status),
                ).length
              }
            </strong>
            <Clock3 size={23} />
          </div>
          <small>Open or assigned</small>
        </div>
        <div className="metric">
          <span>RESOLVED · THIS PAGE</span>
          <div>
            <strong>
              {queue.items.filter((x) => x.status === "RESOLVED").length}
            </strong>
            <CheckCheck size={23} />
          </div>
          <small>Completed by your team</small>
        </div>
      </div>
      <section className="queue-panel">
        <div className="queue-toolbar">
          <div className="tabs" role="group" aria-label="Filter by status">
            {[
              ["", "All reports"],
              ["OPEN", "Open"],
              ["ASSIGNED", "Assigned"],
              ["IN_PROGRESS", "In progress"],
              ["RESOLVED", "Resolved"],
              ["CANCELLED", "Cancelled"],
            ].map(([value, name]) => (
              <button
                key={value}
                className={status === value ? "selected" : ""}
                aria-pressed={status === value}
                onClick={() => {
                  setBusy(true);
                  setStatus(value);
                  setPage(1);
                }}
              >
                {name}
              </button>
            ))}
          </div>
          <button
            className="icon-button"
            title="Refresh queue"
            aria-label="Refresh queue"
            onClick={() => {
              setBusy(true);
              setRevision((x) => x + 1);
            }}
          >
            <RefreshCw size={16} />
          </button>
        </div>
        <div className="queue-filters">
          <label>
            Priority filter
            <select
              value={priority}
              onChange={(event) => filter(setPriority, event.target.value)}
            >
              <option value="">All priorities</option>
              {["LOW", "NORMAL", "HIGH"].map((value) => (
                <option key={value} value={value}>
                  {label(value)}
                </option>
              ))}
            </select>
          </label>
          <label>
            Location filter
            <select
              value={location}
              onChange={(event) => filter(setLocation, event.target.value)}
            >
              <option value="">All locations</option>
              {locations.map((place) => (
                <option key={place.id} value={place.id}>
                  {place.name}
                </option>
              ))}
            </select>
          </label>
          {user.role === "SUPERVISOR" && (
            <label>
              Assignee filter
              <select
                value={assignee}
                onChange={(event) => filter(setAssignee, event.target.value)}
              >
                <option value="">All assignees</option>
                {workers.map((person) => (
                  <option key={person.id} value={person.id}>
                    {person.display_name}
                  </option>
                ))}
              </select>
            </label>
          )}
          <button
            className="button small"
            onClick={() => {
              setBusy(true);
              setStatus("");
              setPriority("");
              setLocation("");
              setAssignee("");
              setQ("");
              setPage(1);
              setRevision((value) => value + 1);
            }}
          >
            Clear filters
          </button>
        </div>
        <div className="search-row">
          <Search size={17} />
          <input
            aria-label="Search work orders"
            placeholder="Search a work order or issue…"
            value={q}
            onChange={(e) => {
              setBusy(true);
              setQ(e.target.value);
              setPage(1);
            }}
          />
          <span>
            {queue.total} work order{queue.total === 1 ? "" : "s"}
          </span>
        </div>
        {error && (
          <div className="alert error" role="alert">
            {error}
          </div>
        )}
        {busy ? (
          <div className="empty-state" role="status">
            <RefreshCw className="pulse" />
            <h3>Getting the latest reports…</h3>
          </div>
        ) : queue.items.length ? (
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>WORK ORDER / ISSUE</th>
                  <th>LOCATION & ASSET</th>
                  <th>STATUS</th>
                  <th>PRIORITY</th>
                  <th>ASSIGNED TO</th>
                  <th>REPORTED</th>
                  <th>
                    <span className="sr-only">Open</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {queue.items.map((order) => (
                  <tr key={order.id}>
                    <td>
                      <a className="order-code" href={"#/orders/" + order.id}>
                        {order.public_code}
                      </a>
                      <p className="table-description">{order.description}</p>
                    </td>
                    <td>
                      <strong>{order.asset_name}</strong>
                      <span>{order.location_name}</span>
                    </td>
                    <td>
                      <span
                        className={"status-badge " + order.status.toLowerCase()}
                      >
                        <i />
                        {label(order.status)}
                      </span>
                    </td>
                    <td>
                      <span
                        className={"priority " + order.priority.toLowerCase()}
                      >
                        <i />
                        {label(order.priority)}
                      </span>
                    </td>
                    <td>
                      {order.assignee_name || (
                        <span className="unassigned">Unassigned</span>
                      )}
                    </td>
                    <td className="time-cell">{date(order.created_at)}</td>
                    <td>
                      <a
                        className="icon-button"
                        aria-label={"Open " + order.public_code}
                        href={"#/orders/" + order.id}
                      >
                        <ArrowDownRight size={18} />
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <ClipboardList size={35} />
            <h3>
              {hasFilters
                ? "No reports match this view."
                : "A clearer day starts here."}
            </h3>
            <p>
              {hasFilters
                ? "Try a different search or filter."
                : user.role === "WORKER"
                  ? "Report your first issue with a short voice recording."
                  : "New worker reports will appear here after they are reviewed and confirmed."}
            </p>
            {user.role === "WORKER" && !hasFilters && (
              <button className="button primary" onClick={() => navigate("/")}>
                Make your first report
                <ArrowRight size={16} />
              </button>
            )}
          </div>
        )}
        <div className="table-footer">
          <span>
            Page {page} · {queue.items.length} shown of {queue.total}
          </span>
          <div>
            <button
              className="button small"
              disabled={page === 1}
              onClick={() => {
                setBusy(true);
                setPage(page - 1);
              }}
            >
              Previous
            </button>
            <button
              className="button small"
              disabled={page * 20 >= queue.total}
              onClick={() => {
                setBusy(true);
                setPage(page + 1);
              }}
            >
              Next
            </button>
          </div>
        </div>
      </section>
      <div className="queue-caption">
        <span className="tiny-dot" />
        Every work order records its voice or manual source and explicit human
        confirmation.
      </div>
    </>
  );
}
