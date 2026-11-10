import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Draft appeal text Guardian wrote for PayPal, if the account is limited */
export type AppealPack = string;

export const appealPackSchema: Schema<AppealPack> = s.of<AppealPack>(s.union([s.string()]));
