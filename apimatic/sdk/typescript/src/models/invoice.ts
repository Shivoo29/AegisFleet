import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { riskSchema, type Risk } from "./risk.js";
import { status2Schema, type Status2 } from "./status2.js";
import { amountCentsSchema, type AmountCents } from "./unions/amount-cents.js";
import { buyerEmailSchema, type BuyerEmail } from "./unions/buyer-email.js";
import { createdAtSchema, type CreatedAt } from "./unions/created-at.js";
import { paidAtSchema, type PaidAt } from "./unions/paid-at.js";
import { payUrlSchema, type PayUrl } from "./unions/pay-url.js";
import { trackingNumberSchema, type TrackingNumber } from "./unions/tracking-number.js";

/** Invoice object */
export type Invoice = {
  /** Unique id */
  id: string;
  /** Buyer's email address */
  buyerEmail?: BuyerEmail;
  /** Amount in minor units (cents) */
  amountCents?: AmountCents;
  /** ISO 4217 currency code */
  currency: string;
  /** Current status */
  status: Status2;
  /** Days past the due date; 0 when paid or not yet due */
  daysOverdue: number;
  /** Payment risk: low, medium or high */
  risk: Risk;
  /** True when tracking was added */
  shipped: boolean;
  /** Carrier tracking number */
  trackingNumber?: TrackingNumber;
  /** When it was created (ISO 8601) */
  createdAt?: CreatedAt;
  /** When payment was verified (ISO 8601) */
  paidAt?: PaidAt;
  /** PayPal payment page for this invoice */
  payUrl?: PayUrl;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const invoiceSchema: Schema<Invoice> = s.object<Invoice>(
  {
    id: s.string(),
    buyerEmail: s.optional(s.lazy(() => buyerEmailSchema)),
    amountCents: s.optional(s.lazy(() => amountCentsSchema)),
    currency: s.string(),
    status: status2Schema,
    daysOverdue: s.int(),
    risk: riskSchema,
    shipped: s.boolean(),
    trackingNumber: s.optional(s.lazy(() => trackingNumberSchema)),
    createdAt: s.optional(s.lazy(() => createdAtSchema)),
    paidAt: s.optional(s.lazy(() => paidAtSchema)),
    payUrl: s.optional(s.lazy(() => payUrlSchema)),
    _keysMap: {
      buyerEmail: "buyer_email",
      amountCents: "amount_cents",
      daysOverdue: "days_overdue",
      trackingNumber: "tracking_number",
      createdAt: "created_at",
      paidAt: "paid_at",
      payUrl: "pay_url",
    },
  },
  { additionalProperties: s.json() },
);
