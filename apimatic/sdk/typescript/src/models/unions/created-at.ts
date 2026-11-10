import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** When it was created (ISO 8601) */
export type CreatedAt = string;

export const createdAtSchema: Schema<CreatedAt> = s.of<CreatedAt>(s.union([s.string()]));
