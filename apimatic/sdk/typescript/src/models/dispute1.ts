import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { amountCentsSchema, type AmountCents } from "./unions/amount-cents.js";
import { buyerNameSchema, type BuyerName } from "./unions/buyer-name.js";
import { currencySchema, type Currency } from "./unions/currency.js";
import { dueBySchema, type DueBy } from "./unions/due-by.js";
import { invoiceIdSchema, type InvoiceId } from "./unions/invoice-id.js";

/** The dispute */
export type Dispute1 = {
  /** Unique id */
  id: string;
  /** Invoice id, e.g. INV-0007 */
  invoiceId?: InvoiceId;
  /** Why */
  reason: string;
  /** Current status */
  status: string;
  /** Amount in minor units (cents) */
  amountCents?: AmountCents;
  /** ISO 4217 currency code */
  currency?: Currency;
  /** Buyer's name as PayPal reports it */
  buyerName?: BuyerName;
  /** When it was created (ISO 8601) */
  createdAt: Date;
  /** Seller response deadline (ISO 8601) */
  dueBy?: DueBy;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const dispute1Schema: Schema<Dispute1> = s.object<Dispute1>(
  {
    id: s.string(),
    invoiceId: s.optional(s.lazy(() => invoiceIdSchema)),
    reason: s.string(),
    status: s.string(),
    amountCents: s.optional(s.lazy(() => amountCentsSchema)),
    currency: s.optional(s.lazy(() => currencySchema)),
    buyerName: s.optional(s.lazy(() => buyerNameSchema)),
    createdAt: s.dateTime(),
    dueBy: s.optional(s.lazy(() => dueBySchema)),
    _keysMap: {
      invoiceId: "invoice_id",
      amountCents: "amount_cents",
      buyerName: "buyer_name",
      createdAt: "created_at",
      dueBy: "due_by",
    },
  },
  { additionalProperties: s.json() },
);
