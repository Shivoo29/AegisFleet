import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { invoiceIdSchema, type InvoiceId } from "./unions/invoice-id.js";
import { trackingNumberSchema, type TrackingNumber } from "./unions/tracking-number.js";

/** ShipmentBody object */
export type ShipmentBody = {
  /** Invoice id, e.g. INV-0007 */
  invoiceId?: InvoiceId;
  /** Carrier tracking number */
  trackingNumber?: TrackingNumber;
  /** Shipping carrier, e.g. UPS @default "OTHER" */
  carrier?: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const shipmentBodySchema: Schema<ShipmentBody> = s.object<ShipmentBody>(
  {
    invoiceId: s.optional(s.lazy(() => invoiceIdSchema)),
    trackingNumber: s.optional(s.lazy(() => trackingNumberSchema)),
    carrier: s.defaulted(s.string(), "OTHER"),
    _keysMap: {
      invoiceId: "invoice_id",
      trackingNumber: "tracking_number",
    },
  },
  { additionalProperties: s.json() },
);
