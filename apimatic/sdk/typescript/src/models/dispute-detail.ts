import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { dispute1Schema, type Dispute1 } from "./dispute1.js";
import { approvalIdSchema, type ApprovalId } from "./unions/approval-id.js";
import { evidencePackSchema, type EvidencePack } from "./unions/evidence-pack.js";

/** DisputeDetail object */
export type DisputeDetail = {
  /** The dispute */
  dispute: Dispute1;
  /** Defender's evidence pack, every fact citing a ledger id */
  evidencePack?: EvidencePack;
  /** Id of the pending approval for this action */
  approvalId?: ApprovalId;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const disputeDetailSchema: Schema<DisputeDetail> = s.object<DisputeDetail>(
  {
    dispute: dispute1Schema,
    evidencePack: s.optional(s.lazy(() => evidencePackSchema)),
    approvalId: s.optional(s.lazy(() => approvalIdSchema)),
    _keysMap: {
      evidencePack: "evidence_pack",
      approvalId: "approval_id",
    },
  },
  { additionalProperties: s.json() },
);
