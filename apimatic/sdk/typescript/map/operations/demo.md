<!-- Generated file — do not edit; regenerated with the SDK. -->

# Demo — operations

Accessor: `client.demo` · Source: `src/resources/demo.ts` · 9 operations · Request types: namespace `Demo`

**Type sources**: every type an operation names, with the file that declares it and the schema value exported beside it. Import every name from `aegis-fleet`; the `Source` path is where to **read** the shape, never what to import. `ApiError`, the runtime error family and the file vocabulary are excluded — see sdk-map.md.

### delivered

- **Signature**: `delivered(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/delivered`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

### demoStatus

- **Signature**: `demoStatus(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/demo/status`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### overdue

- **Signature**: `overdue(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/overdue`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

### replayInjection

- **Signature**: `replayInjection(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/replay_injection`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

### reset

- **Signature**: `reset(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/reset`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

### sandboxInvoice

- **Signature**: `sandboxInvoice(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/sandbox_invoice`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

### sandboxRecordPayment

- **Signature**: `sandboxRecordPayment(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/sandbox_record_payment`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

### scamEmail

- **Signature**: `scamEmail(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/scam_email`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

### tamper

- **Signature**: `tamper(options?: RequestOptions): ApiPromise<DemoResult, ApiError>`
- **Wire**: `POST /api/demo/tamper`
- **Auth**: `httpBasic`
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `DemoResult`
- **Error**: `AegisFleetError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

| Type | Schema value | Source |
| --- | --- | --- |
| `DemoResult` | `demoResultSchema` | `src/models/demo-result.ts` |

