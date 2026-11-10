import * as s from "../core/validation/index.js";
import type { EnumSchema } from "../core/validation/schema.js";

/** dev (seller) or judge */
export const Role = {
  Dev: "dev",
  Judge: "judge",
} as const;
export type Role = (typeof Role)[keyof typeof Role] | (string & {});

export const roleSchema: EnumSchema<Role> = s.enumOf<Role>(Role);
