import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { bodySchema, type Body } from "./unions/body.js";
import { fromSchema, type From } from "./unions/from.js";
import { invoiceIdSchema, type InvoiceId } from "./unions/invoice-id.js";
import { subjectIdSchema, type SubjectId } from "./unions/subject-id.js";
import { subjectSchema, type Subject } from "./unions/subject.js";

/** InboxEmail object */
export type InboxEmail = {
  /** What this is about: an invoice, dispute or email id */
  subjectId?: SubjectId;
  /** Invoice id, e.g. INV-0007 */
  invoiceId?: InvoiceId;
  /** Sender address */
  from?: From;
  /** Email subject */
  subject?: Subject;
  /** Email body text */
  body?: Body;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const inboxEmailSchema: Schema<InboxEmail> = s.object<InboxEmail>(
  {
    subjectId: s.optional(s.lazy(() => subjectIdSchema)),
    invoiceId: s.optional(s.lazy(() => invoiceIdSchema)),
    from: s.optional(s.lazy(() => fromSchema)),
    subject: s.optional(s.lazy(() => subjectSchema)),
    body: s.optional(s.lazy(() => bodySchema)),
    _keysMap: {
      subjectId: "subject_id",
      invoiceId: "invoice_id",
    },
  },
  { additionalProperties: s.json() },
);
