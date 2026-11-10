import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";
import { decision2Schema, type Decision2 } from "../decision2.js";

/** Gateway decision for the executed action */
export type Decision1 = Decision2;

export const decision1Schema: Schema<Decision1> = s.of<Decision1>(s.union([s.lazy(() => decision2Schema)]));
