import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { runIdSchema, type RunId } from "./unions/run-id.js";
import { status21Schema, type Status21 } from "./unions/status21.js";
import { verdictSchema, type Verdict } from "./unions/verdict.js";

/** InboxVerdict object */
export type InboxVerdict = {
  /** Agent run id */
  runId?: RunId;
  /** Current status */
  status?: Status21;
  /** Sentinel verdict: scam | legit | unsure, with red flags */
  verdict?: Verdict;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const inboxVerdictSchema: Schema<InboxVerdict> = s.object<InboxVerdict>(
  {
    runId: s.optional(s.lazy(() => runIdSchema)),
    status: s.optional(s.lazy(() => status21Schema)),
    verdict: s.optional(s.lazy(() => verdictSchema)),
    _keysMap: {
      runId: "run_id",
    },
  },
  { additionalProperties: s.json() },
);
