from __future__ import annotations

from typing import Any

from ..core import (
    ApiResult,
    AsyncRawClient,
    BaseRawResponse,
    RawClient,
    RawError,
    RequestOptionsOrDict,
    async_json_decoder,
    json_decoder,
    raw_error_response,
    unwrap,
)
from ..server.server import Server


class Ops:
    def __init__(self, client: RawClient, server: Server) -> None:
        self._with_raw_response = OpsWithRawResponse(client, server)

    def healthz(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Liveness probe for Render and the keep-alive ping. No auth.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.healthz(request_options=request_options))

    @property
    def with_raw_response(self) -> OpsWithRawResponse:
        return self._with_raw_response


class AsyncOps:
    def __init__(self, client: AsyncRawClient, server: Server) -> None:
        self._with_raw_response = AsyncOpsWithRawResponse(client, server)

    async def healthz(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Liveness probe for Render and the keep-alive ping. No auth.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.healthz(request_options=request_options))

    @property
    def with_raw_response(self) -> AsyncOpsWithRawResponse:
        return self._with_raw_response


class OpsWithRawResponse(BaseRawResponse[RawClient, Server]):
    def healthz(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Liveness probe for Render and the keep-alive ping. No auth.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/healthz"),
            decoder=json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )


class AsyncOpsWithRawResponse(BaseRawResponse[AsyncRawClient, Server]):
    async def healthz(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Liveness probe for Render and the keep-alive ping. No auth.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/healthz"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )
