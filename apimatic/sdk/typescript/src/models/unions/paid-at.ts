import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** When payment was verified (ISO 8601) */
export type PaidAt = Date;

export const paidAtSchema: Schema<PaidAt> = s.of<PaidAt>(s.union([s.dateTime()]));
