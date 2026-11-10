# Reference

**Parsed** endpoints return the typed payload and raise `ApiError` on a documented non-2xx. For the raw endpoints, see [Raw API Reference](raw-api-reference.md).

> Source: [AegisFleetClient](aegis_fleet/client.py)

## Console

> Source: [Console](aegis_fleet/apis/console.py)

<details>
<summary><code>def approvals(*, status: str | None = "pending", request_options: RequestOptionsOrDict | None = None) -> list[Approval]</code></summary>

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
try:
    response = client.console.approvals()
    # TODO: Handle 'response' of type list[Approval]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type ApprovalsErrorBody
```

**Async**

```python
try:
    response = await async_client.console.approvals()
    # TODO: Handle 'response' of type list[Approval]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type ApprovalsErrorBody
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

**OnSuccess**: <code>list&#91;[Approval](aegis_fleet/models/approval.py)&#93;</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[ApprovalsErrorBody](aegis_fleet/errors/approvals_error.py)&#93;</code>

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
<summary><code>def decide_approval(approval_id: str, action: ActionOrStr, *, body: ApprovalBody | ApprovalBodyDict | None = None, request_options: RequestOptionsOrDict | None = None) -> ApprovalResult</code></summary>

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
try:
    response = client.console.decide_approval("some example string", Action.APPROVE)
    # TODO: Handle 'response' of type ApprovalResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type DecideApprovalErrorBody
```

**Async**

```python
try:
    response = await async_client.console.decide_approval("some example string", Action.APPROVE)
    # TODO: Handle 'response' of type ApprovalResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type DecideApprovalErrorBody
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

**OnSuccess**: <code>[ApprovalResult](aegis_fleet/models/approval_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[DecideApprovalErrorBody](aegis_fleet/errors/decide_approval_error.py)&#93;</code>

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
<summary><code>def dispute_detail(dispute_id: str, *, request_options: RequestOptionsOrDict | None = None) -> DisputeDetail</code></summary>

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
try:
    response = client.console.dispute_detail("some example string")
    # TODO: Handle 'response' of type DisputeDetail
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type DisputeDetailErrorBody
```

**Async**

```python
try:
    response = await async_client.console.dispute_detail("some example string")
    # TODO: Handle 'response' of type DisputeDetail
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type DisputeDetailErrorBody
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

**OnSuccess**: <code>[DisputeDetail](aegis_fleet/models/dispute_detail.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[DisputeDetailErrorBody](aegis_fleet/errors/dispute_detail_error.py)&#93;</code>

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
<summary><code>def disputes(*, request_options: RequestOptionsOrDict | None = None) -> list[Dispute]</code></summary>

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
try:
    response = client.console.disputes()
    # TODO: Handle 'response' of type list[Dispute]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type DisputesErrorBody
```

**Async**

```python
try:
    response = await async_client.console.disputes()
    # TODO: Handle 'response' of type list[Dispute]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type DisputesErrorBody
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

**OnSuccess**: <code>list&#91;[Dispute](aegis_fleet/models/dispute.py)&#93;</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[DisputesErrorBody](aegis_fleet/errors/disputes_error.py)&#93;</code>

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
<summary><code>def get_killswitch(*, request_options: RequestOptionsOrDict | None = None) -> KillSwitch</code></summary>

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
try:
    response = client.console.get_killswitch()
    # TODO: Handle 'response' of type KillSwitch
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type GetKillswitchErrorBody
```

**Async**

```python
try:
    response = await async_client.console.get_killswitch()
    # TODO: Handle 'response' of type KillSwitch
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type GetKillswitchErrorBody
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

**OnSuccess**: <code>[KillSwitch](aegis_fleet/models/kill_switch.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[GetKillswitchErrorBody](aegis_fleet/errors/get_killswitch_error.py)&#93;</code>

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
<summary><code>def health(*, request_options: RequestOptionsOrDict | None = None) -> Health</code></summary>

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
try:
    response = client.console.health()
    # TODO: Handle 'response' of type Health
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type HealthErrorBody
```

**Async**

```python
try:
    response = await async_client.console.health()
    # TODO: Handle 'response' of type Health
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type HealthErrorBody
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

**OnSuccess**: <code>[Health](aegis_fleet/models/health.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[HealthErrorBody](aegis_fleet/errors/health_error.py)&#93;</code>

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
<summary><code>def inbox(body: InboxEmail | InboxEmailDict, *, request_options: RequestOptionsOrDict | None = None) -> InboxVerdict</code></summary>

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
try:
    response = client.console.inbox(InboxEmail())
    # TODO: Handle 'response' of type InboxVerdict
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type InboxErrorBody
```

**Async**

```python
try:
    response = await async_client.console.inbox(InboxEmail())
    # TODO: Handle 'response' of type InboxVerdict
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type InboxErrorBody
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

**OnSuccess**: <code>[InboxVerdict](aegis_fleet/models/inbox_verdict.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[InboxErrorBody](aegis_fleet/errors/inbox_error.py)&#93;</code>

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
<summary><code>def invoices(*, request_options: RequestOptionsOrDict | None = None) -> list[Invoice]</code></summary>

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
try:
    response = client.console.invoices()
    # TODO: Handle 'response' of type list[Invoice]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type InvoicesErrorBody
```

**Async**

```python
try:
    response = await async_client.console.invoices()
    # TODO: Handle 'response' of type list[Invoice]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type InvoicesErrorBody
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

**OnSuccess**: <code>list&#91;[Invoice](aegis_fleet/models/invoice.py)&#93;</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[InvoicesErrorBody](aegis_fleet/errors/invoices_error.py)&#93;</code>

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
<summary><code>def ledger(*, kind: str | None = None, subject_id: str | None = None, limit: int | None = 100, request_options: RequestOptionsOrDict | None = None) -> list[LedgerEntry]</code></summary>

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
try:
    response = client.console.ledger()
    # TODO: Handle 'response' of type list[LedgerEntry]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LedgerErrorBody
```

**Async**

```python
try:
    response = await async_client.console.ledger()
    # TODO: Handle 'response' of type list[LedgerEntry]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LedgerErrorBody
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

**OnSuccess**: <code>list&#91;[LedgerEntry](aegis_fleet/models/ledger_entry.py)&#93;</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[LedgerErrorBody](aegis_fleet/errors/ledger_error.py)&#93;</code>

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
<summary><code>def ledger_verify(*, request_options: RequestOptionsOrDict | None = None) -> ChainVerify</code></summary>

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
try:
    response = client.console.ledger_verify()
    # TODO: Handle 'response' of type ChainVerify
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LedgerVerifyErrorBody
```

**Async**

```python
try:
    response = await async_client.console.ledger_verify()
    # TODO: Handle 'response' of type ChainVerify
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LedgerVerifyErrorBody
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

**OnSuccess**: <code>[ChainVerify](aegis_fleet/models/chain_verify.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[LedgerVerifyErrorBody](aegis_fleet/errors/ledger_verify_error.py)&#93;</code>

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
<summary><code>def login(body: LoginBody | LoginBodyDict, *, request_options: RequestOptionsOrDict | None = None) -> Me</code></summary>

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
try:
    response = client.console.login(LoginBody())
    # TODO: Handle 'response' of type Me
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LoginErrorBody
```

**Async**

```python
try:
    response = await async_client.console.login(LoginBody())
    # TODO: Handle 'response' of type Me
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LoginErrorBody
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

**OnSuccess**: <code>[Me](aegis_fleet/models/me.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[LoginErrorBody](aegis_fleet/errors/login_error.py)&#93;</code>

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
<summary><code>def logout(*, request_options: RequestOptionsOrDict | None = None) -> Ok</code></summary>

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
try:
    response = client.console.logout()
    # TODO: Handle 'response' of type Ok
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LogoutErrorBody
```

**Async**

```python
try:
    response = await async_client.console.logout()
    # TODO: Handle 'response' of type Ok
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type LogoutErrorBody
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

**OnSuccess**: <code>[Ok](aegis_fleet/models/ok.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[LogoutErrorBody](aegis_fleet/errors/logout_error.py)&#93;</code>

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
<summary><code>def me(*, request_options: RequestOptionsOrDict | None = None) -> Me</code></summary>

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
try:
    response = client.console.me()
    # TODO: Handle 'response' of type Me
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type MeErrorBody
```

**Async**

```python
try:
    response = await async_client.console.me()
    # TODO: Handle 'response' of type Me
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type MeErrorBody
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

**OnSuccess**: <code>[Me](aegis_fleet/models/me.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[MeErrorBody](aegis_fleet/errors/me_error.py)&#93;</code>

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
<summary><code>def plans_cancel(plan_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Ok</code></summary>

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
try:
    response = client.console.plans_cancel("some example string")
    # TODO: Handle 'response' of type Ok
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PlansCancelErrorBody
```

**Async**

```python
try:
    response = await async_client.console.plans_cancel("some example string")
    # TODO: Handle 'response' of type Ok
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PlansCancelErrorBody
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

**OnSuccess**: <code>[Ok](aegis_fleet/models/ok.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[PlansCancelErrorBody](aegis_fleet/errors/plans_cancel_error.py)&#93;</code>

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
<summary><code>def plans_list(*, request_options: RequestOptionsOrDict | None = None) -> list[Plan]</code></summary>

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
try:
    response = client.console.plans_list()
    # TODO: Handle 'response' of type list[Plan]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PlansListErrorBody
```

**Async**

```python
try:
    response = await async_client.console.plans_list()
    # TODO: Handle 'response' of type list[Plan]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PlansListErrorBody
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

**OnSuccess**: <code>list&#91;[Plan](aegis_fleet/models/plan.py)&#93;</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[PlansListErrorBody](aegis_fleet/errors/plans_list_error.py)&#93;</code>

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
<summary><code>def plans_move(plan_id: str, body: PlanMove | PlanMoveDict, *, request_options: RequestOptionsOrDict | None = None) -> Plan</code></summary>

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
try:
    response = client.console.plans_move(
        "some example string", PlanMove(due_at=datetime(2024, 1, 15, 9, 30, 0, tzinfo=timezone.utc))
    )
    # TODO: Handle 'response' of type Plan
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PlansMoveErrorBody
```

**Async**

```python
try:
    response = await async_client.console.plans_move(
        "some example string", PlanMove(due_at=datetime(2024, 1, 15, 9, 30, 0, tzinfo=timezone.utc))
    )
    # TODO: Handle 'response' of type Plan
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PlansMoveErrorBody
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

**OnSuccess**: <code>[Plan](aegis_fleet/models/plan.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[PlansMoveErrorBody](aegis_fleet/errors/plans_move_error.py)&#93;</code>

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
<summary><code>def post_killswitch(body: KillSwitchBody | KillSwitchBodyDict, *, request_options: RequestOptionsOrDict | None = None) -> KillSwitch</code></summary>

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
try:
    response = client.console.post_killswitch(KillSwitchBody())
    # TODO: Handle 'response' of type KillSwitch
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PostKillswitchErrorBody
```

**Async**

```python
try:
    response = await async_client.console.post_killswitch(KillSwitchBody())
    # TODO: Handle 'response' of type KillSwitch
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type PostKillswitchErrorBody
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

**OnSuccess**: <code>[KillSwitch](aegis_fleet/models/kill_switch.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[PostKillswitchErrorBody](aegis_fleet/errors/post_killswitch_error.py)&#93;</code>

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
<summary><code>def runs(*, limit: int | None = 20, request_options: RequestOptionsOrDict | None = None) -> list[AgentRun]</code></summary>

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
try:
    response = client.console.runs()
    # TODO: Handle 'response' of type list[AgentRun]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RunsErrorBody
```

**Async**

```python
try:
    response = await async_client.console.runs()
    # TODO: Handle 'response' of type list[AgentRun]
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RunsErrorBody
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

**OnSuccess**: <code>list&#91;[AgentRun](aegis_fleet/models/agent_run.py)&#93;</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RunsErrorBody](aegis_fleet/errors/runs_error.py)&#93;</code>

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
<summary><code>def shipments(body: ShipmentBody | ShipmentBodyDict, *, request_options: RequestOptionsOrDict | None = None) -> ShipmentResult</code></summary>

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
try:
    response = client.console.shipments(ShipmentBody())
    # TODO: Handle 'response' of type ShipmentResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type ShipmentsErrorBody
```

**Async**

```python
try:
    response = await async_client.console.shipments(ShipmentBody())
    # TODO: Handle 'response' of type ShipmentResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type ShipmentsErrorBody
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

**OnSuccess**: <code>[ShipmentResult](aegis_fleet/models/shipment_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[ShipmentsErrorBody](aegis_fleet/errors/shipments_error.py)&#93;</code>

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
<summary><code>def summary(*, request_options: RequestOptionsOrDict | None = None) -> Summary</code></summary>

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
try:
    response = client.console.summary()
    # TODO: Handle 'response' of type Summary
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type SummaryErrorBody
```

**Async**

```python
try:
    response = await async_client.console.summary()
    # TODO: Handle 'response' of type Summary
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type SummaryErrorBody
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

**OnSuccess**: <code>[Summary](aegis_fleet/models/summary.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[SummaryErrorBody](aegis_fleet/errors/summary_error.py)&#93;</code>

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
<summary><code>def delivered(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.delivered()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.delivered()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def demo_status(*, request_options: RequestOptionsOrDict | None = None) -> Any</code></summary>

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
try:
    response = client.demo.demo_status()
    # TODO: Handle 'response' of type Any
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.demo_status()
    # TODO: Handle 'response' of type Any
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>Any</code> -- Successful Response

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def overdue(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.overdue()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.overdue()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def replay_injection(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.replay_injection()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.replay_injection()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def reset(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.reset()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.reset()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def sandbox_invoice(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.sandbox_invoice()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.sandbox_invoice()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def sandbox_record_payment(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.sandbox_record_payment()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.sandbox_record_payment()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def scam_email(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.scam_email()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.scam_email()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def tamper(*, request_options: RequestOptionsOrDict | None = None) -> DemoResult</code></summary>

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
try:
    response = client.demo.tamper()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.demo.tamper()
    # TODO: Handle 'response' of type DemoResult
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>[DemoResult](aegis_fleet/models/demo_result.py)</code> -- OK

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

## Ops

> Source: [Ops](aegis_fleet/apis/ops.py)

<details>
<summary><code>def healthz(*, request_options: RequestOptionsOrDict | None = None) -> Any</code></summary>

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
try:
    response = client.ops.healthz()
    # TODO: Handle 'response' of type Any
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.ops.healthz()
    # TODO: Handle 'response' of type Any
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>Any</code> -- Successful Response

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

## Webhooks

> Source: [Webhooks](aegis_fleet/apis/webhooks.py)

<details>
<summary><code>def paypal_webhook(*, request_options: RequestOptionsOrDict | None = None) -> Any</code></summary>

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
try:
    response = client.webhooks.paypal_webhook()
    # TODO: Handle 'response' of type Any
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
```

**Async**

```python
try:
    response = await async_client.webhooks.paypal_webhook()
    # TODO: Handle 'response' of type Any
except ApiError as e:
    ...  # TODO: Handle 'e.error' of type RawError
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

**OnSuccess**: <code>Any</code> -- Successful Response

**OnError**: <code>[ApiError](aegis_fleet/core/exceptions.py)&#91;[RawError](aegis_fleet/core/results.py)&#93;</code>

</dd>
</dl>

</dd>
</dl>

</details>

