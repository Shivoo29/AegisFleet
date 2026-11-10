import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** First ledger id whose hash no longer matches */
export type BrokenAt = number;

export const brokenAtSchema: Schema<BrokenAt> = s.of<BrokenAt>(s.union([s.int()]));
