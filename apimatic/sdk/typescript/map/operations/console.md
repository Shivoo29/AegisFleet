<!-- Generated file — do not edit; regenerated with the SDK. -->

# Console — operations

Accessor: `client.console` · Source: `src/resources/console.ts` · 21 operations · Request and error types: namespace `Console`

**Type sources**: every type an operation names, with the file that declares it and the schema value exported beside it. Import every name from `aegis-fleet`; the `Source` path is where to **read** the shape, never what to import. `ApiError`, the runtime error family and the file vocabulary are excluded — see sdk-map.md.

### approvals

- **Signature**: `approvals(request?: Console.ApprovalsRequest, options?: RequestOptions): ApiPromise<Approval[], Console.ApprovalsError>`
- **Wire**: `GET /api/approvals`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Approval[]` — a bare `application/json` array; the success type *is* the array, not a wrapper model
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.ApprovalsError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.ApprovalsRequest` (1):

| Field | Channel | Type | Req | Default |
| --- | --- | --- | --- | --- |
| `status` | `query` | `string` | no | `"pending"` |

| Type | Schema value | Source |
| --- | --- | --- |
| `Approval` | `approvalSchema` | `src/models/approval.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### decideApproval

- **Signature**: `decideApproval(request: Console.DecideApprovalRequest, options?: RequestOptions): ApiPromise<ApprovalResult, Console.DecideApprovalError>`
- **Wire**: `POST /api/approvals/{approval_id}/{action}`
- **Auth**: `httpBasic`
- **Request body**: `application/json` — the `body` field. **Optional**: omit it and the request carries no body and no `Content-Type` header at all
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `ApprovalResult`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.DecideApprovalError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.DecideApprovalRequest` (3):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `approvalId` | `path` | `approval_id` | `string` | yes |
| `action` | `path` | — | `Action` | yes |
| `body` | `body` | — | `Body1` | no |

| Type | Schema value | Source |
| --- | --- | --- |
| `Action` | `actionSchema` | `src/models/action.ts` |
| `Body1` | `body1Schema` | `src/models/unions/body1.ts` |
| `ApprovalResult` | `approvalResultSchema` | `src/models/approval-result.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### disputeDetail

- **Signature**: `disputeDetail(request: Console.DisputeDetailRequest, options?: RequestOptions): ApiPromise<DisputeDetail, Console.DisputeDetailError>`
- **Wire**: `GET /api/disputes/{dispute_id}`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `DisputeDetail`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.DisputeDetailError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"error404"` [404] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.DisputeDetailRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `disputeId` | `path` | `dispute_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `DisputeDetail` | `disputeDetailSchema` | `src/models/dispute-detail.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### disputes

- **Signature**: `disputes(options?: RequestOptions): ApiPromise<Dispute[], Console.DisputesError>`
- **Wire**: `GET /api/disputes`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Dispute[]` — a bare `application/json` array; the success type *is* the array, not a wrapper model
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.DisputesError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `Dispute` | `disputeSchema` | `src/models/dispute.ts` |

### getKillswitch

- **Signature**: `getKillswitch(options?: RequestOptions): ApiPromise<KillSwitch, Console.GetKillswitchError>`
- **Wire**: `GET /api/killswitch`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `KillSwitch`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.GetKillswitchError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `KillSwitch` | `killSwitchSchema` | `src/models/kill-switch.ts` |

### health

- **Signature**: `health(options?: RequestOptions): ApiPromise<Health, Console.HealthError>`
- **Wire**: `GET /api/health`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Health`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.HealthError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `Health` | `healthSchema` | `src/models/health.ts` |

### inbox

- **Signature**: `inbox(request: Console.InboxRequest, options?: RequestOptions): ApiPromise<InboxVerdict, Console.InboxError>`
- **Wire**: `POST /api/inbox`
- **Auth**: `httpBasic`
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `InboxVerdict`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.InboxError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.InboxRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `body` | `body` | `InboxEmail` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `InboxEmail` | `inboxEmailSchema` | `src/models/inbox-email.ts` |
| `InboxVerdict` | `inboxVerdictSchema` | `src/models/inbox-verdict.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### invoices

- **Signature**: `invoices(options?: RequestOptions): ApiPromise<Invoice[], Console.InvoicesError>`
- **Wire**: `GET /api/invoices`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Invoice[]` — a bare `application/json` array; the success type *is* the array, not a wrapper model
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.InvoicesError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `Invoice` | `invoiceSchema` | `src/models/invoice.ts` |

### ledger

- **Signature**: `ledger(request?: Console.LedgerRequest, options?: RequestOptions): ApiPromise<LedgerEntry[], Console.LedgerError>`
- **Wire**: `GET /api/ledger`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `LedgerEntry[]` — a bare `application/json` array; the success type *is* the array, not a wrapper model
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.LedgerError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.LedgerRequest` (3):

| Field | Channel | Wire | Type | Req | Default |
| --- | --- | --- | --- | --- | --- |
| `kind` | `query` | — | `Kind1` | no | — |
| `subjectId` | `query` | `subject_id` | `SubjectIdModel` | no | — |
| `limit` | `query` | — | `number` | no | `100` |

| Type | Schema value | Source |
| --- | --- | --- |
| `Kind1` | `kind1Schema` | `src/models/unions/kind1.ts` |
| `SubjectIdModel` | `subjectIdModelSchema` | `src/models/unions/subject-id-model.ts` |
| `LedgerEntry` | `ledgerEntrySchema` | `src/models/ledger-entry.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### ledgerVerify

- **Signature**: `ledgerVerify(options?: RequestOptions): ApiPromise<ChainVerify, Console.LedgerVerifyError>`
- **Wire**: `GET /api/ledger/verify`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `ChainVerify`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.LedgerVerifyError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `ChainVerify` | `chainVerifySchema` | `src/models/chain-verify.ts` |

### login

- **Signature**: `login(request: Console.LoginRequest, options?: RequestOptions): ApiPromise<Me, Console.LoginError>`
- **Wire**: `POST /api/login`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Me`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.LoginError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.LoginRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `body` | `body` | `LoginBody` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `LoginBody` | `loginBodySchema` | `src/models/login-body.ts` |
| `Me` | `meSchema` | `src/models/me.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### logout

- **Signature**: `logout(options?: RequestOptions): ApiPromise<Ok, Console.LogoutError>`
- **Wire**: `POST /api/logout`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Ok`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.LogoutError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `Ok` | `okSchema` | `src/models/ok.ts` |

### mcpLink

- **Signature**: `mcpLink(options?: RequestOptions): ApiPromise<Record<string, unknown>, Console.McpLinkError>`
- **Wire**: `GET /api/mcp/link`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.McpLinkError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

### me

- **Signature**: `me(options?: RequestOptions): ApiPromise<Me, Console.MeError>`
- **Wire**: `GET /api/me`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Me`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.MeError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `Me` | `meSchema` | `src/models/me.ts` |

### plansCancel

- **Signature**: `plansCancel(request: Console.PlansCancelRequest, options?: RequestOptions): ApiPromise<Ok, Console.PlansCancelError>`
- **Wire**: `POST /api/plans/{plan_id}/cancel`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Ok`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.PlansCancelError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"error404"` [404] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.PlansCancelRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `planId` | `path` | `plan_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `Ok` | `okSchema` | `src/models/ok.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### plansList

- **Signature**: `plansList(options?: RequestOptions): ApiPromise<Plan[], Console.PlansListError>`
- **Wire**: `GET /api/plans`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Plan[]` — a bare `application/json` array; the success type *is* the array, not a wrapper model
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.PlansListError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `Plan` | `planSchema` | `src/models/plan.ts` |

### plansMove

- **Signature**: `plansMove(request: Console.PlansMoveRequest, options?: RequestOptions): ApiPromise<Plan, Console.PlansMoveError>`
- **Wire**: `PATCH /api/plans/{plan_id}`
- **Auth**: `httpBasic`
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Plan`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.PlansMoveError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"error404"` [404] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.PlansMoveRequest` (2):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `planId` | `path` | `plan_id` | `string` | yes |
| `body` | `body` | — | `PlanMove` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `PlanMove` | `planMoveSchema` | `src/models/plan-move.ts` |
| `Plan` | `planSchema` | `src/models/plan.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### postKillswitch

- **Signature**: `postKillswitch(request: Console.PostKillswitchRequest, options?: RequestOptions): ApiPromise<KillSwitch, Console.PostKillswitchError>`
- **Wire**: `POST /api/killswitch`
- **Auth**: `httpBasic`
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `KillSwitch`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.PostKillswitchError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.PostKillswitchRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `body` | `body` | `KillSwitchBody` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `KillSwitchBody` | `killSwitchBodySchema` | `src/models/kill-switch-body.ts` |
| `KillSwitch` | `killSwitchSchema` | `src/models/kill-switch.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### runs

- **Signature**: `runs(request?: Console.RunsRequest, options?: RequestOptions): ApiPromise<AgentRun[], Console.RunsError>`
- **Wire**: `GET /api/runs`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `AgentRun[]` — a bare `application/json` array; the success type *is* the array, not a wrapper model
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.RunsError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.RunsRequest` (1):

| Field | Channel | Type | Req | Default |
| --- | --- | --- | --- | --- |
| `limit` | `query` | `number` | no | `20` |

| Type | Schema value | Source |
| --- | --- | --- |
| `AgentRun` | `agentRunSchema` | `src/models/agent-run.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### shipments

- **Signature**: `shipments(request: Console.ShipmentsRequest, options?: RequestOptions): ApiPromise<ShipmentResult, Console.ShipmentsError>`
- **Wire**: `POST /api/shipments`
- **Auth**: `httpBasic`
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `ShipmentResult`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.ShipmentsError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `Console.ShipmentsRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `body` | `body` | `ShipmentBody` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `ShipmentBody` | `shipmentBodySchema` | `src/models/shipment-body.ts` |
| `ShipmentResult` | `shipmentResultSchema` | `src/models/shipment-result.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### summary

- **Signature**: `summary(options?: RequestOptions): ApiPromise<Summary, Console.SummaryError>`
- **Wire**: `GET /api/summary`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Summary`
- **Error**: `AegisFleetError` with `kind: "api"`, an instance of `Console.SummaryError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"error401"` [401] no body · `"undeclared"` [any other] `rawBody: ArrayBuffer`

| Type | Schema value | Source |
| --- | --- | --- |
| `Summary` | `summarySchema` | `src/models/summary.ts` |

