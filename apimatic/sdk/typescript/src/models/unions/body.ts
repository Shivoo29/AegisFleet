import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Email body text */
export type Body = string;

export const bodySchema: Schema<Body> = s.of<Body>(s.union([s.string()]));
