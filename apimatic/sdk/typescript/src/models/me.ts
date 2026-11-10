import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { roleSchema, type Role } from "./role.js";

/** Me object */
export type Me = {
  /** Logged-in user name */
  user: string;
  /** dev (seller) or judge */
  role: Role;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const meSchema: Schema<Me> = s.object<Me>(
  {
    user: s.string(),
    role: roleSchema,
  },
  { additionalProperties: s.json() },
);
