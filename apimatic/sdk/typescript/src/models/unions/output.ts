import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Agent's structured result */
export type Output = Record<string, unknown>;

export const outputSchema: Schema<Output> = s.of<Output>(s.union([s.record(s.string(), s.unknown())]));
