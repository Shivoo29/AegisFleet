import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";
import { approvalBodySchema, type ApprovalBody } from "../approval-body.js";

export type Body1 = ApprovalBody;

export const body1Schema: Schema<Body1> = s.of<Body1>(s.union([s.lazy(() => approvalBodySchema)]));
