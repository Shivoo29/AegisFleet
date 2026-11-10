import type { AuthSchemes } from "../auth-schemes.js";
import { ApiError } from "../core/api-error.js";
import type { ApiPromise } from "../core/api-promise.js";
import type { RequestOptions } from "../core/api-request.js";
import type { RawClient } from "../core/raw-client.js";
import { uuid } from "../core/uuid.js";
import * as s from "../core/validation/index.js";
import { demoResultSchema, type DemoResult } from "../models/demo-result.js";
import type { Servers } from "../servers.js";

/**
 * One-click story beats for judges (demo mode only).
 */
export class Demo {
  readonly #rawClient: RawClient;
  readonly #servers: Servers;
  readonly #auth: AuthSchemes;

  constructor(rawClient: RawClient, servers: Servers, auth: AuthSchemes) {
    this.#rawClient = rawClient;
    this.#servers = servers;
    this.#auth = auth;
  }

  /**
   * Delivered
   *
   * @remarks
   * Courier says the parcel arrived -> Guardian updates tracking.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  delivered(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/delivered"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Demo Status
   *
   * @remarks
   * 200 when demo mode is on (404 otherwise).
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  demoStatus(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/demo/status"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Overdue
   *
   * @remarks
   * INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  overdue(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/overdue"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Replay Injection
   *
   * @remarks
   * An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  replayInjection(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/replay_injection"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Reset
   *
   * @remarks
   * Wipe everything, then replay Riya's story so the console never starts empty.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  reset(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/reset"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Sandbox Invoice
   *
   * @remarks
   * Create a real invoice in the PayPal sandbox. Paying it fires a real, signed webhook.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  sandboxInvoice(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/sandbox_invoice"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Sandbox Record Payment
   *
   * @remarks
   * Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.
   *
   * PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  sandboxRecordPayment(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/sandbox_record_payment"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Scam Email
   *
   * @remarks
   * Fake 'payment received' email: no verified payment in the ledger -> Sentinel says scam.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  scamEmail(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/scam_email"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Tamper
   *
   * @remarks
   * Edit one sealed entry behind the ledger's back -> verify() points at it.
   *
   * @returns OK
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link AegisFleetError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  tamper(options?: RequestOptions): ApiPromise<DemoResult, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/tamper"),
        auth: this.#auth.httpBasic,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: demoResultSchema },
        errorFactory: ApiError,
      },
      options,
    );
  }
}
