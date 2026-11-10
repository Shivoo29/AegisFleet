import * as s from "../core/validation/index.js";
import type { EnumSchema } from "../core/validation/schema.js";

/** approve or reject */
export const Action = {
  Approve: "approve",
  Reject: "reject",
} as const;
export type Action = (typeof Action)[keyof typeof Action] | (string & {});

export const actionSchema: EnumSchema<Action> = s.enumOf<Action>(Action);
