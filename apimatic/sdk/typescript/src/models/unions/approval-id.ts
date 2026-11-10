import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Id of the pending approval for this action */
export type ApprovalId = string;

export const approvalIdSchema: Schema<ApprovalId> = s.of<ApprovalId>(s.union([s.string()]));
