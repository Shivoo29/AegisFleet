import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { healthFactorSchema, type HealthFactor } from "./health-factor.js";
import { appealPackSchema, type AppealPack } from "./unions/appeal-pack.js";

/** Health object */
export type Health = {
  /** Health score, 0-100 */
  score: number;
  /** What the health score is made of */
  factors: HealthFactor[];
  /** Steps that would raise the score */
  recommendations: string[];
  /** Draft appeal text Guardian wrote for PayPal, if the account is limited */
  appealPack?: AppealPack;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const healthSchema: Schema<Health> = s.object<Health>(
  {
    score: s.int(),
    factors: s.array(s.lazy(() => healthFactorSchema)),
    recommendations: s.array(s.string()),
    appealPack: s.optional(s.lazy(() => appealPackSchema)),
    _keysMap: {
      appealPack: "appeal_pack",
    },
  },
  { additionalProperties: s.json() },
);
