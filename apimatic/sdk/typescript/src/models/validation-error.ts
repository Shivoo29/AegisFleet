import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { locSchema, type Loc } from "./unions/loc.js";

/** ValidationError object */
export type ValidationError = {
  /** Where the invalid value is */
  loc: Loc[];
  /** Error message */
  msg: string;
  /** Error type */
  type: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const validationErrorSchema: Schema<ValidationError> = s.object<ValidationError>(
  {
    loc: s.array(s.lazy(() => locSchema)),
    msg: s.string(),
    type: s.string(),
  },
  { additionalProperties: s.json() },
);
