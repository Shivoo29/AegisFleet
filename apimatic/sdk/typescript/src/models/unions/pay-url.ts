import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** PayPal payment page for this invoice */
export type PayUrl = string;

export const payUrlSchema: Schema<PayUrl> = s.of<PayUrl>(s.union([s.string()]));
