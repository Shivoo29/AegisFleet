import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** KillSwitch object */
export type KillSwitch = {
  /** True when the kill switch is on */
  on: boolean;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const killSwitchSchema: Schema<KillSwitch> = s.object<KillSwitch>(
  {
    on: s.boolean(),
  },
  { additionalProperties: s.json() },
);
