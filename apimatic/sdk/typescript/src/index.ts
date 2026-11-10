export { AegisFleetClient } from "./client.js";
export type { ClientOptions } from "./client-options.js";

export type { BasicAuthCredentials } from "./core/auth/credentials.js";

export { Console } from "./resources/console.js";
export { Demo } from "./resources/demo.js";
export { Ops } from "./resources/ops.js";
export { Webhooks } from "./resources/webhooks.js";

export { agentRunSchema, type AgentRun } from "./models/agent-run.js";
export { amountCentsSchema, type AmountCents } from "./models/unions/amount-cents.js";
export { appealPackSchema, type AppealPack } from "./models/unions/appeal-pack.js";
export { approvalSchema, type Approval } from "./models/approval.js";
export { approvalBodySchema, type ApprovalBody } from "./models/approval-body.js";
export { approvalIdSchema, type ApprovalId } from "./models/unions/approval-id.js";
export { approvalResultSchema, type ApprovalResult } from "./models/approval-result.js";
export { bodySchema, type Body } from "./models/unions/body.js";
export { body1Schema, type Body1 } from "./models/unions/body1.js";
export { brokenAtSchema, type BrokenAt } from "./models/unions/broken-at.js";
export { buyerEmailSchema, type BuyerEmail } from "./models/unions/buyer-email.js";
export { buyerNameSchema, type BuyerName } from "./models/unions/buyer-name.js";
export { chainVerifySchema, type ChainVerify } from "./models/chain-verify.js";
export { createdAtSchema, type CreatedAt } from "./models/unions/created-at.js";
export { currencySchema, type Currency } from "./models/unions/currency.js";
export { decisionSchema, type Decision } from "./models/decision.js";
export { decision1Schema, type Decision1 } from "./models/unions/decision1.js";
export { decision2Schema, type Decision2 } from "./models/decision2.js";
export { demoResultSchema, type DemoResult } from "./models/demo-result.js";
export { disputeSchema, type Dispute } from "./models/dispute.js";
export { dispute1Schema, type Dispute1 } from "./models/dispute1.js";
export { disputeDetailSchema, type DisputeDetail } from "./models/dispute-detail.js";
export { dueBySchema, type DueBy } from "./models/unions/due-by.js";
export { evidencePackSchema, type EvidencePack } from "./models/unions/evidence-pack.js";
export { fromSchema, type From } from "./models/unions/from.js";
export { httpValidationErrorSchema, type HttpValidationError } from "./models/http-validation-error.js";
export {
  httpValidationErrorErrorSchema,
  type HttpValidationErrorError,
} from "./models/http-validation-error-error.js";
export { healthSchema, type Health } from "./models/health.js";
export { healthFactorSchema, type HealthFactor } from "./models/health-factor.js";
export { inboxEmailSchema, type InboxEmail } from "./models/inbox-email.js";
export { inboxVerdictSchema, type InboxVerdict } from "./models/inbox-verdict.js";
export { invoiceSchema, type Invoice } from "./models/invoice.js";
export { invoiceIdSchema, type InvoiceId } from "./models/unions/invoice-id.js";
export { killSwitchSchema, type KillSwitch } from "./models/kill-switch.js";
export { killSwitchBodySchema, type KillSwitchBody } from "./models/kill-switch-body.js";
export { Kind, kindSchema } from "./models/kind.js";
export { ledgerEntrySchema, type LedgerEntry } from "./models/ledger-entry.js";
export { locSchema, type Loc } from "./models/unions/loc.js";
export { loginBodySchema, type LoginBody } from "./models/login-body.js";
export { meSchema, type Me } from "./models/me.js";
export { okSchema, type Ok } from "./models/ok.js";
export { Outcome, outcomeSchema } from "./models/outcome.js";
export { outcome1Schema, type Outcome1 } from "./models/unions/outcome1.js";
export { outputSchema, type Output } from "./models/unions/output.js";
export { paidAtSchema, type PaidAt } from "./models/unions/paid-at.js";
export { payUrlSchema, type PayUrl } from "./models/unions/pay-url.js";
export { planSchema, type Plan } from "./models/plan.js";
export { planMoveSchema, type PlanMove } from "./models/plan-move.js";
export { resultSchema, type Result } from "./models/unions/result.js";
export { Risk, riskSchema } from "./models/risk.js";
export { Role, roleSchema } from "./models/role.js";
export { runIdSchema, type RunId } from "./models/unions/run-id.js";
export { shipmentBodySchema, type ShipmentBody } from "./models/shipment-body.js";
export { shipmentResultSchema, type ShipmentResult } from "./models/shipment-result.js";
export { Status, statusSchema } from "./models/status.js";
export { Status1, status1Schema } from "./models/status1.js";
export { Status2, status2Schema } from "./models/status2.js";
export { status21Schema, type Status21 } from "./models/unions/status21.js";
export { Status3, status3Schema } from "./models/status3.js";
export { subjectSchema, type Subject } from "./models/unions/subject.js";
export { subjectIdSchema, type SubjectId } from "./models/unions/subject-id.js";
export { summarySchema, type Summary } from "./models/summary.js";
export { summary1Schema, type Summary1 } from "./models/unions/summary1.js";
export { trackingNumberSchema, type TrackingNumber } from "./models/unions/tracking-number.js";
export { validationErrorSchema, type ValidationError } from "./models/validation-error.js";
export { verdictSchema, type Verdict } from "./models/unions/verdict.js";
export { Action, actionSchema } from "./models/action.js";
export { kind1Schema, type Kind1 } from "./models/unions/kind1.js";
export { subjectIdModelSchema, type SubjectIdModel } from "./models/unions/subject-id-model.js";

export {
  CoreError as AegisFleetError,
  ResponseError,
  DecodeError,
  EncodeError,
  ConnectionError,
  TimeoutError,
  AuthError,
  PaginationError,
  ConfigurationError,
} from "./core/errors.js";
export { ApiError } from "./core/api-error.js";
export { SchemaError } from "./core/validation/schema-error.js";
export {
  defaultLoggingOptions,
  type LoggingOptions,
  type RequestLoggingOptions,
  type Logger,
  type LogDetails,
  type HttpRequestDetails,
  type RequestHeadersDetails,
  type RequestBodyDetails,
  type HttpResponseDetails,
  type ResponseHeadersDetails,
  type HttpRetryingDetails,
  type HttpFailedDetails,
  type LogLevel,
} from "./core/logging.js";
export type { ApiPromise, ApiResult } from "./core/api-promise.js";
export type { Pageable, PageableApiResult } from "./core/pagination/pageable.js";
export type { HttpMethod, RequestOptions } from "./core/api-request.js";
export type { RetryOptions, RequestRetryOptions, RetryAttempt, RetryReason } from "./core/retry.js";
export type { BinaryContent, BinaryData, BinaryErrorContent, FileData, FileInput } from "./core/binary.js";
export type { ErrorKind } from "./core/errors.js";
export type { Declared, Undeclared } from "./core/api-error.js";
export type { Schema, EnumSchema, Encoded, ValidationResult, JsonValue } from "./core/validation/schema.js";
