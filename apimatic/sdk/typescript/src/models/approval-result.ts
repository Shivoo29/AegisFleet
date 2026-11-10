import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { status1Schema, type Status1 } from "./status1.js";
import { decision1Schema, type Decision1 } from "./unions/decision1.js";

/** ApprovalResult object */
export type ApprovalResult = {
  /** Current status */
  status: Status1;
  /** Gateway decision for the executed action */
  decision?: Decision1;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const approvalResultSchema: Schema<ApprovalResult> = s.object<ApprovalResult>(
  {
    status: status1Schema,
    decision: s.optional(s.lazy(() => decision1Schema)),
  },
  { additionalProperties: s.json() },
);
