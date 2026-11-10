import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Sentinel verdict: scam | legit | unsure, with red flags */
export type Verdict = Record<string, unknown>;

export const verdictSchema: Schema<Verdict> = s.of<Verdict>(s.union([s.record(s.string(), s.unknown())]));
