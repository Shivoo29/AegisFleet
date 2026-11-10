import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** KillSwitchBody object */
export type KillSwitchBody = {
  /** true stops every agent action at the gateway @default false */
  on?: boolean;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const killSwitchBodySchema: Schema<KillSwitchBody> = s.object<KillSwitchBody>(
  {
    on: s.defaulted(s.boolean(), false),
  },
  { additionalProperties: s.json() },
);
