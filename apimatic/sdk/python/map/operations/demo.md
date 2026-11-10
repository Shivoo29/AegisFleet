<!-- Generated file — do not edit; regenerated with the SDK. -->

# Demo — operations

Accessor: `client.demo` · Source: `aegis_fleet/apis/demo.py` · 9 operations

Each `###` block is one operation and assumes `sdk-map.md` is loaded: blocks omit what its invariants table covers and are otherwise self-contained, so chunk at block level. Signatures are the sync parsed spelling; the async and raw spellings take the same parameters (see sdk-map.md). **Type sources** names the module declaring each type an operation mentions, so resolving a body, return or error payload is a lookup rather than a search; the runtime types `RawError` and `ApiResult` are excluded, and an operation with no table mentions nothing but builtins and those.

### client.demo.delivered

- **Route**: `POST /api/demo/delivered`
- **Auth**: `http_basic`
- **Signature**: `def delivered(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

### client.demo.demo_status

- **Route**: `GET /api/demo/status`
- **Auth**: `http_basic`
- **Signature**: `def demo_status(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.demo.overdue

- **Route**: `POST /api/demo/overdue`
- **Auth**: `http_basic`
- **Signature**: `def overdue(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

### client.demo.replay_injection

- **Route**: `POST /api/demo/replay_injection`
- **Auth**: `http_basic`
- **Signature**: `def replay_injection(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

### client.demo.reset

- **Route**: `POST /api/demo/reset`
- **Auth**: `http_basic`
- **Signature**: `def reset(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

### client.demo.sandbox_invoice

- **Route**: `POST /api/demo/sandbox_invoice`
- **Auth**: `http_basic`
- **Signature**: `def sandbox_invoice(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

### client.demo.sandbox_record_payment

- **Route**: `POST /api/demo/sandbox_record_payment`
- **Auth**: `http_basic`
- **Signature**: `def sandbox_record_payment(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

### client.demo.scam_email

- **Route**: `POST /api/demo/scam_email`
- **Auth**: `http_basic`
- **Signature**: `def scam_email(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

### client.demo.tamper

- **Route**: `POST /api/demo/tamper`
- **Auth**: `http_basic`
- **Signature**: `def tamper(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `DemoResult`
- **Returns (raw)**: `ApiResult[DemoResult, RawError]`
- **Error**: `RawError` — **Case B**

| Type | Source |
| --- | --- |
| `DemoResult` | `aegis_fleet/models/demo_result.py` |

