import * as s from "../core/validation/index.js";
import type { EnumSchema } from "../core/validation/schema.js";

/** allow, hold or deny */
export const Outcome = {
  Allow: "allow",
  Hold: "hold",
  Deny: "deny",
} as const;
export type Outcome = (typeof Outcome)[keyof typeof Outcome] | (string & {});

export const outcomeSchema: EnumSchema<Outcome> = s.enumOf<Outcome>(Outcome);
