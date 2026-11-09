export interface User {
  id: string;
  display_name: string;
  email: string;
  role: "WORKER" | "SUPERVISOR";
}
export interface Location {
  id: string;
  name: string;
  code: string;
}
export interface Asset {
  id: string;
  name: string;
  location_id: string;
  asset_code: string;
}
export interface Intake {
  source_type: "GNANI_STT" | "MANUAL_TEXT";
  intake_id: string;
  status: string;
  raw_transcript: string;
  edited_transcript?: string;
  input_language_code: string;
  stt_latency_ms: number | null;
  audio_duration_seconds: number | null;
  provider: { name: string; model: string; request_id: string } | null;
  parser_version?: string | null;
  evidence_spans?: Record<
    string,
    { text: string; start: number; end: number }[]
  >;
  suggested_fields: {
    location_id: string | null;
    asset_id: string | null;
    issue_category: string;
    priority_suggestion: string;
  };
  field_evidence: Record<string, string[]>;
  unresolved_fields: string[];
  emergency_warning: boolean;
  possible_duplicates?: number;
}
export interface Audit {
  id: string;
  action: string;
  actor_name: string;
  from_state: string;
  to_state: string;
  details: Record<string, string | boolean | null>;
  occurred_at: string;
}
export interface Order {
  id: string;
  public_code: string;
  intake_id: string;
  asset_name: string;
  asset_id: string;
  location_name: string;
  location_id: string;
  description: string;
  issue_category: string;
  status: string;
  priority: string;
  priority_suggestion: string;
  assignee_id: string | null;
  assignee_name: string | null;
  version: number;
  created_at: string;
  updated_at: string;
  intake?: Intake;
  audit?: Audit[];
}
export interface Queue {
  items: Order[];
  total: number;
  page: number;
  page_size: number;
}

export class ApiError extends Error {
  code: string;
  status: number;
  constructor(message: string, code: string, status: number) {
    super(message);
    this.code = code;
    this.status = status;
  }
}
export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("X-Requested-With", "FieldSaarthi");
  if (options.body && !(options.body instanceof FormData))
    headers.set("Content-Type", "application/json");
  const response = await fetch("/api/v1" + path, {
    ...options,
    credentials: "same-origin",
    headers,
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new ApiError(
      data.error?.message || "The request could not be completed.",
      data.error?.code || "NETWORK_ERROR",
      response.status,
    );
  }
  return response.json() as Promise<T>;
}
export const label = (text: string) =>
  text
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/^./, (c) => c.toUpperCase());
export const date = (value: string) =>
  new Date(value).toLocaleString("en-IN", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });

export async function acknowledgmentAudio(orderId: string): Promise<Blob> {
  const response = await fetch(
    "/api/v1/work-orders/" + orderId + "/acknowledgment-audio",
    {
      method: "POST",
      credentials: "same-origin",
      headers: { "X-Requested-With": "FieldSaarthi" },
    },
  );
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(
      body.error?.message || "Audio is unavailable. Your report remains saved.",
    );
  }
  return response.blob();
}
