import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { statusSchema, type Status } from "./status.js";
import { amountCentsSchema, type AmountCents } from "./unions/amount-cents.js";
import { currencySchema, type Currency } from "./unions/currency.js";
import { summary1Schema, type Summary1 } from "./unions/summary1.js";

/** Approval object */
export type Approval = {
  /** Unique id */
  id: string;
  /** Agent name: sentinel, defender, guardian or collector */
  agent: string;
  /** Gateway tool the agent called */
  tool: string;
  /** Tool arguments the agent asked the gateway to run */
  args: Record<string, unknown>;
  /** Why */
  reason: string;
  /** One-line summary */
  summary?: Summary1;
  /** Amount in minor units (cents) */
  amountCents?: AmountCents;
  /** ISO 4217 currency code */
  currency?: Currency;
  /** Current status */
  status: Status;
  /** When it was created (ISO 8601) */
  createdAt: Date;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const approvalSchema: Schema<Approval> = s.object<Approval>(
  {
    id: s.string(),
    agent: s.string(),
    tool: s.string(),
    args: s.record(s.string(), s.unknown()),
    reason: s.string(),
    summary: s.optional(s.lazy(() => summary1Schema)),
    amountCents: s.optional(s.lazy(() => amountCentsSchema)),
    currency: s.optional(s.lazy(() => currencySchema)),
    status: statusSchema,
    createdAt: s.dateTime(),
    _keysMap: {
      amountCents: "amount_cents",
      createdAt: "created_at",
    },
  },
  { additionalProperties: s.json() },
);
