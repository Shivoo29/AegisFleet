import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Invoice id, e.g. INV-0007 */
export type InvoiceId = string;

export const invoiceIdSchema: Schema<InvoiceId> = s.of<InvoiceId>(s.union([s.string()]));
