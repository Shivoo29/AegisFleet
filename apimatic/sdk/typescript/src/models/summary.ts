import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

/** Summary object */
export type Summary = {
  /** Total held for approval, in cents */
  moneyAtRiskCents: number;
  /** ISO 4217 currency code */
  currency: string;
  /** Actions waiting for a human */
  pendingApprovals: number;
  /** Number of open disputes */
  openDisputes: number;
  /** Number of overdue invoice events */
  overdueInvoices: number;
  /** Account health score, 0-100 */
  healthScore: number;
  /** True when the kill switch blocks all agent actions */
  killSwitch: boolean;
  /** True when every ledger hash still matches */
  chainOk: boolean;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const summarySchema: Schema<Summary> = s.object<Summary>(
  {
    moneyAtRiskCents: s.int(),
    currency: s.string(),
    pendingApprovals: s.int(),
    openDisputes: s.int(),
    overdueInvoices: s.int(),
    healthScore: s.int(),
    killSwitch: s.boolean(),
    chainOk: s.boolean(),
    _keysMap: {
      moneyAtRiskCents: "money_at_risk_cents",
      pendingApprovals: "pending_approvals",
      openDisputes: "open_disputes",
      overdueInvoices: "overdue_invoices",
      healthScore: "health_score",
      killSwitch: "kill_switch",
      chainOk: "chain_ok",
    },
  },
  { additionalProperties: s.json() },
);
