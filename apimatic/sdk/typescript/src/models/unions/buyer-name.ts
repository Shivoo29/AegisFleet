import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Buyer's name as PayPal reports it */
export type BuyerName = string;

export const buyerNameSchema: Schema<BuyerName> = s.of<BuyerName>(s.union([s.string()]));
