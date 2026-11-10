import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { brokenAtSchema, type BrokenAt } from "./unions/broken-at.js";

/** ChainVerify object */
export type ChainVerify = {
  /** True on success */
  ok: boolean;
  /** Number of ledger entries checked */
  checked: number;
  /** First ledger id whose hash no longer matches */
  brokenAt?: BrokenAt;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const chainVerifySchema: Schema<ChainVerify> = s.object<ChainVerify>(
  {
    ok: s.boolean(),
    checked: s.int(),
    brokenAt: s.optional(s.lazy(() => brokenAtSchema)),
    _keysMap: {
      brokenAt: "broken_at",
    },
  },
  { additionalProperties: s.json() },
);
