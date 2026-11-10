import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** ApprovalBody object */
export type ApprovalBody = {
  /** Optional reason, sealed into the ledger with the decision */
  note?: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const approvalBodySchema: Schema<ApprovalBody> = s.object<ApprovalBody>(
  {
    note: s.optional(s.string()),
  },
  { additionalProperties: s.json() },
);
