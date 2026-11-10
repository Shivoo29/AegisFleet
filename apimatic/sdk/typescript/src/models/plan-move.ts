import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** PlanMove object */
export type PlanMove = {
  /** New time to run it (ISO 8601) */
  dueAt: Date;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const planMoveSchema: Schema<PlanMove> = s.object<PlanMove>(
  {
    dueAt: s.dateTime(),
    _keysMap: {
      dueAt: "due_at",
    },
  },
  { additionalProperties: s.json() },
);
