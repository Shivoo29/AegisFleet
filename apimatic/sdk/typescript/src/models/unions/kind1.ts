import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Entry kind: event, decision, agent_step, approval or note */
export type Kind1 = string;

export const kind1Schema: Schema<Kind1> = s.of<Kind1>(s.union([s.string()]));
