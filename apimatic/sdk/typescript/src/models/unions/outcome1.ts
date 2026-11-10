import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** allow, hold or deny */
export type Outcome1 = Record<string, unknown>;

export const outcome1Schema: Schema<Outcome1> = s.of<Outcome1>(s.union([s.record(s.string(), s.unknown())]));
