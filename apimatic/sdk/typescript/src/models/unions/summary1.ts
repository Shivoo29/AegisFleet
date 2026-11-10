import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** One-line summary */
export type Summary1 = string;

export const summary1Schema: Schema<Summary1> = s.of<Summary1>(s.union([s.string()]));
