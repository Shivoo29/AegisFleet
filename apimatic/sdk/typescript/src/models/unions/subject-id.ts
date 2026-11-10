import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** What this is about: an invoice, dispute or email id */
export type SubjectId = string;

export const subjectIdSchema: Schema<SubjectId> = s.of<SubjectId>(s.union([s.string()]));
