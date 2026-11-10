<!-- Generated file — do not edit; regenerated with the SDK. -->

# Console — operations

Accessor: `client.console` · Source: `aegis_fleet/apis/console.py` · 21 operations

Each `###` block is one operation and assumes `sdk-map.md` is loaded: blocks omit what its invariants table covers and are otherwise self-contained, so chunk at block level. Signatures are the sync parsed spelling; the async and raw spellings take the same parameters (see sdk-map.md). **Type sources** names the module declaring each type an operation mentions, so resolving a body, return or error payload is a lookup rather than a search; the runtime types `RawError` and `ApiResult` are excluded.

### client.console.approvals

- **Route**: `GET /api/approvals`
- **Auth**: `http_basic`
- **Signature**: `def approvals(*, status: str | None = "pending", request_options: RequestOptionsOrDict | None = None)`
- **Params**: `status` — query
- **Returns (parsed)**: `list[Approval]`
- **Returns (raw)**: `ApiResult[list[Approval], ApprovalsErrorBody]`
- **Error**: `ApprovalsErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Approval` | `aegis_fleet/models/approval.py` |
| `ApprovalsErrorBody` | `aegis_fleet/errors/approvals_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.decide_approval

- **Route**: `POST /api/approvals/{approval_id}/{action}`
- **Auth**: `http_basic`
- **Signature**: `def decide_approval(approval_id: str, action: ActionOrStr, *, body: ApprovalBody | ApprovalBodyDict | None = None, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `approval_id`, `action`
- **Params**: `approval_id` — path · `action` — path · `body` — JSON body
- **Returns (parsed)**: `ApprovalResult`
- **Returns (raw)**: `ApiResult[ApprovalResult, DecideApprovalErrorBody]`
- **Error**: `DecideApprovalErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `ActionOrStr` | `aegis_fleet/models/enums/action.py` |
| `ApprovalBody` | `aegis_fleet/models/approval_body.py` |
| `ApprovalBodyDict` | `aegis_fleet/models/approval_body.py` |
| `ApprovalResult` | `aegis_fleet/models/approval_result.py` |
| `DecideApprovalErrorBody` | `aegis_fleet/errors/decide_approval_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.dispute_detail

- **Route**: `GET /api/disputes/{dispute_id}`
- **Auth**: `http_basic`
- **Signature**: `def dispute_detail(dispute_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `dispute_id`
- **Params**: `dispute_id` — path
- **Returns (parsed)**: `DisputeDetail`
- **Returns (raw)**: `ApiResult[DisputeDetail, DisputeDetailErrorBody]`
- **Error**: `DisputeDetailErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, 404, anything unmapped]

| Type | Source |
| --- | --- |
| `DisputeDetail` | `aegis_fleet/models/dispute_detail.py` |
| `DisputeDetailErrorBody` | `aegis_fleet/errors/dispute_detail_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.disputes

- **Route**: `GET /api/disputes`
- **Auth**: `http_basic`
- **Signature**: `def disputes(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `list[Dispute]`
- **Returns (raw)**: `ApiResult[list[Dispute], DisputesErrorBody]`
- **Error**: `DisputesErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Dispute` | `aegis_fleet/models/dispute.py` |
| `DisputesErrorBody` | `aegis_fleet/errors/disputes_error.py` |

### client.console.get_killswitch

- **Route**: `GET /api/killswitch`
- **Auth**: `http_basic`
- **Signature**: `def get_killswitch(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `KillSwitch`
- **Returns (raw)**: `ApiResult[KillSwitch, GetKillswitchErrorBody]`
- **Error**: `GetKillswitchErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `KillSwitch` | `aegis_fleet/models/kill_switch.py` |
| `GetKillswitchErrorBody` | `aegis_fleet/errors/get_killswitch_error.py` |

### client.console.health

- **Route**: `GET /api/health`
- **Auth**: `http_basic`
- **Signature**: `def health(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Health`
- **Returns (raw)**: `ApiResult[Health, HealthErrorBody]`
- **Error**: `HealthErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Health` | `aegis_fleet/models/health.py` |
| `HealthErrorBody` | `aegis_fleet/errors/health_error.py` |

### client.console.inbox

- **Route**: `POST /api/inbox`
- **Auth**: `http_basic`
- **Signature**: `def inbox(body: InboxEmail | InboxEmailDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `body`
- **Params**: `body` — JSON body
- **Returns (parsed)**: `InboxVerdict`
- **Returns (raw)**: `ApiResult[InboxVerdict, InboxErrorBody]`
- **Error**: `InboxErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `InboxEmail` | `aegis_fleet/models/inbox_email.py` |
| `InboxEmailDict` | `aegis_fleet/models/inbox_email.py` |
| `InboxVerdict` | `aegis_fleet/models/inbox_verdict.py` |
| `InboxErrorBody` | `aegis_fleet/errors/inbox_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.invoices

- **Route**: `GET /api/invoices`
- **Auth**: `http_basic`
- **Signature**: `def invoices(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `list[Invoice]`
- **Returns (raw)**: `ApiResult[list[Invoice], InvoicesErrorBody]`
- **Error**: `InvoicesErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Invoice` | `aegis_fleet/models/invoice.py` |
| `InvoicesErrorBody` | `aegis_fleet/errors/invoices_error.py` |

### client.console.ledger

- **Route**: `GET /api/ledger`
- **Auth**: `http_basic`
- **Signature**: `def ledger(*, kind: str | None = None, subject_id: str | None = None, limit: int | None = 100, request_options: RequestOptionsOrDict | None = None)`
- **Params**: `kind` — query · `subject_id` — query · `limit` — query
- **Returns (parsed)**: `list[LedgerEntry]`
- **Returns (raw)**: `ApiResult[list[LedgerEntry], LedgerErrorBody]`
- **Error**: `LedgerErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `LedgerEntry` | `aegis_fleet/models/ledger_entry.py` |
| `LedgerErrorBody` | `aegis_fleet/errors/ledger_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.ledger_verify

- **Route**: `GET /api/ledger/verify`
- **Auth**: `http_basic`
- **Signature**: `def ledger_verify(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `ChainVerify`
- **Returns (raw)**: `ApiResult[ChainVerify, LedgerVerifyErrorBody]`
- **Error**: `LedgerVerifyErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `ChainVerify` | `aegis_fleet/models/chain_verify.py` |
| `LedgerVerifyErrorBody` | `aegis_fleet/errors/ledger_verify_error.py` |

### client.console.login

- **Route**: `POST /api/login`
- **Signature**: `def login(body: LoginBody | LoginBodyDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `body`
- **Params**: `body` — JSON body
- **Returns (parsed)**: `Me`
- **Returns (raw)**: `ApiResult[Me, LoginErrorBody]`
- **Error**: `LoginErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `LoginBody` | `aegis_fleet/models/login_body.py` |
| `LoginBodyDict` | `aegis_fleet/models/login_body.py` |
| `Me` | `aegis_fleet/models/me.py` |
| `LoginErrorBody` | `aegis_fleet/errors/login_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.logout

- **Route**: `POST /api/logout`
- **Signature**: `def logout(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Ok`
- **Returns (raw)**: `ApiResult[Ok, LogoutErrorBody]`
- **Error**: `LogoutErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Ok` | `aegis_fleet/models/ok.py` |
| `LogoutErrorBody` | `aegis_fleet/errors/logout_error.py` |

### client.console.mcp_link

- **Route**: `GET /api/mcp/link`
- **Auth**: `http_basic`
- **Signature**: `def mcp_link(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, McpLinkErrorBody]`
- **Error**: `McpLinkErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `McpLinkErrorBody` | `aegis_fleet/errors/mcp_link_error.py` |

### client.console.me

- **Route**: `GET /api/me`
- **Auth**: `http_basic`
- **Signature**: `def me(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Me`
- **Returns (raw)**: `ApiResult[Me, MeErrorBody]`
- **Error**: `MeErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Me` | `aegis_fleet/models/me.py` |
| `MeErrorBody` | `aegis_fleet/errors/me_error.py` |

### client.console.plans_cancel

- **Route**: `POST /api/plans/{plan_id}/cancel`
- **Auth**: `http_basic`
- **Signature**: `def plans_cancel(plan_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `plan_id`
- **Params**: `plan_id` — path
- **Returns (parsed)**: `Ok`
- **Returns (raw)**: `ApiResult[Ok, PlansCancelErrorBody]`
- **Error**: `PlansCancelErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, 404, anything unmapped]

| Type | Source |
| --- | --- |
| `Ok` | `aegis_fleet/models/ok.py` |
| `PlansCancelErrorBody` | `aegis_fleet/errors/plans_cancel_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.plans_list

- **Route**: `GET /api/plans`
- **Auth**: `http_basic`
- **Signature**: `def plans_list(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `list[Plan]`
- **Returns (raw)**: `ApiResult[list[Plan], PlansListErrorBody]`
- **Error**: `PlansListErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Plan` | `aegis_fleet/models/plan.py` |
| `PlansListErrorBody` | `aegis_fleet/errors/plans_list_error.py` |

### client.console.plans_move

- **Route**: `PATCH /api/plans/{plan_id}`
- **Auth**: `http_basic`
- **Signature**: `def plans_move(plan_id: str, body: PlanMove | PlanMoveDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `plan_id`, `body`
- **Params**: `plan_id` — path · `body` — JSON body
- **Returns (parsed)**: `Plan`
- **Returns (raw)**: `ApiResult[Plan, PlansMoveErrorBody]`
- **Error**: `PlansMoveErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, 404, anything unmapped]

| Type | Source |
| --- | --- |
| `PlanMove` | `aegis_fleet/models/plan_move.py` |
| `PlanMoveDict` | `aegis_fleet/models/plan_move.py` |
| `Plan` | `aegis_fleet/models/plan.py` |
| `PlansMoveErrorBody` | `aegis_fleet/errors/plans_move_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.post_killswitch

- **Route**: `POST /api/killswitch`
- **Auth**: `http_basic`
- **Signature**: `def post_killswitch(body: KillSwitchBody | KillSwitchBodyDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `body`
- **Params**: `body` — JSON body
- **Returns (parsed)**: `KillSwitch`
- **Returns (raw)**: `ApiResult[KillSwitch, PostKillswitchErrorBody]`
- **Error**: `PostKillswitchErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `KillSwitchBody` | `aegis_fleet/models/kill_switch_body.py` |
| `KillSwitchBodyDict` | `aegis_fleet/models/kill_switch_body.py` |
| `KillSwitch` | `aegis_fleet/models/kill_switch.py` |
| `PostKillswitchErrorBody` | `aegis_fleet/errors/post_killswitch_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.runs

- **Route**: `GET /api/runs`
- **Auth**: `http_basic`
- **Signature**: `def runs(*, limit: int | None = 20, request_options: RequestOptionsOrDict | None = None)`
- **Params**: `limit` — query
- **Returns (parsed)**: `list[AgentRun]`
- **Returns (raw)**: `ApiResult[list[AgentRun], RunsErrorBody]`
- **Error**: `RunsErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `AgentRun` | `aegis_fleet/models/agent_run.py` |
| `RunsErrorBody` | `aegis_fleet/errors/runs_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.shipments

- **Route**: `POST /api/shipments`
- **Auth**: `http_basic`
- **Signature**: `def shipments(body: ShipmentBody | ShipmentBodyDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `body`
- **Params**: `body` — JSON body
- **Returns (parsed)**: `ShipmentResult`
- **Returns (raw)**: `ApiResult[ShipmentResult, ShipmentsErrorBody]`
- **Error**: `ShipmentsErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `ShipmentBody` | `aegis_fleet/models/shipment_body.py` |
| `ShipmentBodyDict` | `aegis_fleet/models/shipment_body.py` |
| `ShipmentResult` | `aegis_fleet/models/shipment_result.py` |
| `ShipmentsErrorBody` | `aegis_fleet/errors/shipments_error.py` |
| `HttpValidationError` | `aegis_fleet/models/http_validation_error.py` |

### client.console.summary

- **Route**: `GET /api/summary`
- **Auth**: `http_basic`
- **Signature**: `def summary(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Summary`
- **Returns (raw)**: `ApiResult[Summary, SummaryErrorBody]`
- **Error**: `SummaryErrorBody` — **Case A (typed)**
- **Error arms**: `RawError` [401, anything unmapped]

| Type | Source |
| --- | --- |
| `Summary` | `aegis_fleet/models/summary.py` |
| `SummaryErrorBody` | `aegis_fleet/errors/summary_error.py` |

