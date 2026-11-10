import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** What this is about: an invoice, dispute or email id */
export type SubjectIdModel = string;

export const subjectIdModelSchema: Schema<SubjectIdModel> = s.of<SubjectIdModel>(s.union([s.string()]));
