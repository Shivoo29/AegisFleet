import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { outcomeSchema, type Outcome } from "./outcome.js";
import { approvalIdSchema, type ApprovalId } from "./unions/approval-id.js";
import { resultSchema, type Result } from "./unions/result.js";

/** Gateway decision for the executed action */
export type Decision2 = {
  /** allow, hold or deny */
  outcome: Outcome;
  /** Why */
  reason: string;
  /** Id of the pending approval for this action */
  approvalId?: ApprovalId;
  /** What the executed tool returned */
  result?: Result;
  /** Ledger entry that seals this */
  ledgerEntryId: number;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const decision2Schema: Schema<Decision2> = s.object<Decision2>(
  {
    outcome: outcomeSchema,
    reason: s.string(),
    approvalId: s.optional(s.lazy(() => approvalIdSchema)),
    result: s.optional(s.lazy(() => resultSchema)),
    ledgerEntryId: s.int(),
    _keysMap: {
      approvalId: "approval_id",
      ledgerEntryId: "ledger_entry_id",
    },
  },
  { additionalProperties: s.json() },
);
