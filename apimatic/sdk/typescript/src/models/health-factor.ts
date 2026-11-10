import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** HealthFactor object */
export type HealthFactor = {
  /** Factor name */
  name: string;
  /** Measured value */
  value: Record<string, unknown>;
  /** How this factor moves the score */
  impact: string;
  /** Free-text note */
  note: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const healthFactorSchema: Schema<HealthFactor> = s.object<HealthFactor>(
  {
    name: s.string(),
    value: s.record(s.string(), s.unknown()),
    impact: s.string(),
    note: s.string(),
  },
  { additionalProperties: s.json() },
);
