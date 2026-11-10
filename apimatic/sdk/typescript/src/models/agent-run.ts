import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { outputSchema, type Output } from "./unions/output.js";

/** AgentRun object */
export type AgentRun = {
  /** Unique id */
  id: string;
  /** Agent name: sentinel, defender, guardian or collector */
  agent: string;
  /** Event that started the run, e.g. dispute.created */
  eventType: string;
  /** Current status */
  status: string;
  /** Each step the agent took */
  steps: Record<string, unknown>[];
  /** Agent's structured result */
  output?: Output;
  /** When the run started (ISO 8601) */
  startedAt: Date;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const agentRunSchema: Schema<AgentRun> = s.object<AgentRun>(
  {
    id: s.string(),
    agent: s.string(),
    eventType: s.string(),
    status: s.string(),
    steps: s.array(s.record(s.string(), s.unknown())),
    output: s.optional(s.lazy(() => outputSchema)),
    startedAt: s.dateTime(),
    _keysMap: {
      eventType: "event_type",
      startedAt: "started_at",
    },
  },
  { additionalProperties: s.json() },
);
