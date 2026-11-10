import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** LoginBody object */
export type LoginBody = {
  /** dev or judge */
  username?: string;
  /** Console password */
  password?: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const loginBodySchema: Schema<LoginBody> = s.object<LoginBody>(
  {
    username: s.optional(s.string()),
    password: s.optional(s.string()),
  },
  { additionalProperties: s.json() },
);
