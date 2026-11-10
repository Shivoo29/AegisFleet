import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { runIdSchema, type RunId } from "./unions/run-id.js";

/** ShipmentResult object */
export type ShipmentResult = {
  /** True on success */
  ok: boolean;
  /** True once the event is in the ledger */
  sealed: boolean;
  /** Agent run id */
  runId?: RunId;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const shipmentResultSchema: Schema<ShipmentResult> = s.object<ShipmentResult>(
  {
    ok: s.boolean(),
    sealed: s.boolean(),
    runId: s.optional(s.lazy(() => runIdSchema)),
    _keysMap: {
      runId: "run_id",
    },
  },
  { additionalProperties: s.json() },
);
