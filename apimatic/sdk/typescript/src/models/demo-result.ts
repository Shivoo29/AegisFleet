import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** DemoResult object */
export type DemoResult = {
  /** True on success */
  ok: boolean;
  /** What happened, in plain words, for the console toast */
  message: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const demoResultSchema: Schema<DemoResult> = s.object<DemoResult>(
  {
    ok: s.boolean(),
    message: s.string(),
  },
  { additionalProperties: s.json() },
);
