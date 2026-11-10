# Reference

> Source: [AegisFleetClient](src/client.ts)

## Console

> Source: [Console](src/resources/console.ts)

<details>
<summary><code>approvals(request?: Console.ApprovalsRequest, options?: RequestOptions): ApiPromise&lt;Approval[], Console.ApprovalsError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Agent actions the gateway held for a human decision (over the money cap).

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.approvals();
  // TODO: Handle 'response' of type Approval[]
} catch (err) {
  // TODO: Handle 'err' of type Console.ApprovalsError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.approvals().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Approval[]
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>status?</code> | <code>string</code> | Current status<br>**Default**: "pending" |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.approvals(request)`

- **OnSuccess**: <code>[Approval](src/models/approval.ts)[]</code>
- **OnError**: throws <code>[Console.ApprovalsError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.approvals(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Approval[], Console.ApprovalsError&gt;</code>, with `result.value` of type <code>[Approval](src/models/approval.ts)[]</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>decideApproval(request: Console.DecideApprovalRequest, options?: RequestOptions): ApiPromise&lt;ApprovalResult, Console.DecideApprovalError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Approve (the gateway then executes the held action) or reject it. Both are sealed.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.decideApproval({
    approvalId: "some example string",
    action: Action.Approve,
  });
  // TODO: Handle 'response' of type ApprovalResult
} catch (err) {
  // TODO: Handle 'err' of type Console.DecideApprovalError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console
  .decideApproval({ approvalId: "some example string", action: Action.Approve })
  .asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type ApprovalResult
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>approvalId</code> | <code>string</code> | Id of the pending approval for this action |
| <code>action</code> | <code>[Action](src/models/action.ts)</code> | approve or reject |
| <code>body?</code> | <code>[Body1](src/models/unions/body1.ts)</code> | - |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.decideApproval(request)`

- **OnSuccess**: <code>[ApprovalResult](src/models/approval-result.ts)</code>
- **OnError**: throws <code>[Console.DecideApprovalError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.decideApproval(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;ApprovalResult, Console.DecideApprovalError&gt;</code>, with `result.value` of type <code>[ApprovalResult](src/models/approval-result.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>disputeDetail(request: Console.DisputeDetailRequest, options?: RequestOptions): ApiPromise&lt;DisputeDetail, Console.DisputeDetailError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

One dispute with Defender's evidence pack and the pending approval to submit it.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.disputeDetail({ disputeId: "some example string" });
  // TODO: Handle 'response' of type DisputeDetail
} catch (err) {
  // TODO: Handle 'err' of type Console.DisputeDetailError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.disputeDetail({ disputeId: "some example string" }).asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DisputeDetail
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>disputeId</code> | <code>string</code> | PayPal dispute id, e.g. PP-D-12345 |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.disputeDetail(request)`

- **OnSuccess**: <code>[DisputeDetail](src/models/dispute-detail.ts)</code>
- **OnError**: throws <code>[Console.DisputeDetailError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.disputeDetail(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DisputeDetail, Console.DisputeDetailError&gt;</code>, with `result.value` of type <code>[DisputeDetail](src/models/dispute-detail.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>disputes(options?: RequestOptions): ApiPromise&lt;Dispute[], Console.DisputesError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Latest state of every PayPal dispute, newest first.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.disputes();
  // TODO: Handle 'response' of type Dispute[]
} catch (err) {
  // TODO: Handle 'err' of type Console.DisputesError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.disputes().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Dispute[]
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.disputes()`

- **OnSuccess**: <code>[Dispute](src/models/dispute.ts)[]</code>
- **OnError**: throws <code>[Console.DisputesError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.disputes().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Dispute[], Console.DisputesError&gt;</code>, with `result.value` of type <code>[Dispute](src/models/dispute.ts)[]</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>getKillswitch(options?: RequestOptions): ApiPromise&lt;KillSwitch, Console.GetKillswitchError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Is the kill switch on?

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.getKillswitch();
  // TODO: Handle 'response' of type KillSwitch
} catch (err) {
  // TODO: Handle 'err' of type Console.GetKillswitchError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.getKillswitch().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type KillSwitch
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.getKillswitch()`

- **OnSuccess**: <code>[KillSwitch](src/models/kill-switch.ts)</code>
- **OnError**: throws <code>[Console.GetKillswitchError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.getKillswitch().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;KillSwitch, Console.GetKillswitchError&gt;</code>, with `result.value` of type <code>[KillSwitch](src/models/kill-switch.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>health(options?: RequestOptions): ApiPromise&lt;Health, Console.HealthError&gt;</code></summary>

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

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.health();
  // TODO: Handle 'response' of type Health
} catch (err) {
  // TODO: Handle 'err' of type Console.HealthError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.health().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Health
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.health()`

- **OnSuccess**: <code>[Health](src/models/health.ts)</code>
- **OnError**: throws <code>[Console.HealthError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.health().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Health, Console.HealthError&gt;</code>, with `result.value` of type <code>[Health](src/models/health.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>inbox(request: Console.InboxRequest, options?: RequestOptions): ApiPromise&lt;InboxVerdict, Console.InboxError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Run Sentinel inline (a few seconds) so the console gets the verdict in one call.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.inbox({ body: {} });
  // TODO: Handle 'response' of type InboxVerdict
} catch (err) {
  // TODO: Handle 'err' of type Console.InboxError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.inbox({ body: {} }).asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type InboxVerdict
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[InboxEmail](src/models/inbox-email.ts)</code> | - |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.inbox(request)`

- **OnSuccess**: <code>[InboxVerdict](src/models/inbox-verdict.ts)</code>
- **OnError**: throws <code>[Console.InboxError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.inbox(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;InboxVerdict, Console.InboxError&gt;</code>, with `result.value` of type <code>[InboxVerdict](src/models/inbox-verdict.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>invoices(options?: RequestOptions): ApiPromise&lt;Invoice[], Console.InvoicesError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Invoices with paid/overdue status, risk, shipment and PayPal payment link.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.invoices();
  // TODO: Handle 'response' of type Invoice[]
} catch (err) {
  // TODO: Handle 'err' of type Console.InvoicesError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.invoices().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Invoice[]
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.invoices()`

- **OnSuccess**: <code>[Invoice](src/models/invoice.ts)[]</code>
- **OnError**: throws <code>[Console.InvoicesError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.invoices().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Invoice[], Console.InvoicesError&gt;</code>, with `result.value` of type <code>[Invoice](src/models/invoice.ts)[]</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>ledger(request?: Console.LedgerRequest, options?: RequestOptions): ApiPromise&lt;LedgerEntry[], Console.LedgerError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Proof Ledger entries, newest first. Each entry's hash covers the previous one.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.ledger();
  // TODO: Handle 'response' of type LedgerEntry[]
} catch (err) {
  // TODO: Handle 'err' of type Console.LedgerError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.ledger().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type LedgerEntry[]
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>kind?</code> | <code>[Kind1](src/models/unions/kind1.ts)</code> | Entry kind: event, decision, agent_step, approval or note |
| <code>subjectId?</code> | <code>[SubjectIdModel](src/models/unions/subject-id-model.ts)</code> | What this is about: an invoice, dispute or email id |
| <code>limit?</code> | <code>number</code> | Maximum number of items to return<br>**Default**: 100 |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.ledger(request)`

- **OnSuccess**: <code>[LedgerEntry](src/models/ledger-entry.ts)[]</code>
- **OnError**: throws <code>[Console.LedgerError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.ledger(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;LedgerEntry[], Console.LedgerError&gt;</code>, with `result.value` of type <code>[LedgerEntry](src/models/ledger-entry.ts)[]</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>ledgerVerify(options?: RequestOptions): ApiPromise&lt;ChainVerify, Console.LedgerVerifyError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Recompute every hash in the chain and report the first entry that no longer matches.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.ledgerVerify();
  // TODO: Handle 'response' of type ChainVerify
} catch (err) {
  // TODO: Handle 'err' of type Console.LedgerVerifyError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.ledgerVerify().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type ChainVerify
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.ledgerVerify()`

- **OnSuccess**: <code>[ChainVerify](src/models/chain-verify.ts)</code>
- **OnError**: throws <code>[Console.LedgerVerifyError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.ledgerVerify().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;ChainVerify, Console.LedgerVerifyError&gt;</code>, with `result.value` of type <code>[ChainVerify](src/models/chain-verify.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>login(request: Console.LoginRequest, options?: RequestOptions): ApiPromise&lt;Me, Console.LoginError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Check a username and password and set a 12-hour session cookie.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.login({ body: {} });
  // TODO: Handle 'response' of type Me
} catch (err) {
  // TODO: Handle 'err' of type Console.LoginError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.login({ body: {} }).asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Me
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[LoginBody](src/models/login-body.ts)</code> | - |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.login(request)`

- **OnSuccess**: <code>[Me](src/models/me.ts)</code>
- **OnError**: throws <code>[Console.LoginError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.login(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Me, Console.LoginError&gt;</code>, with `result.value` of type <code>[Me](src/models/me.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>logout(options?: RequestOptions): ApiPromise&lt;Ok, Console.LogoutError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Clear the session cookie.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.logout();
  // TODO: Handle 'response' of type Ok
} catch (err) {
  // TODO: Handle 'err' of type Console.LogoutError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.logout().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Ok
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.logout()`

- **OnSuccess**: <code>[Ok](src/models/ok.ts)</code>
- **OnError**: throws <code>[Console.LogoutError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.logout().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Ok, Console.LogoutError&gt;</code>, with `result.value` of type <code>[Ok](src/models/ok.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>me(options?: RequestOptions): ApiPromise&lt;Me, Console.MeError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Who is logged in, and whether they are the seller (dev) or a read-mostly judge.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.me();
  // TODO: Handle 'response' of type Me
} catch (err) {
  // TODO: Handle 'err' of type Console.MeError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.me().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Me
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.me()`

- **OnSuccess**: <code>[Me](src/models/me.ts)</code>
- **OnError**: throws <code>[Console.MeError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.me().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Me, Console.MeError&gt;</code>, with `result.value` of type <code>[Me](src/models/me.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>plansCancel(request: Console.PlansCancelRequest, options?: RequestOptions): ApiPromise&lt;Ok, Console.PlansCancelError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Seller cancels a planned action. Sealed in the ledger.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.plansCancel({ planId: "some example string" });
  // TODO: Handle 'response' of type Ok
} catch (err) {
  // TODO: Handle 'err' of type Console.PlansCancelError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.plansCancel({ planId: "some example string" }).asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Ok
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>planId</code> | <code>string</code> | plan_id |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.plansCancel(request)`

- **OnSuccess**: <code>[Ok](src/models/ok.ts)</code>
- **OnError**: throws <code>[Console.PlansCancelError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.plansCancel(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Ok, Console.PlansCancelError&gt;</code>, with `result.value` of type <code>[Ok](src/models/ok.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>plansList(options?: RequestOptions): ApiPromise&lt;Plan[], Console.PlansListError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

What the agents have scheduled: planned, done, held, blocked and cancelled actions.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.plansList();
  // TODO: Handle 'response' of type Plan[]
} catch (err) {
  // TODO: Handle 'err' of type Console.PlansListError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.plansList().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Plan[]
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.plansList()`

- **OnSuccess**: <code>[Plan](src/models/plan.ts)[]</code>
- **OnError**: throws <code>[Console.PlansListError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.plansList().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Plan[], Console.PlansListError&gt;</code>, with `result.value` of type <code>[Plan](src/models/plan.ts)[]</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>plansMove(request: Console.PlansMoveRequest, options?: RequestOptions): ApiPromise&lt;Plan, Console.PlansMoveError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.plansMove({
    planId: "some example string",
    body: { dueAt: new Date(Date.UTC(2024, 0, 15, 9, 30, 0)) },
  });
  // TODO: Handle 'response' of type Plan
} catch (err) {
  // TODO: Handle 'err' of type Console.PlansMoveError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console
  .plansMove({ planId: "some example string", body: { dueAt: new Date(Date.UTC(2024, 0, 15, 9, 30, 0)) } })
  .asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Plan
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>planId</code> | <code>string</code> | plan_id |
| <code>body</code> | <code>[PlanMove](src/models/plan-move.ts)</code> | - |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.plansMove(request)`

- **OnSuccess**: <code>[Plan](src/models/plan.ts)</code>
- **OnError**: throws <code>[Console.PlansMoveError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.plansMove(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Plan, Console.PlansMoveError&gt;</code>, with `result.value` of type <code>[Plan](src/models/plan.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>postKillswitch(request: Console.PostKillswitchRequest, options?: RequestOptions): ApiPromise&lt;KillSwitch, Console.PostKillswitchError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Turn the kill switch on or off. While on, the gateway denies every agent action.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.postKillswitch({ body: {} });
  // TODO: Handle 'response' of type KillSwitch
} catch (err) {
  // TODO: Handle 'err' of type Console.PostKillswitchError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.postKillswitch({ body: {} }).asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type KillSwitch
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[KillSwitchBody](src/models/kill-switch-body.ts)</code> | - |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.postKillswitch(request)`

- **OnSuccess**: <code>[KillSwitch](src/models/kill-switch.ts)</code>
- **OnError**: throws <code>[Console.PostKillswitchError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.postKillswitch(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;KillSwitch, Console.PostKillswitchError&gt;</code>, with `result.value` of type <code>[KillSwitch](src/models/kill-switch.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>runs(request?: Console.RunsRequest, options?: RequestOptions): ApiPromise&lt;AgentRun[], Console.RunsError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Recent agent runs with their steps and structured output.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.runs();
  // TODO: Handle 'response' of type AgentRun[]
} catch (err) {
  // TODO: Handle 'err' of type Console.RunsError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.runs().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type AgentRun[]
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>limit?</code> | <code>number</code> | Maximum number of items to return<br>**Default**: 20 |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.runs(request)`

- **OnSuccess**: <code>[AgentRun](src/models/agent-run.ts)[]</code>
- **OnError**: throws <code>[Console.RunsError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.runs(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;AgentRun[], Console.RunsError&gt;</code>, with `result.value` of type <code>[AgentRun](src/models/agent-run.ts)[]</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>shipments(request: Console.ShipmentsRequest, options?: RequestOptions): ApiPromise&lt;ShipmentResult, Console.ShipmentsError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.shipments({ body: {} });
  // TODO: Handle 'response' of type ShipmentResult
} catch (err) {
  // TODO: Handle 'err' of type Console.ShipmentsError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.shipments({ body: {} }).asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type ShipmentResult
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[ShipmentBody](src/models/shipment-body.ts)</code> | - |

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.shipments(request)`

- **OnSuccess**: <code>[ShipmentResult](src/models/shipment-result.ts)</code>
- **OnError**: throws <code>[Console.ShipmentsError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.shipments(request).asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;ShipmentResult, Console.ShipmentsError&gt;</code>, with `result.value` of type <code>[ShipmentResult](src/models/shipment-result.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>summary(options?: RequestOptions): ApiPromise&lt;Summary, Console.SummaryError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain state.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.console.summary();
  // TODO: Handle 'response' of type Summary
} catch (err) {
  // TODO: Handle 'err' of type Console.SummaryError, discriminated with 'err.payload.kind'
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.console.summary().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Summary
} else {
  // TODO: Handle 'result', discriminated with 'result.payload.kind'
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.console.summary()`

- **OnSuccess**: <code>[Summary](src/models/summary.ts)</code>
- **OnError**: throws <code>[Console.SummaryError](src/resources/console.ts)</code>, with `err.payload` discriminated on `kind`

**As ApiResult**: `await client.console.summary().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Summary, Console.SummaryError&gt;</code>, with `result.value` of type <code>[Summary](src/models/summary.ts)</code>
- **OnError**: `result.payload` discriminated on `kind`, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

## Demo

> Source: [Demo](src/resources/demo.ts)

<details>
<summary><code>delivered(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Courier says the parcel arrived -> Guardian updates tracking.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.delivered();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.delivered().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.delivered()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.delivered().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>demoStatus(options?: RequestOptions): ApiPromise&lt;Record&lt;string, unknown&gt;, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

200 when demo mode is on (404 otherwise).

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.demoStatus();
  // TODO: Handle 'response' of type Record<string, unknown>
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.demoStatus().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Record<string, unknown>
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.demoStatus()`

- **OnSuccess**: <code>Record&lt;string, unknown&gt;</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.demoStatus().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Record&lt;string, unknown&gt;, ApiError&gt;</code>, with `result.value` of type <code>Record&lt;string, unknown&gt;</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>overdue(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.overdue();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.overdue().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.overdue()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.overdue().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>replayInjection(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.replayInjection();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.replayInjection().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.replayInjection()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.replayInjection().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>reset(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Wipe everything, then replay Riya's story so the console never starts empty.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.reset();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.reset().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.reset()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.reset().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>sandboxInvoice(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Create a real invoice in the PayPal sandbox. Paying it fires a real, signed webhook.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.sandboxInvoice();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.sandboxInvoice().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.sandboxInvoice()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.sandboxInvoice().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>sandboxRecordPayment(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.

PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.sandboxRecordPayment();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.sandboxRecordPayment().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.sandboxRecordPayment()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.sandboxRecordPayment().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>scamEmail(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Fake 'payment received' email: no verified payment in the ledger -> Sentinel says scam.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.scamEmail();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.scamEmail().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.scamEmail()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.scamEmail().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>tamper(options?: RequestOptions): ApiPromise&lt;DemoResult, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Edit one sealed entry behind the ledger's back -> verify() points at it.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.demo.tamper();
  // TODO: Handle 'response' of type DemoResult
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.demo.tamper().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type DemoResult
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.demo.tamper()`

- **OnSuccess**: <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.demo.tamper().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;DemoResult, ApiError&gt;</code>, with `result.value` of type <code>[DemoResult](src/models/demo-result.ts)</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

## Ops

> Source: [Ops](src/resources/ops.ts)

<details>
<summary><code>healthz(options?: RequestOptions): ApiPromise&lt;Record&lt;string, unknown&gt;, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Liveness probe for Render and the keep-alive ping. No auth.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.ops.healthz();
  // TODO: Handle 'response' of type Record<string, unknown>
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.ops.healthz().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Record<string, unknown>
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.ops.healthz()`

- **OnSuccess**: <code>Record&lt;string, unknown&gt;</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.ops.healthz().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Record&lt;string, unknown&gt;, ApiError&gt;</code>, with `result.value` of type <code>Record&lt;string, unknown&gt;</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

## Webhooks

> Source: [Webhooks](src/resources/webhooks.ts)

<details>
<summary><code>paypalWebhook(options?: RequestOptions): ApiPromise&lt;Record&lt;string, unknown&gt;, ApiError&gt;</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

PayPal calls this. The signature is verified with PayPal before the event is sealed and routed.

</dd>
</dl>

### Direct Usage

<dl>
<dd>

```ts
try {
  const response = await client.webhooks.paypalWebhook();
  // TODO: Handle 'response' of type Record<string, unknown>
} catch (err) {
  // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Usage as ApiResult

<dl>
<dd>

```ts
const result = await client.webhooks.paypalWebhook().asApiResult();
// TODO: Use 'result.status' and 'result.headers' to read the raw response status and headers
if (result.ok) {
  // TODO: Use 'result.value' of type Record<string, unknown>
} else {
  // TODO: Handle 'result', where 'result.payload' is always the Undeclared arm
}
```

</dd>
</dl>

### Response

<dl>
<dd>

**Direct**: `await client.webhooks.paypalWebhook()`

- **OnSuccess**: <code>Record&lt;string, unknown&gt;</code>
- **OnError**: throws <code>[ApiError](src/core/api-error.ts)</code>, with `err.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm

**As ApiResult**: `await client.webhooks.paypalWebhook().asApiResult()`

- **OnSuccess**: <code>[ApiResult](src/core/api-promise.ts)&lt;Record&lt;string, unknown&gt;, ApiError&gt;</code>, with `result.value` of type <code>Record&lt;string, unknown&gt;</code>
- **OnError**: `result.payload` always the <code>[Undeclared](src/core/api-error.ts)</code> arm, with `result.message`

**Thrown**: <code>[AegisFleetError](src/core/errors.ts)</code> on any operational failure — a caller abort and a programmer error stay outside the family and reach you raw

</dd>
</dl>

</dd>
</dl>

</details>

