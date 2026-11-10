# Raw Reference

**Raw** endpoints, reached through `with_raw_response`, return `ApiResult[T, E]` and never raise for an API error. For the parsed endpoints, see [API Reference](api-reference.md).

> Source: [AegisFleetClient](aegis_fleet/client.py)

## Console

> Source: [Console](aegis_fleet/apis/console.py)

<details>
<summary><code>def approvals(*, status: str | None = "pending", request_options: RequestOptionsOrDict | None = None) -> ApiResult[list[Approval], ApprovalsErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Agent actions the gateway held for a human decision (over the money cap).

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.approvals()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Approval]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ApprovalsErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.approvals()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Approval]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ApprovalsErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>status</code> | <code>str \| None</code> | Current status<br>**Default**: <code>"pending"</code> |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;list&#91;[Approval](aegis_fleet/models/approval.py)&#93;, [ApprovalsErrorBody](aegis_fleet/errors/approvals_error.py)&#93;</code>

**On `Success`**: `payload` is <code>list&#91;[Approval](aegis_fleet/models/approval.py)&#93;</code> -- OK

**On `Failure`**: `error` is <code>[ApprovalsErrorBody](aegis_fleet/errors/approvals_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def decide_approval(approval_id: str, action: ActionOrStr, *, body: ApprovalBody | ApprovalBodyDict | None = None, request_options: RequestOptionsOrDict | None = None) -> ApiResult[ApprovalResult, DecideApprovalErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Approve (the gateway then executes the held action) or reject it. Both are sealed.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.decide_approval("some example string", Action.APPROVE)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type ApprovalResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type DecideApprovalErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.decide_approval("some example string", Action.APPROVE)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type ApprovalResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type DecideApprovalErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>approval_id</code> | <code>str</code> | Id of the pending approval for this action |
| <code>action</code> | <code>[ActionOrStr](aegis_fleet/models/enums/action.py)</code> | approve or reject |
| <code>body</code> | <code>[ApprovalBody](aegis_fleet/models/approval_body.py) \| [ApprovalBodyDict](aegis_fleet/models/approval_body.py) \| None</code> | The request body.<br>**Default**: <code>None</code> |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[ApprovalResult](aegis_fleet/models/approval_result.py), [DecideApprovalErrorBody](aegis_fleet/errors/decide_approval_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[ApprovalResult](aegis_fleet/models/approval_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[DecideApprovalErrorBody](aegis_fleet/errors/decide_approval_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def dispute_detail(dispute_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DisputeDetail, DisputeDetailErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

One dispute with Defender's evidence pack and the pending approval to submit it.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.dispute_detail("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DisputeDetail
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type DisputeDetailErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.dispute_detail("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DisputeDetail
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type DisputeDetailErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>dispute_id</code> | <code>str</code> | PayPal dispute id, e.g. PP-D-12345 |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DisputeDetail](aegis_fleet/models/dispute_detail.py), [DisputeDetailErrorBody](aegis_fleet/errors/dispute_detail_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[DisputeDetail](aegis_fleet/models/dispute_detail.py)</code> -- OK

**On `Failure`**: `error` is <code>[DisputeDetailErrorBody](aegis_fleet/errors/dispute_detail_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401, 404 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def disputes(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[list[Dispute], DisputesErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Latest state of every PayPal dispute, newest first.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.disputes()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Dispute]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type DisputesErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.disputes()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Dispute]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type DisputesErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;list&#91;[Dispute](aegis_fleet/models/dispute.py)&#93;, [DisputesErrorBody](aegis_fleet/errors/disputes_error.py)&#93;</code>

**On `Success`**: `payload` is <code>list&#91;[Dispute](aegis_fleet/models/dispute.py)&#93;</code> -- OK

**On `Failure`**: `error` is <code>[DisputesErrorBody](aegis_fleet/errors/disputes_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def get_killswitch(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[KillSwitch, GetKillswitchErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Is the kill switch on?

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.get_killswitch()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type KillSwitch
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type GetKillswitchErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.get_killswitch()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type KillSwitch
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type GetKillswitchErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[KillSwitch](aegis_fleet/models/kill_switch.py), [GetKillswitchErrorBody](aegis_fleet/errors/get_killswitch_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[KillSwitch](aegis_fleet/models/kill_switch.py)</code> -- OK

**On `Failure`**: `error` is <code>[GetKillswitchErrorBody](aegis_fleet/errors/get_killswitch_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def health(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Health, HealthErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Score and factors are recomputed from the ledger on every call, so a dispute that
arrived after Guardian's last run still counts. Guardian's AI recommendations are
reused only while the factors they were written for still hold.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.health()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Health
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type HealthErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.health()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Health
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type HealthErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[Health](aegis_fleet/models/health.py), [HealthErrorBody](aegis_fleet/errors/health_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[Health](aegis_fleet/models/health.py)</code> -- OK

**On `Failure`**: `error` is <code>[HealthErrorBody](aegis_fleet/errors/health_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def inbox(body: InboxEmail | InboxEmailDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[InboxVerdict, InboxErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Run Sentinel inline (a few seconds) so the console gets the verdict in one call.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.inbox(InboxEmail())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type InboxVerdict
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type InboxErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.inbox(InboxEmail())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type InboxVerdict
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type InboxErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[InboxEmail](aegis_fleet/models/inbox_email.py) \| [InboxEmailDict](aegis_fleet/models/inbox_email.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[InboxVerdict](aegis_fleet/models/inbox_verdict.py), [InboxErrorBody](aegis_fleet/errors/inbox_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[InboxVerdict](aegis_fleet/models/inbox_verdict.py)</code> -- OK

**On `Failure`**: `error` is <code>[InboxErrorBody](aegis_fleet/errors/inbox_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def invoices(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[list[Invoice], InvoicesErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Invoices with paid/overdue status, risk, shipment and PayPal payment link.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.invoices()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Invoice]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type InvoicesErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.invoices()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Invoice]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type InvoicesErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;list&#91;[Invoice](aegis_fleet/models/invoice.py)&#93;, [InvoicesErrorBody](aegis_fleet/errors/invoices_error.py)&#93;</code>

**On `Success`**: `payload` is <code>list&#91;[Invoice](aegis_fleet/models/invoice.py)&#93;</code> -- OK

**On `Failure`**: `error` is <code>[InvoicesErrorBody](aegis_fleet/errors/invoices_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def ledger(*, kind: str | None = None, subject_id: str | None = None, limit: int | None = 100, request_options: RequestOptionsOrDict | None = None) -> ApiResult[list[LedgerEntry], LedgerErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Proof Ledger entries, newest first. Each entry's hash covers the previous one.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.ledger()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[LedgerEntry]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LedgerErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.ledger()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[LedgerEntry]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LedgerErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>kind</code> | <code>str \| None</code> | Entry kind: event, decision, agent_step, approval or note<br>**Default**: <code>None</code> |
| <code>subject_id</code> | <code>str \| None</code> | What this is about: an invoice, dispute or email id<br>**Default**: <code>None</code> |
| <code>limit</code> | <code>int \| None</code> | Maximum number of items to return<br>**Default**: <code>100</code> |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;list&#91;[LedgerEntry](aegis_fleet/models/ledger_entry.py)&#93;, [LedgerErrorBody](aegis_fleet/errors/ledger_error.py)&#93;</code>

**On `Success`**: `payload` is <code>list&#91;[LedgerEntry](aegis_fleet/models/ledger_entry.py)&#93;</code> -- OK

**On `Failure`**: `error` is <code>[LedgerErrorBody](aegis_fleet/errors/ledger_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def ledger_verify(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[ChainVerify, LedgerVerifyErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Recompute every hash in the chain and report the first entry that no longer matches.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.ledger_verify()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type ChainVerify
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LedgerVerifyErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.ledger_verify()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type ChainVerify
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LedgerVerifyErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[ChainVerify](aegis_fleet/models/chain_verify.py), [LedgerVerifyErrorBody](aegis_fleet/errors/ledger_verify_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[ChainVerify](aegis_fleet/models/chain_verify.py)</code> -- OK

**On `Failure`**: `error` is <code>[LedgerVerifyErrorBody](aegis_fleet/errors/ledger_verify_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def login(body: LoginBody | LoginBodyDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Me, LoginErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Check a username and password and set a 12-hour session cookie.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.login(LoginBody())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Me
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LoginErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.login(LoginBody())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Me
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LoginErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[LoginBody](aegis_fleet/models/login_body.py) \| [LoginBodyDict](aegis_fleet/models/login_body.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[Me](aegis_fleet/models/me.py), [LoginErrorBody](aegis_fleet/errors/login_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[Me](aegis_fleet/models/me.py)</code> -- OK

**On `Failure`**: `error` is <code>[LoginErrorBody](aegis_fleet/errors/login_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def logout(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Ok, LogoutErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Clear the session cookie.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.logout()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Ok
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LogoutErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.logout()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Ok
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type LogoutErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[Ok](aegis_fleet/models/ok.py), [LogoutErrorBody](aegis_fleet/errors/logout_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[Ok](aegis_fleet/models/ok.py)</code> -- OK

**On `Failure`**: `error` is <code>[LogoutErrorBody](aegis_fleet/errors/logout_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def me(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Me, MeErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Who is logged in, and whether they are the seller (dev) or a read-mostly judge.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.me()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Me
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type MeErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.me()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Me
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type MeErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[Me](aegis_fleet/models/me.py), [MeErrorBody](aegis_fleet/errors/me_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[Me](aegis_fleet/models/me.py)</code> -- OK

**On `Failure`**: `error` is <code>[MeErrorBody](aegis_fleet/errors/me_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def plans_cancel(plan_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Ok, PlansCancelErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Seller cancels a planned action. Sealed in the ledger.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.plans_cancel("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Ok
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PlansCancelErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.plans_cancel("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Ok
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PlansCancelErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>plan_id</code> | <code>str</code> | plan_id |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[Ok](aegis_fleet/models/ok.py), [PlansCancelErrorBody](aegis_fleet/errors/plans_cancel_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[Ok](aegis_fleet/models/ok.py)</code> -- OK

**On `Failure`**: `error` is <code>[PlansCancelErrorBody](aegis_fleet/errors/plans_cancel_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401, 404 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def plans_list(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[list[Plan], PlansListErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

What the agents have scheduled: planned, done, held, blocked and cancelled actions.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.plans_list()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Plan]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PlansListErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.plans_list()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[Plan]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PlansListErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;list&#91;[Plan](aegis_fleet/models/plan.py)&#93;, [PlansListErrorBody](aegis_fleet/errors/plans_list_error.py)&#93;</code>

**On `Success`**: `payload` is <code>list&#91;[Plan](aegis_fleet/models/plan.py)&#93;</code> -- OK

**On `Failure`**: `error` is <code>[PlansListErrorBody](aegis_fleet/errors/plans_list_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def plans_move(plan_id: str, body: PlanMove | PlanMoveDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Plan, PlansMoveErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.plans_move(
    "some example string", PlanMove(due_at=datetime(2024, 1, 15, 9, 30, 0, tzinfo=timezone.utc))
)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Plan
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PlansMoveErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.plans_move(
    "some example string", PlanMove(due_at=datetime(2024, 1, 15, 9, 30, 0, tzinfo=timezone.utc))
)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Plan
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PlansMoveErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>plan_id</code> | <code>str</code> | plan_id |
| <code>body</code> | <code>[PlanMove](aegis_fleet/models/plan_move.py) \| [PlanMoveDict](aegis_fleet/models/plan_move.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[Plan](aegis_fleet/models/plan.py), [PlansMoveErrorBody](aegis_fleet/errors/plans_move_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[Plan](aegis_fleet/models/plan.py)</code> -- OK

**On `Failure`**: `error` is <code>[PlansMoveErrorBody](aegis_fleet/errors/plans_move_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401, 404 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def post_killswitch(body: KillSwitchBody | KillSwitchBodyDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[KillSwitch, PostKillswitchErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Turn the kill switch on or off. While on, the gateway denies every agent action.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.post_killswitch(KillSwitchBody())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type KillSwitch
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PostKillswitchErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.post_killswitch(KillSwitchBody())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type KillSwitch
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type PostKillswitchErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[KillSwitchBody](aegis_fleet/models/kill_switch_body.py) \| [KillSwitchBodyDict](aegis_fleet/models/kill_switch_body.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[KillSwitch](aegis_fleet/models/kill_switch.py), [PostKillswitchErrorBody](aegis_fleet/errors/post_killswitch_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[KillSwitch](aegis_fleet/models/kill_switch.py)</code> -- OK

**On `Failure`**: `error` is <code>[PostKillswitchErrorBody](aegis_fleet/errors/post_killswitch_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def runs(*, limit: int | None = 20, request_options: RequestOptionsOrDict | None = None) -> ApiResult[list[AgentRun], RunsErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Recent agent runs with their steps and structured output.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.runs()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[AgentRun]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RunsErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.runs()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type list[AgentRun]
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RunsErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>limit</code> | <code>int \| None</code> | Maximum number of items to return<br>**Default**: <code>20</code> |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;list&#91;[AgentRun](aegis_fleet/models/agent_run.py)&#93;, [RunsErrorBody](aegis_fleet/errors/runs_error.py)&#93;</code>

**On `Success`**: `payload` is <code>list&#91;[AgentRun](aegis_fleet/models/agent_run.py)&#93;</code> -- OK

**On `Failure`**: `error` is <code>[RunsErrorBody](aegis_fleet/errors/runs_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def shipments(body: ShipmentBody | ShipmentBodyDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[ShipmentResult, ShipmentsErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.shipments(ShipmentBody())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type ShipmentResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ShipmentsErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.shipments(ShipmentBody())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type ShipmentResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ShipmentsErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[ShipmentBody](aegis_fleet/models/shipment_body.py) \| [ShipmentBodyDict](aegis_fleet/models/shipment_body.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[ShipmentResult](aegis_fleet/models/shipment_result.py), [ShipmentsErrorBody](aegis_fleet/errors/shipments_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[ShipmentResult](aegis_fleet/models/shipment_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[ShipmentsErrorBody](aegis_fleet/errors/shipments_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| 422 | <code>[HttpValidationError](aegis_fleet/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def summary(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Summary, SummaryErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain state.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.console.with_raw_response.summary()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Summary
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type SummaryErrorBody
```

**Async**

```python
result = await async_client.console.with_raw_response.summary()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Summary
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type SummaryErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[Summary](aegis_fleet/models/summary.py), [SummaryErrorBody](aegis_fleet/errors/summary_error.py)&#93;</code>

**On `Success`**: `payload` is <code>[Summary](aegis_fleet/models/summary.py)</code> -- OK

**On `Failure`**: `error` is <code>[SummaryErrorBody](aegis_fleet/errors/summary_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 401 | <code>[RawError](aegis_fleet/core/results.py)</code> |
| anything unmapped | <code>[RawError](aegis_fleet/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

## Demo

> Source: [Demo](aegis_fleet/apis/demo.py)

<details>
<summary><code>def delivered(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Courier says the parcel arrived -> Guardian updates tracking.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.delivered()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.delivered()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def demo_status(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

200 when demo mode is on (404 otherwise).

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.demo_status()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.demo_status()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;Any, [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def overdue(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.overdue()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.overdue()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def replay_injection(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.replay_injection()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.replay_injection()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def reset(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Wipe everything, then replay Riya's story so the console never starts empty.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.reset()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.reset()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def sandbox_invoice(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Create a real invoice in the PayPal sandbox. Paying it fires a real, signed webhook.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.sandbox_invoice()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.sandbox_invoice()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def sandbox_record_payment(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.

PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.sandbox_record_payment()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.sandbox_record_payment()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def scam_email(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Fake 'payment received' email: no verified payment in the ledger -> Sentinel says scam.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.scam_email()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.scam_email()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def tamper(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Edit one sealed entry behind the ledger's back -> verify() points at it.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.demo.with_raw_response.tamper()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.demo.with_raw_response.tamper()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type DemoResult
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;[DemoResult](aegis_fleet/models/demo_result.py), [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

## Ops

> Source: [Ops](aegis_fleet/apis/ops.py)

<details>
<summary><code>def healthz(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Liveness probe for Render and the keep-alive ping. No auth.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.ops.with_raw_response.healthz()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.ops.with_raw_response.healthz()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;Any, [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

## Webhooks

> Source: [Webhooks](aegis_fleet/apis/webhooks.py)

<details>
<summary><code>def paypal_webhook(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

PayPal calls this. The signature is verified with PayPal before the event is sealed and routed.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.webhooks.with_raw_response.paypal_webhook()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.webhooks.with_raw_response.paypal_webhook()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](aegis_fleet/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](aegis_fleet/core/results.py)&#91;Any, [RawError](aegis_fleet/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](aegis_fleet/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

