import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** ISO 4217 currency code */
export type Currency = string;

export const currencySchema: Schema<Currency> = s.of<Currency>(s.union([s.string()]));
