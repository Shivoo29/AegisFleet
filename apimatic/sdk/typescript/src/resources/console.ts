import type { AuthSchemes } from "../auth-schemes.js";
import { ApiError, type Declared, type Undeclared } from "../core/api-error.js";
import type { ApiPromise } from "../core/api-promise.js";
import type { RequestOptions } from "../core/api-request.js";
import { noneAuth } from "../core/auth/schemes.js";
import type { RawClient } from "../core/raw-client.js";
import type { ErrorDecoders } from "../core/response-decoder.js";
import { uuid } from "../core/uuid.js";
import * as s from "../core/validation/index.js";
import { actionSchema, type Action } from "../models/action.js";
import { agentRunSchema, type AgentRun } from "../models/agent-run.js";
import { approvalResultSchema, type ApprovalResult } from "../models/approval-result.js";
import { approvalSchema, type Approval } from "../models/approval.js";
import { chainVerifySchema, type ChainVerify } from "../models/chain-verify.js";
import { disputeDetailSchema, type DisputeDetail } from "../models/dispute-detail.js";
import { disputeSchema, type Dispute } from "../models/dispute.js";
import { healthSchema, type Health } from "../models/health.js";
import { httpValidationErrorSchema, type HttpValidationError } from "../models/http-validation-error.js";
import { inboxEmailSchema, type InboxEmail } from "../models/inbox-email.js";
import { inboxVerdictSchema, type InboxVerdict } from "../models/inbox-verdict.js";
import { invoiceSchema, type Invoice } from "../models/invoice.js";
import { killSwitchBodySchema, type KillSwitchBody } from "../models/kill-switch-body.js";
import { killSwitchSchema, type KillSwitch } from "../models/kill-switch.js";
import { ledgerEntrySchema, type LedgerEntry } from "../models/ledger-entry.js";
import { loginBodySchema, type LoginBody } from "../models/login-body.js";
import { meSchema, type Me } from "../models/me.js";
import { okSchema, type Ok } from "../models/ok.js";
import { planMoveSchema, type PlanMove } from "../models/plan-move.js";
import { planSchema, type Plan } from "../models/plan.js";
import { shipmentBodySchema, type ShipmentBody } from "../models/shipment-body.js";
import { shipmentResultSchema, type ShipmentResult } from "../models/shipment-result.js";
import { summarySchema, type Summary } from "../models/summary.js";
import { body1Schema, type Body1 } from "../models/unions/body1.js";
import { kind1Schema, type Kind1 } from "../models/unions/kind1.js";
import { subjectIdModelSchema, type SubjectIdModel } from "../models/unions/subject-id-model.js";
import type { Servers } from "../servers.js";

/**
 * Summary, Proof Ledger, approvals, agent runs, disputes, invoices, health.
 */
export class Console {
  readonly #rawClient: RawClient;
  readonly #servers: Servers;
  readonly #auth: AuthSchemes;

  constructor(rawClient: RawClient, servers: Servers, auth: AuthSchemes) {
    this.#rawClient = rawClient;
    this.#servers = servers;
    this.#auth = auth;
  }

  /**
   * Approvals
   *
   * @remarks
   * Agent actions the gateway held for a human decision (over the money cap).
   *
   * @returns OK
   *
   * @throws {@link Console.ApprovalsError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  approvals(
    request: Console.ApprovalsRequest = {},
    options?: RequestOptions,
  ): ApiPromise<Approval[], Console.ApprovalsError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/approvals"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [{ name: "status", value: request.status, schema: s.defaulted(s.string(), "pending") }],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.array(s.lazy(() => approvalSchema)) },
        errorFactory: Console.ApprovalsError,
      },
      options,
    );
  }

  /**
   * Decide Approval
   *
   * @remarks
   * Approve (the gateway then executes the held action) or reject it. Both are sealed.
   *
   * @returns OK
   *
   * @throws {@link Console.DecideApprovalError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  decideApproval(
    request: Console.DecideApprovalRequest,
    options?: RequestOptions,
  ): ApiPromise<ApprovalResult, Console.DecideApprovalError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/approvals/{approval_id}/{action}"),
        auth: this.#auth.httpBasic,
        pathParams: [
          { name: "approval_id", value: request.approvalId, schema: s.string() },
          { name: "action", value: request.action, schema: actionSchema },
        ],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: s.optional(s.lazy(() => body1Schema)) },
      },
      {
        success: { kind: "json", schema: approvalResultSchema },
        errorFactory: Console.DecideApprovalError,
      },
      options,
    );
  }

  /**
   * Dispute Detail
   *
   * @remarks
   * One dispute with Defender's evidence pack and the pending approval to submit it.
   *
   * @returns OK
   *
   * @throws {@link Console.DisputeDetailError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  disputeDetail(
    request: Console.DisputeDetailRequest,
    options?: RequestOptions,
  ): ApiPromise<DisputeDetail, Console.DisputeDetailError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/disputes/{dispute_id}"),
        auth: this.#auth.httpBasic,
        pathParams: [{ name: "dispute_id", value: request.disputeId, schema: s.string() }],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: disputeDetailSchema },
        errorFactory: Console.DisputeDetailError,
      },
      options,
    );
  }

  /**
   * Disputes
   *
   * @remarks
   * Latest state of every PayPal dispute, newest first.
   *
   * @returns OK
   *
   * @throws {@link Console.DisputesError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  disputes(options?: RequestOptions): ApiPromise<Dispute[], Console.DisputesError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/disputes"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.array(s.lazy(() => disputeSchema)) },
        errorFactory: Console.DisputesError,
      },
      options,
    );
  }

  /**
   * Get Killswitch
   *
   * @remarks
   * Is the kill switch on?
   *
   * @returns OK
   *
   * @throws {@link Console.GetKillswitchError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  getKillswitch(options?: RequestOptions): ApiPromise<KillSwitch, Console.GetKillswitchError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/killswitch"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: killSwitchSchema },
        errorFactory: Console.GetKillswitchError,
      },
      options,
    );
  }

  /**
   * Health
   *
   * @remarks
   * Score and factors are recomputed from the ledger on every call, so a dispute that arrived after
   * Guardian's last run still counts. Guardian's AI recommendations are reused only while the
   * factors they were written for still hold.
   *
   * @returns OK
   *
   * @throws {@link Console.HealthError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  health(options?: RequestOptions): ApiPromise<Health, Console.HealthError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/health"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: healthSchema },
        errorFactory: Console.HealthError,
      },
      options,
    );
  }

  /**
   * Inbox
   *
   * @remarks
   * Run Sentinel inline (a few seconds) so the console gets the verdict in one call.
   *
   * @returns OK
   *
   * @throws {@link Console.InboxError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  inbox(
    request: Console.InboxRequest,
    options?: RequestOptions,
  ): ApiPromise<InboxVerdict, Console.InboxError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/inbox"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: inboxEmailSchema },
      },
      {
        success: { kind: "json", schema: inboxVerdictSchema },
        errorFactory: Console.InboxError,
      },
      options,
    );
  }

  /**
   * Invoices
   *
   * @remarks
   * Invoices with paid/overdue status, risk, shipment and PayPal payment link.
   *
   * @returns OK
   *
   * @throws {@link Console.InvoicesError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  invoices(options?: RequestOptions): ApiPromise<Invoice[], Console.InvoicesError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/invoices"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.array(s.lazy(() => invoiceSchema)) },
        errorFactory: Console.InvoicesError,
      },
      options,
    );
  }

  /**
   * Ledger
   *
   * @remarks
   * Proof Ledger entries, newest first. Each entry's hash covers the previous one.
   *
   * @returns OK
   *
   * @throws {@link Console.LedgerError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  ledger(
    request: Console.LedgerRequest = {},
    options?: RequestOptions,
  ): ApiPromise<LedgerEntry[], Console.LedgerError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/ledger"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [
          { name: "kind", value: request.kind, schema: s.optional(s.lazy(() => kind1Schema)) },
          {
            name: "subject_id",
            value: request.subjectId,
            schema: s.optional(s.lazy(() => subjectIdModelSchema)),
          },
          { name: "limit", value: request.limit, schema: s.defaulted(s.int(), 100) },
        ],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.array(s.lazy(() => ledgerEntrySchema)) },
        errorFactory: Console.LedgerError,
      },
      options,
    );
  }

  /**
   * Ledger Verify
   *
   * @remarks
   * Recompute every hash in the chain and report the first entry that no longer matches.
   *
   * @returns OK
   *
   * @throws {@link Console.LedgerVerifyError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  ledgerVerify(options?: RequestOptions): ApiPromise<ChainVerify, Console.LedgerVerifyError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/ledger/verify"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: chainVerifySchema },
        errorFactory: Console.LedgerVerifyError,
      },
      options,
    );
  }

  /**
   * Login
   *
   * @remarks
   * Check a username and password and set a 12-hour session cookie.
   *
   * @returns OK
   *
   * @throws {@link Console.LoginError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  login(request: Console.LoginRequest, options?: RequestOptions): ApiPromise<Me, Console.LoginError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/login"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: loginBodySchema },
      },
      {
        success: { kind: "json", schema: meSchema },
        errorFactory: Console.LoginError,
      },
      options,
    );
  }

  /**
   * Logout
   *
   * @remarks
   * Clear the session cookie.
   *
   * @returns OK
   *
   * @throws {@link Console.LogoutError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  logout(options?: RequestOptions): ApiPromise<Ok, Console.LogoutError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/logout"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: okSchema },
        errorFactory: Console.LogoutError,
      },
      options,
    );
  }

  /**
   * Me
   *
   * @remarks
   * Who is logged in, and whether they are the seller (dev) or a read-mostly judge.
   *
   * @returns OK
   *
   * @throws {@link Console.MeError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  me(options?: RequestOptions): ApiPromise<Me, Console.MeError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/me"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: meSchema },
        errorFactory: Console.MeError,
      },
      options,
    );
  }

  /**
   * Plans Cancel
   *
   * @remarks
   * Seller cancels a planned action. Sealed in the ledger.
   *
   * @returns OK
   *
   * @throws {@link Console.PlansCancelError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  plansCancel(
    request: Console.PlansCancelRequest,
    options?: RequestOptions,
  ): ApiPromise<Ok, Console.PlansCancelError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/plans/{plan_id}/cancel"),
        auth: this.#auth.httpBasic,
        pathParams: [{ name: "plan_id", value: request.planId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: okSchema },
        errorFactory: Console.PlansCancelError,
      },
      options,
    );
  }

  /**
   * Plans List
   *
   * @remarks
   * What the agents have scheduled: planned, done, held, blocked and cancelled actions.
   *
   * @returns OK
   *
   * @throws {@link Console.PlansListError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  plansList(options?: RequestOptions): ApiPromise<Plan[], Console.PlansListError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/plans"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.array(s.lazy(() => planSchema)) },
        errorFactory: Console.PlansListError,
      },
      options,
    );
  }

  /**
   * Plans Move
   *
   * @remarks
   * Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.
   *
   * @returns OK
   *
   * @throws {@link Console.PlansMoveError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  plansMove(
    request: Console.PlansMoveRequest,
    options?: RequestOptions,
  ): ApiPromise<Plan, Console.PlansMoveError> {
    return this.#rawClient.execute(
      {
        method: "PATCH",
        urlTemplate: this.#servers.default("/api/plans/{plan_id}"),
        auth: this.#auth.httpBasic,
        pathParams: [{ name: "plan_id", value: request.planId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: planMoveSchema },
      },
      {
        success: { kind: "json", schema: planSchema },
        errorFactory: Console.PlansMoveError,
      },
      options,
    );
  }

  /**
   * Post Killswitch
   *
   * @remarks
   * Turn the kill switch on or off. While on, the gateway denies every agent action.
   *
   * @returns OK
   *
   * @throws {@link Console.PostKillswitchError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  postKillswitch(
    request: Console.PostKillswitchRequest,
    options?: RequestOptions,
  ): ApiPromise<KillSwitch, Console.PostKillswitchError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/killswitch"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: killSwitchBodySchema },
      },
      {
        success: { kind: "json", schema: killSwitchSchema },
        errorFactory: Console.PostKillswitchError,
      },
      options,
    );
  }

  /**
   * Runs
   *
   * @remarks
   * Recent agent runs with their steps and structured output.
   *
   * @returns OK
   *
   * @throws {@link Console.RunsError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  runs(
    request: Console.RunsRequest = {},
    options?: RequestOptions,
  ): ApiPromise<AgentRun[], Console.RunsError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/runs"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [{ name: "limit", value: request.limit, schema: s.defaulted(s.int(), 20) }],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.array(s.lazy(() => agentRunSchema)) },
        errorFactory: Console.RunsError,
      },
      options,
    );
  }

  /**
   * Shipments
   *
   * @remarks
   * Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).
   *
   * @returns OK
   *
   * @throws {@link Console.ShipmentsError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  shipments(
    request: Console.ShipmentsRequest,
    options?: RequestOptions,
  ): ApiPromise<ShipmentResult, Console.ShipmentsError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/shipments"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: shipmentBodySchema },
      },
      {
        success: { kind: "json", schema: shipmentResultSchema },
        errorFactory: Console.ShipmentsError,
      },
      options,
    );
  }

  /**
   * Summary
   *
   * @remarks
   * Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain
   * state.
   *
   * @returns OK
   *
   * @throws {@link Console.SummaryError} when the API answers with an error status — narrow on
   * `err.payload.kind`
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  summary(options?: RequestOptions): ApiPromise<Summary, Console.SummaryError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/summary"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: summarySchema },
        errorFactory: Console.SummaryError,
      },
      options,
    );
  }
}

export namespace Console {
  export type ApprovalsRequest = {
    /** Current status @default "pending" */
    status?: string;
  };

  export class ApprovalsError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<ApprovalsError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type DecideApprovalRequest = {
    /** Id of the pending approval for this action */
    approvalId: string;
    /** approve or reject */
    action: Action;
    body?: Body1;
  };

  export class DecideApprovalError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<DecideApprovalError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type DisputeDetailRequest = {
    /** PayPal dispute id, e.g. PP-D-12345 */
    disputeId: string;
  };

  export class DisputeDetailError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"error404", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<DisputeDetailError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 404, kind: "error404", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export class DisputesError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<DisputesError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export class GetKillswitchError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<GetKillswitchError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export class HealthError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<HealthError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export type InboxRequest = {
    body: InboxEmail;
  };

  export class InboxError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<InboxError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export class InvoicesError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<InvoicesError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export type LedgerRequest = {
    /** Entry kind: event, decision, agent_step, approval or note */
    kind?: Kind1;
    /** What this is about: an invoice, dispute or email id */
    subjectId?: SubjectIdModel;
    /** Maximum number of items to return @default 100 */
    limit?: number;
  };

  export class LedgerError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<LedgerError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export class LedgerVerifyError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<LedgerVerifyError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export type LoginRequest = {
    body: LoginBody;
  };

  export class LoginError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<LoginError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export class LogoutError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<LogoutError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export class MeError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<MeError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export type PlansCancelRequest = {
    /** plan_id */
    planId: string;
  };

  export class PlansCancelError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"error404", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<PlansCancelError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 404, kind: "error404", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export class PlansListError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<PlansListError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }

  export type PlansMoveRequest = {
    /** plan_id */
    planId: string;
    body: PlanMove;
  };

  export class PlansMoveError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"error404", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<PlansMoveError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 404, kind: "error404", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type PostKillswitchRequest = {
    body: KillSwitchBody;
  };

  export class PostKillswitchError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<PostKillswitchError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type RunsRequest = {
    /** Maximum number of items to return @default 20 */
    limit?: number;
  };

  export class RunsError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<RunsError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type ShipmentsRequest = {
    body: ShipmentBody;
  };

  export class ShipmentsError extends ApiError {
    declare readonly payload:
      | Declared<"error401", undefined>
      | Declared<"httpValidationError", HttpValidationError>
      | Undeclared;

    static readonly errors: ErrorDecoders<ShipmentsError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export class SummaryError extends ApiError {
    declare readonly payload: Declared<"error401", undefined> | Undeclared;

    static readonly errors: ErrorDecoders<SummaryError> = [
      { on: 401, kind: "error401", decode: { kind: "empty" } },
    ];
  }
}
