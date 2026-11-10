import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { kindSchema, type Kind } from "./kind.js";

/** LedgerEntry object */
export type LedgerEntry = {
  /** Unique id */
  id: number;
  /** Entry kind: event, decision, agent_step, approval or note */
  kind: Kind;
  /** What this is about: an invoice, dispute or email id */
  subjectId: string;
  /** One-line summary */
  summary: string;
  /** Sealed data for this entry */
  payload: Record<string, unknown>;
  /** Hash of the previous entry; empty for the first */
  prevHash: string;
  /** SHA-256 of this entry plus the previous hash */
  hash: string;
  /** When it was created (ISO 8601) */
  createdAt: Date;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const ledgerEntrySchema: Schema<LedgerEntry> = s.object<LedgerEntry>(
  {
    id: s.int(),
    kind: kindSchema,
    subjectId: s.string(),
    summary: s.string(),
    payload: s.record(s.string(), s.unknown()),
    prevHash: s.string(),
    hash: s.string(),
    createdAt: s.dateTime(),
    _keysMap: {
      subjectId: "subject_id",
      prevHash: "prev_hash",
      createdAt: "created_at",
    },
  },
  { additionalProperties: s.json() },
);
