import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Defender's evidence pack, every fact citing a ledger id */
export type EvidencePack = Record<string, unknown>;

export const evidencePackSchema: Schema<EvidencePack> = s.of<EvidencePack>(
  s.union([s.record(s.string(), s.unknown())]),
);
