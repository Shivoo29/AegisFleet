import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Amount in minor units (cents) */
export type AmountCents = number;

export const amountCentsSchema: Schema<AmountCents> = s.of<AmountCents>(s.union([s.int()]));
