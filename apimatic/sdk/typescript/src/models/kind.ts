import * as s from "../core/validation/index.js";
import type { EnumSchema } from "../core/validation/schema.js";

/** Entry kind: event, decision, agent_step, approval or note */
export const Kind = {
  Event: "event",
  Decision: "decision",
  AgentStep: "agent_step",
  Approval: "approval",
  Note: "note",
} as const;
export type Kind = (typeof Kind)[keyof typeof Kind] | (string & {});

export const kindSchema: EnumSchema<Kind> = s.enumOf<Kind>(Kind);
