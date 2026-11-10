from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from ..auth import AsyncAuthSchemes, AuthSchemes
from ..core import (
    ApiResult,
    AsyncRawClient,
    RawClient,
    RawError,
    RequestOptionsOrDict,
    SecuredRawResponse,
    async_json_decoder,
    json_decoder,
    param,
    raw_error_response,
    unwrap,
)
from ..models.demo_result import DemoResult
from ..server.server import Server


class Demo:
    def __init__(self, client: RawClient, server: Server, auth: AuthSchemes) -> None:
        self._with_raw_response = DemoWithRawResponse(client, server, auth)

    def delivered(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Courier says the parcel arrived -> Guardian updates tracking.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.delivered(request_options=request_options))

    def demo_status(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """200 when demo mode is on (404 otherwise).

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.demo_status(request_options=request_options))

    def overdue(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.overdue(request_options=request_options))

    def replay_injection(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.replay_injection(request_options=request_options))

    def reset(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Wipe everything, then replay Riya's story so the console never starts empty.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.reset(request_options=request_options))

    def sandbox_invoice(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Create a real invoice in the PayPal sandbox. Paying it fires a real, signed webhook.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.sandbox_invoice(request_options=request_options))

    def sandbox_record_payment(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.

        PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.sandbox_record_payment(request_options=request_options))

    def scam_email(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Fake 'payment received' email: no verified payment in the ledger -> Sentinel says scam.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.scam_email(request_options=request_options))

    def tamper(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Edit one sealed entry behind the ledger's back -> verify() points at it.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.tamper(request_options=request_options))

    @property
    def with_raw_response(self) -> DemoWithRawResponse:
        return self._with_raw_response


class AsyncDemo:
    def __init__(self, client: AsyncRawClient, server: Server, auth: AsyncAuthSchemes) -> None:
        self._with_raw_response = AsyncDemoWithRawResponse(client, server, auth)

    async def delivered(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Courier says the parcel arrived -> Guardian updates tracking.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.delivered(request_options=request_options))

    async def demo_status(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """200 when demo mode is on (404 otherwise).

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.demo_status(request_options=request_options))

    async def overdue(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.overdue(request_options=request_options))

    async def replay_injection(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.replay_injection(request_options=request_options))

    async def reset(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Wipe everything, then replay Riya's story so the console never starts empty.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.reset(request_options=request_options))

    async def sandbox_invoice(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Create a real invoice in the PayPal sandbox. Paying it fires a real, signed webhook.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.sandbox_invoice(request_options=request_options))

    async def sandbox_record_payment(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.

        PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.sandbox_record_payment(request_options=request_options))

    async def scam_email(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Fake 'payment received' email: no verified payment in the ledger -> Sentinel says scam.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.scam_email(request_options=request_options))

    async def tamper(self, *, request_options: RequestOptionsOrDict | None = None) -> DemoResult:
        """Edit one sealed entry behind the ledger's back -> verify() points at it.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.tamper(request_options=request_options))

    @property
    def with_raw_response(self) -> AsyncDemoWithRawResponse:
        return self._with_raw_response


class DemoWithRawResponse(SecuredRawResponse[RawClient, Server, AuthSchemes]):
    def delivered(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """Courier says the parcel arrived -> Guardian updates tracking.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/delivered"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def demo_status(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """200 when demo mode is on (404 otherwise).

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/demo/status"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def overdue(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/overdue"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def replay_injection(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/replay_injection"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def reset(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """Wipe everything, then replay Riya's story so the console never starts empty.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/reset"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def sandbox_invoice(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """Create a real invoice in the PayPal sandbox. Paying it fires a real, signed webhook.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/sandbox_invoice"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def sandbox_record_payment(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.

        PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/sandbox_record_payment"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def scam_email(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """Fake 'payment received' email: no verified payment in the ledger -> Sentinel says scam.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/scam_email"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    def tamper(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """Edit one sealed entry behind the ledger's back -> verify() points at it.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/tamper"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )


class AsyncDemoWithRawResponse(SecuredRawResponse[AsyncRawClient, Server, AsyncAuthSchemes]):
    async def delivered(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """Courier says the parcel arrived -> Guardian updates tracking.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/delivered"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def demo_status(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """200 when demo mode is on (404 otherwise).

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/demo/status"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def overdue(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/overdue"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def replay_injection(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/replay_injection"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def reset(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """Wipe everything, then replay Riya's story so the console never starts empty.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/reset"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def sandbox_invoice(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """Create a real invoice in the PayPal sandbox. Paying it fires a real, signed webhook.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/sandbox_invoice"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def sandbox_record_payment(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.

        PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/sandbox_record_payment"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def scam_email(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DemoResult, RawError]:
        """Fake 'payment received' email: no verified payment in the ledger -> Sentinel says scam.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/scam_email"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def tamper(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[DemoResult, RawError]:
        """Edit one sealed entry behind the ledger's back -> verify() points at it.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/tamper"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DemoResult],
            error_mapper=raw_error_response,
            request_options=request_options,
        )
