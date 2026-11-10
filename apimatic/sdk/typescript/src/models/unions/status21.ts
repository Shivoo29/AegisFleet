import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Current status */
export type Status21 = string;

export const status21Schema: Schema<Status21> = s.of<Status21>(s.union([s.string()]));
