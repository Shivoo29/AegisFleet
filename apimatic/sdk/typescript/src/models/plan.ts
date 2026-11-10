import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { status3Schema, type Status3 } from "./status3.js";
import { outcome1Schema, type Outcome1 } from "./unions/outcome1.js";

/** Plan object */
export type Plan = {
  /** Unique id */
  id: string;
  /** Agent name: sentinel, defender, guardian or collector */
  agent: string;
  /** Gateway tool the agent called */
  tool: string;
  /** Tool arguments the agent asked the gateway to run */
  args: Record<string, unknown>;
  /** Why */
  reason: string;
  /** Title */
  title: string;
  /** What this is about: an invoice, dispute or email id */
  subjectId: string;
  /** Due at */
  dueAt: Date;
  /** Current status */
  status: Status3;
  /** allow, hold or deny */
  outcome?: Outcome1;
  /** When it was created (ISO 8601) */
  createdAt: Date;
  /** Updated at */
  updatedAt: Date;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const planSchema: Schema<Plan> = s.object<Plan>(
  {
    id: s.string(),
    agent: s.string(),
    tool: s.string(),
    args: s.record(s.string(), s.unknown()),
    reason: s.string(),
    title: s.string(),
    subjectId: s.string(),
    dueAt: s.dateTime(),
    status: status3Schema,
    outcome: s.optional(s.lazy(() => outcome1Schema)),
    createdAt: s.dateTime(),
    updatedAt: s.dateTime(),
    _keysMap: {
      subjectId: "subject_id",
      dueAt: "due_at",
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
  },
  { additionalProperties: s.json() },
);
