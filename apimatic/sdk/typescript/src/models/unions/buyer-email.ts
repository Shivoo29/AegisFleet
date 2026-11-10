import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Buyer's email address */
export type BuyerEmail = string;

export const buyerEmailSchema: Schema<BuyerEmail> = s.of<BuyerEmail>(s.union([s.string()]));
