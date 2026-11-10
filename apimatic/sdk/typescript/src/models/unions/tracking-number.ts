import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

/** Carrier tracking number */
export type TrackingNumber = string;

export const trackingNumberSchema: Schema<TrackingNumber> = s.of<TrackingNumber>(s.union([s.string()]));
