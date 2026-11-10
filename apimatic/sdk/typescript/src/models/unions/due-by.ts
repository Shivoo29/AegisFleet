import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Seller response deadline (ISO 8601) */
export type DueBy = string;

export const dueBySchema: Schema<DueBy> = s.of<DueBy>(s.union([s.string()]));
