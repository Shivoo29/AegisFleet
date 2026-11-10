from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from ..core import (
    ApiResult,
    AsyncRawClient,
    BaseRawResponse,
    RawClient,
    RawError,
    RequestOptionsOrDict,
    async_json_decoder,
    json_decoder,
    param,
    raw_error_response,
    unwrap,
)
from ..server.server import Server


class Webhooks:
    def __init__(self, client: RawClient, server: Server) -> None:
        self._with_raw_response = WebhooksWithRawResponse(client, server)

    def paypal_webhook(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """PayPal calls this. The signature is verified with PayPal before the event is sealed and routed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.paypal_webhook(request_options=request_options))

    @property
    def with_raw_response(self) -> WebhooksWithRawResponse:
        return self._with_raw_response


class AsyncWebhooks:
    def __init__(self, client: AsyncRawClient, server: Server) -> None:
        self._with_raw_response = AsyncWebhooksWithRawResponse(client, server)

    async def paypal_webhook(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """PayPal calls this. The signature is verified with PayPal before the event is sealed and routed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.paypal_webhook(request_options=request_options))

    @property
    def with_raw_response(self) -> AsyncWebhooksWithRawResponse:
        return self._with_raw_response


class WebhooksWithRawResponse(BaseRawResponse[RawClient, Server]):
    def paypal_webhook(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """PayPal calls this. The signature is verified with PayPal before the event is sealed and routed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/webhooks/paypal"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )


class AsyncWebhooksWithRawResponse(BaseRawResponse[AsyncRawClient, Server]):
    async def paypal_webhook(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """PayPal calls this. The signature is verified with PayPal before the event is sealed and routed.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/webhooks/paypal"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )
