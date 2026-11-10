from __future__ import annotations

from uuid import UUID, uuid4

from ..auth import AsyncAuthSchemes, AuthSchemes
from ..core import (
    ApiResult,
    AsyncRawClient,
    RawClient,
    RequestOptionsOrDict,
    SecuredRawResponse,
    async_json_decoder,
    json_body,
    json_decoder,
    param,
    unwrap,
)
from ..errors.approvals_error import ApprovalsErrorBody, approvals_error_mapper
from ..errors.decide_approval_error import DecideApprovalErrorBody, decide_approval_error_mapper
from ..errors.dispute_detail_error import DisputeDetailErrorBody, dispute_detail_error_mapper
from ..errors.disputes_error import DisputesErrorBody, disputes_error_mapper
from ..errors.get_killswitch_error import GetKillswitchErrorBody, get_killswitch_error_mapper
from ..errors.health_error import HealthErrorBody, health_error_mapper
from ..errors.inbox_error import InboxErrorBody, inbox_error_mapper
from ..errors.invoices_error import InvoicesErrorBody, invoices_error_mapper
from ..errors.ledger_error import LedgerErrorBody, ledger_error_mapper
from ..errors.ledger_verify_error import LedgerVerifyErrorBody, ledger_verify_error_mapper
from ..errors.login_error import LoginErrorBody, login_error_mapper
from ..errors.logout_error import LogoutErrorBody, logout_error_mapper
from ..errors.me_error import MeErrorBody, me_error_mapper
from ..errors.plans_cancel_error import PlansCancelErrorBody, plans_cancel_error_mapper
from ..errors.plans_list_error import PlansListErrorBody, plans_list_error_mapper
from ..errors.plans_move_error import PlansMoveErrorBody, plans_move_error_mapper
from ..errors.post_killswitch_error import PostKillswitchErrorBody, post_killswitch_error_mapper
from ..errors.runs_error import RunsErrorBody, runs_error_mapper
from ..errors.shipments_error import ShipmentsErrorBody, shipments_error_mapper
from ..errors.summary_error import SummaryErrorBody, summary_error_mapper
from ..models.agent_run import AgentRun
from ..models.approval import Approval
from ..models.approval_body import ApprovalBody, ApprovalBodyDict
from ..models.approval_result import ApprovalResult
from ..models.chain_verify import ChainVerify
from ..models.dispute import Dispute
from ..models.dispute_detail import DisputeDetail
from ..models.enums.action import ActionOrStr
from ..models.health import Health
from ..models.inbox_email import InboxEmail, InboxEmailDict
from ..models.inbox_verdict import InboxVerdict
from ..models.invoice import Invoice
from ..models.kill_switch import KillSwitch
from ..models.kill_switch_body import KillSwitchBody, KillSwitchBodyDict
from ..models.ledger_entry import LedgerEntry
from ..models.login_body import LoginBody, LoginBodyDict
from ..models.me import Me
from ..models.ok import Ok
from ..models.plan import Plan
from ..models.plan_move import PlanMove, PlanMoveDict
from ..models.shipment_body import ShipmentBody, ShipmentBodyDict
from ..models.shipment_result import ShipmentResult
from ..models.summary import Summary
from ..server.server import Server


class Console:
    def __init__(self, client: RawClient, server: Server, auth: AuthSchemes) -> None:
        self._with_raw_response = ConsoleWithRawResponse(client, server, auth)

    def approvals(
        self, *, status: str | None = "pending", request_options: RequestOptionsOrDict | None = None
    ) -> list[Approval]:
        """Agent actions the gateway held for a human decision (over the money cap).

        Args:
            status: Current status
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.approvals(status=status, request_options=request_options))

    def decide_approval(
        self,
        approval_id: str,
        action: ActionOrStr,
        *,
        body: ApprovalBody | ApprovalBodyDict | None = None,
        request_options: RequestOptionsOrDict | None = None,
    ) -> ApprovalResult:
        """Approve (the gateway then executes the held action) or reject it. Both are sealed.

        Args:
            approval_id: Id of the pending approval for this action
            action: approve or reject
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(
            self._with_raw_response.decide_approval(approval_id, action, body=body, request_options=request_options)
        )

    def dispute_detail(self, dispute_id: str, *, request_options: RequestOptionsOrDict | None = None) -> DisputeDetail:
        """One dispute with Defender's evidence pack and the pending approval to submit it.

        Args:
            dispute_id: PayPal dispute id, e.g. PP-D-12345
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie No such dispute Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.dispute_detail(dispute_id, request_options=request_options))

    def disputes(self, *, request_options: RequestOptionsOrDict | None = None) -> list[Dispute]:
        """Latest state of every PayPal dispute, newest first.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.disputes(request_options=request_options))

    def get_killswitch(self, *, request_options: RequestOptionsOrDict | None = None) -> KillSwitch:
        """Is the kill switch on?

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.get_killswitch(request_options=request_options))

    def health(self, *, request_options: RequestOptionsOrDict | None = None) -> Health:
        """Score and factors are recomputed from the ledger on every call, so a dispute that arrived after Guardian's
        last run still counts. Guardian's AI recommendations are reused only while the factors they were written for
        still hold.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.health(request_options=request_options))

    def inbox(
        self, body: InboxEmail | InboxEmailDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> InboxVerdict:
        """Run Sentinel inline (a few seconds) so the console gets the verdict in one call.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.inbox(body, request_options=request_options))

    def invoices(self, *, request_options: RequestOptionsOrDict | None = None) -> list[Invoice]:
        """Invoices with paid/overdue status, risk, shipment and PayPal payment link.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.invoices(request_options=request_options))

    def ledger(
        self,
        *,
        kind: str | None = None,
        subject_id: str | None = None,
        limit: int | None = 100,
        request_options: RequestOptionsOrDict | None = None,
    ) -> list[LedgerEntry]:
        """Proof Ledger entries, newest first. Each entry's hash covers the previous one.

        Args:
            kind: Entry kind: event, decision, agent_step, approval or note
            subject_id: What this is about: an invoice, dispute or email id
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(
            self._with_raw_response.ledger(
                kind=kind, subject_id=subject_id, limit=limit, request_options=request_options
            ),
        )

    def ledger_verify(self, *, request_options: RequestOptionsOrDict | None = None) -> ChainVerify:
        """Recompute every hash in the chain and report the first entry that no longer matches.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.ledger_verify(request_options=request_options))

    def login(self, body: LoginBody | LoginBodyDict, *, request_options: RequestOptionsOrDict | None = None) -> Me:
        """Check a username and password and set a 12-hour session cookie.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.login(body, request_options=request_options))

    def logout(self, *, request_options: RequestOptionsOrDict | None = None) -> Ok:
        """Clear the session cookie.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.logout(request_options=request_options))

    def me(self, *, request_options: RequestOptionsOrDict | None = None) -> Me:
        """Who is logged in, and whether they are the seller (dev) or a read-mostly judge.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.me(request_options=request_options))

    def plans_cancel(self, plan_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Ok:
        """Seller cancels a planned action. Sealed in the ledger.

        Args:
            plan_id: plan_id
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie No planned action with this id Validation Error
                ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.plans_cancel(plan_id, request_options=request_options))

    def plans_list(self, *, request_options: RequestOptionsOrDict | None = None) -> list[Plan]:
        """What the agents have scheduled: planned, done, held, blocked and cancelled actions.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.plans_list(request_options=request_options))

    def plans_move(
        self, plan_id: str, body: PlanMove | PlanMoveDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Plan:
        """Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.

        Args:
            plan_id: plan_id
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie No planned action with this id Validation Error
                ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.plans_move(plan_id, body, request_options=request_options))

    def post_killswitch(
        self, body: KillSwitchBody | KillSwitchBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> KillSwitch:
        """Turn the kill switch on or off. While on, the gateway denies every agent action.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.post_killswitch(body, request_options=request_options))

    def runs(self, *, limit: int | None = 20, request_options: RequestOptionsOrDict | None = None) -> list[AgentRun]:
        """Recent agent runs with their steps and structured output.

        Args:
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.runs(limit=limit, request_options=request_options))

    def shipments(
        self, body: ShipmentBody | ShipmentBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ShipmentResult:
        """Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(self._with_raw_response.shipments(body, request_options=request_options))

    def summary(self, *, request_options: RequestOptionsOrDict | None = None) -> Summary:
        """Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain state.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(self._with_raw_response.summary(request_options=request_options))

    @property
    def with_raw_response(self) -> ConsoleWithRawResponse:
        return self._with_raw_response


class AsyncConsole:
    def __init__(self, client: AsyncRawClient, server: Server, auth: AsyncAuthSchemes) -> None:
        self._with_raw_response = AsyncConsoleWithRawResponse(client, server, auth)

    async def approvals(
        self, *, status: str | None = "pending", request_options: RequestOptionsOrDict | None = None
    ) -> list[Approval]:
        """Agent actions the gateway held for a human decision (over the money cap).

        Args:
            status: Current status
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.approvals(status=status, request_options=request_options))

    async def decide_approval(
        self,
        approval_id: str,
        action: ActionOrStr,
        *,
        body: ApprovalBody | ApprovalBodyDict | None = None,
        request_options: RequestOptionsOrDict | None = None,
    ) -> ApprovalResult:
        """Approve (the gateway then executes the held action) or reject it. Both are sealed.

        Args:
            approval_id: Id of the pending approval for this action
            action: approve or reject
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(
            await self._with_raw_response.decide_approval(
                approval_id, action, body=body, request_options=request_options
            ),
        )

    async def dispute_detail(
        self, dispute_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> DisputeDetail:
        """One dispute with Defender's evidence pack and the pending approval to submit it.

        Args:
            dispute_id: PayPal dispute id, e.g. PP-D-12345
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie No such dispute Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.dispute_detail(dispute_id, request_options=request_options))

    async def disputes(self, *, request_options: RequestOptionsOrDict | None = None) -> list[Dispute]:
        """Latest state of every PayPal dispute, newest first.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.disputes(request_options=request_options))

    async def get_killswitch(self, *, request_options: RequestOptionsOrDict | None = None) -> KillSwitch:
        """Is the kill switch on?

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.get_killswitch(request_options=request_options))

    async def health(self, *, request_options: RequestOptionsOrDict | None = None) -> Health:
        """Score and factors are recomputed from the ledger on every call, so a dispute that arrived after Guardian's
        last run still counts. Guardian's AI recommendations are reused only while the factors they were written for
        still hold.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.health(request_options=request_options))

    async def inbox(
        self, body: InboxEmail | InboxEmailDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> InboxVerdict:
        """Run Sentinel inline (a few seconds) so the console gets the verdict in one call.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.inbox(body, request_options=request_options))

    async def invoices(self, *, request_options: RequestOptionsOrDict | None = None) -> list[Invoice]:
        """Invoices with paid/overdue status, risk, shipment and PayPal payment link.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.invoices(request_options=request_options))

    async def ledger(
        self,
        *,
        kind: str | None = None,
        subject_id: str | None = None,
        limit: int | None = 100,
        request_options: RequestOptionsOrDict | None = None,
    ) -> list[LedgerEntry]:
        """Proof Ledger entries, newest first. Each entry's hash covers the previous one.

        Args:
            kind: Entry kind: event, decision, agent_step, approval or note
            subject_id: What this is about: an invoice, dispute or email id
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(
            await self._with_raw_response.ledger(
                kind=kind, subject_id=subject_id, limit=limit, request_options=request_options
            ),
        )

    async def ledger_verify(self, *, request_options: RequestOptionsOrDict | None = None) -> ChainVerify:
        """Recompute every hash in the chain and report the first entry that no longer matches.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.ledger_verify(request_options=request_options))

    async def login(
        self, body: LoginBody | LoginBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Me:
        """Check a username and password and set a 12-hour session cookie.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.login(body, request_options=request_options))

    async def logout(self, *, request_options: RequestOptionsOrDict | None = None) -> Ok:
        """Clear the session cookie.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.logout(request_options=request_options))

    async def me(self, *, request_options: RequestOptionsOrDict | None = None) -> Me:
        """Who is logged in, and whether they are the seller (dev) or a read-mostly judge.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.me(request_options=request_options))

    async def plans_cancel(self, plan_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Ok:
        """Seller cancels a planned action. Sealed in the ledger.

        Args:
            plan_id: plan_id
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie No planned action with this id Validation Error
                ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.plans_cancel(plan_id, request_options=request_options))

    async def plans_list(self, *, request_options: RequestOptionsOrDict | None = None) -> list[Plan]:
        """What the agents have scheduled: planned, done, held, blocked and cancelled actions.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.plans_list(request_options=request_options))

    async def plans_move(
        self, plan_id: str, body: PlanMove | PlanMoveDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Plan:
        """Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.

        Args:
            plan_id: plan_id
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie No planned action with this id Validation Error
                ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.plans_move(plan_id, body, request_options=request_options))

    async def post_killswitch(
        self, body: KillSwitchBody | KillSwitchBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> KillSwitch:
        """Turn the kill switch on or off. While on, the gateway denies every agent action.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.post_killswitch(body, request_options=request_options))

    async def runs(
        self, *, limit: int | None = 20, request_options: RequestOptionsOrDict | None = None
    ) -> list[AgentRun]:
        """Recent agent runs with their steps and structured output.

        Args:
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.runs(limit=limit, request_options=request_options))

    async def shipments(
        self, body: ShipmentBody | ShipmentBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ShipmentResult:
        """Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie Validation Error ``error`` is
                ``HttpValidationError | RawError``."""
        return unwrap(await self._with_raw_response.shipments(body, request_options=request_options))

    async def summary(self, *, request_options: RequestOptionsOrDict | None = None) -> Summary:
        """Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain state.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            OK

        Raises:
            ApiError: Login required: HTTP Basic or the session cookie ``error`` is ``RawError``."""
        return unwrap(await self._with_raw_response.summary(request_options=request_options))

    @property
    def with_raw_response(self) -> AsyncConsoleWithRawResponse:
        return self._with_raw_response


class ConsoleWithRawResponse(SecuredRawResponse[RawClient, Server, AuthSchemes]):
    def approvals(
        self, *, status: str | None = "pending", request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Approval], ApprovalsErrorBody]:
        """Agent actions the gateway held for a human decision (over the money cap).

        Args:
            status: Current status
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/approvals"),
            query_params=[param[str | None]("status", status)],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[list[Approval]],
            error_mapper=approvals_error_mapper,
            request_options=request_options,
        )

    def decide_approval(
        self,
        approval_id: str,
        action: ActionOrStr,
        *,
        body: ApprovalBody | ApprovalBodyDict | None = None,
        request_options: RequestOptionsOrDict | None = None,
    ) -> ApiResult[ApprovalResult, DecideApprovalErrorBody]:
        """Approve (the gateway then executes the held action) or reject it. Both are sealed.

        Args:
            approval_id: Id of the pending approval for this action
            action: approve or reject
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/approvals/{approval_id}/{action}"),
            path_params=[param[str]("approval_id", approval_id), param[ActionOrStr]("action", action)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[ApprovalBody | ApprovalBodyDict | None](body),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[ApprovalResult],
            error_mapper=decide_approval_error_mapper,
            request_options=request_options,
        )

    def dispute_detail(
        self, dispute_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DisputeDetail, DisputeDetailErrorBody]:
        """One dispute with Defender's evidence pack and the pending approval to submit it.

        Args:
            dispute_id: PayPal dispute id, e.g. PP-D-12345
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/disputes/{dispute_id}"),
            path_params=[param[str]("dispute_id", dispute_id)],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[DisputeDetail],
            error_mapper=dispute_detail_error_mapper,
            request_options=request_options,
        )

    def disputes(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Dispute], DisputesErrorBody]:
        """Latest state of every PayPal dispute, newest first.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/disputes"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[list[Dispute]],
            error_mapper=disputes_error_mapper,
            request_options=request_options,
        )

    def get_killswitch(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[KillSwitch, GetKillswitchErrorBody]:
        """Is the kill switch on?

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/killswitch"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[KillSwitch],
            error_mapper=get_killswitch_error_mapper,
            request_options=request_options,
        )

    def health(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Health, HealthErrorBody]:
        """Score and factors are recomputed from the ledger on every call, so a dispute that arrived after Guardian's
        last run still counts. Guardian's AI recommendations are reused only while the factors they were written for
        still hold.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/health"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[Health],
            error_mapper=health_error_mapper,
            request_options=request_options,
        )

    def inbox(
        self, body: InboxEmail | InboxEmailDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[InboxVerdict, InboxErrorBody]:
        """Run Sentinel inline (a few seconds) so the console gets the verdict in one call.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/inbox"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[InboxEmail | InboxEmailDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[InboxVerdict],
            error_mapper=inbox_error_mapper,
            request_options=request_options,
        )

    def invoices(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Invoice], InvoicesErrorBody]:
        """Invoices with paid/overdue status, risk, shipment and PayPal payment link.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/invoices"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[list[Invoice]],
            error_mapper=invoices_error_mapper,
            request_options=request_options,
        )

    def ledger(
        self,
        *,
        kind: str | None = None,
        subject_id: str | None = None,
        limit: int | None = 100,
        request_options: RequestOptionsOrDict | None = None,
    ) -> ApiResult[list[LedgerEntry], LedgerErrorBody]:
        """Proof Ledger entries, newest first. Each entry's hash covers the previous one.

        Args:
            kind: Entry kind: event, decision, agent_step, approval or note
            subject_id: What this is about: an invoice, dispute or email id
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/ledger"),
            query_params=[
                param[str | None]("kind", kind),
                param[str | None]("subject_id", subject_id),
                param[int | None]("limit", limit),
            ],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[list[LedgerEntry]],
            error_mapper=ledger_error_mapper,
            request_options=request_options,
        )

    def ledger_verify(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[ChainVerify, LedgerVerifyErrorBody]:
        """Recompute every hash in the chain and report the first entry that no longer matches.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/ledger/verify"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[ChainVerify],
            error_mapper=ledger_verify_error_mapper,
            request_options=request_options,
        )

    def login(
        self, body: LoginBody | LoginBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Me, LoginErrorBody]:
        """Check a username and password and set a 12-hour session cookie.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/login"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[LoginBody | LoginBodyDict](body),
            decoder=json_decoder[Me],
            error_mapper=login_error_mapper,
            request_options=request_options,
        )

    def logout(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Ok, LogoutErrorBody]:
        """Clear the session cookie.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/logout"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=json_decoder[Ok],
            error_mapper=logout_error_mapper,
            request_options=request_options,
        )

    def me(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Me, MeErrorBody]:
        """Who is logged in, and whether they are the seller (dev) or a read-mostly judge.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/me"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[Me],
            error_mapper=me_error_mapper,
            request_options=request_options,
        )

    def plans_cancel(
        self, plan_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Ok, PlansCancelErrorBody]:
        """Seller cancels a planned action. Sealed in the ledger.

        Args:
            plan_id: plan_id
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/plans/{plan_id}/cancel"),
            path_params=[param[str]("plan_id", plan_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[Ok],
            error_mapper=plans_cancel_error_mapper,
            request_options=request_options,
        )

    def plans_list(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Plan], PlansListErrorBody]:
        """What the agents have scheduled: planned, done, held, blocked and cancelled actions.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/plans"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[list[Plan]],
            error_mapper=plans_list_error_mapper,
            request_options=request_options,
        )

    def plans_move(
        self, plan_id: str, body: PlanMove | PlanMoveDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Plan, PlansMoveErrorBody]:
        """Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.

        Args:
            plan_id: plan_id
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="PATCH",
            url_template=self._server.default("/api/plans/{plan_id}"),
            path_params=[param[str]("plan_id", plan_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[PlanMove | PlanMoveDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[Plan],
            error_mapper=plans_move_error_mapper,
            request_options=request_options,
        )

    def post_killswitch(
        self, body: KillSwitchBody | KillSwitchBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[KillSwitch, PostKillswitchErrorBody]:
        """Turn the kill switch on or off. While on, the gateway denies every agent action.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/killswitch"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[KillSwitchBody | KillSwitchBodyDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[KillSwitch],
            error_mapper=post_killswitch_error_mapper,
            request_options=request_options,
        )

    def runs(
        self, *, limit: int | None = 20, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[AgentRun], RunsErrorBody]:
        """Recent agent runs with their steps and structured output.

        Args:
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/runs"),
            query_params=[param[int | None]("limit", limit)],
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[list[AgentRun]],
            error_mapper=runs_error_mapper,
            request_options=request_options,
        )

    def shipments(
        self, body: ShipmentBody | ShipmentBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[ShipmentResult, ShipmentsErrorBody]:
        """Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/shipments"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[ShipmentBody | ShipmentBodyDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[ShipmentResult],
            error_mapper=shipments_error_mapper,
            request_options=request_options,
        )

    def summary(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Summary, SummaryErrorBody]:
        """Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain state.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/summary"),
            auth_scheme=self._auth.http_basic,
            decoder=json_decoder[Summary],
            error_mapper=summary_error_mapper,
            request_options=request_options,
        )


class AsyncConsoleWithRawResponse(SecuredRawResponse[AsyncRawClient, Server, AsyncAuthSchemes]):
    async def approvals(
        self, *, status: str | None = "pending", request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Approval], ApprovalsErrorBody]:
        """Agent actions the gateway held for a human decision (over the money cap).

        Args:
            status: Current status
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/approvals"),
            query_params=[param[str | None]("status", status)],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[list[Approval]],
            error_mapper=approvals_error_mapper,
            request_options=request_options,
        )

    async def decide_approval(
        self,
        approval_id: str,
        action: ActionOrStr,
        *,
        body: ApprovalBody | ApprovalBodyDict | None = None,
        request_options: RequestOptionsOrDict | None = None,
    ) -> ApiResult[ApprovalResult, DecideApprovalErrorBody]:
        """Approve (the gateway then executes the held action) or reject it. Both are sealed.

        Args:
            approval_id: Id of the pending approval for this action
            action: approve or reject
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/approvals/{approval_id}/{action}"),
            path_params=[param[str]("approval_id", approval_id), param[ActionOrStr]("action", action)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[ApprovalBody | ApprovalBodyDict | None](body),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[ApprovalResult],
            error_mapper=decide_approval_error_mapper,
            request_options=request_options,
        )

    async def dispute_detail(
        self, dispute_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[DisputeDetail, DisputeDetailErrorBody]:
        """One dispute with Defender's evidence pack and the pending approval to submit it.

        Args:
            dispute_id: PayPal dispute id, e.g. PP-D-12345
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/disputes/{dispute_id}"),
            path_params=[param[str]("dispute_id", dispute_id)],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[DisputeDetail],
            error_mapper=dispute_detail_error_mapper,
            request_options=request_options,
        )

    async def disputes(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Dispute], DisputesErrorBody]:
        """Latest state of every PayPal dispute, newest first.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/disputes"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[list[Dispute]],
            error_mapper=disputes_error_mapper,
            request_options=request_options,
        )

    async def get_killswitch(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[KillSwitch, GetKillswitchErrorBody]:
        """Is the kill switch on?

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/killswitch"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[KillSwitch],
            error_mapper=get_killswitch_error_mapper,
            request_options=request_options,
        )

    async def health(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Health, HealthErrorBody]:
        """Score and factors are recomputed from the ledger on every call, so a dispute that arrived after Guardian's
        last run still counts. Guardian's AI recommendations are reused only while the factors they were written for
        still hold.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/health"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[Health],
            error_mapper=health_error_mapper,
            request_options=request_options,
        )

    async def inbox(
        self, body: InboxEmail | InboxEmailDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[InboxVerdict, InboxErrorBody]:
        """Run Sentinel inline (a few seconds) so the console gets the verdict in one call.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/inbox"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[InboxEmail | InboxEmailDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[InboxVerdict],
            error_mapper=inbox_error_mapper,
            request_options=request_options,
        )

    async def invoices(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Invoice], InvoicesErrorBody]:
        """Invoices with paid/overdue status, risk, shipment and PayPal payment link.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/invoices"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[list[Invoice]],
            error_mapper=invoices_error_mapper,
            request_options=request_options,
        )

    async def ledger(
        self,
        *,
        kind: str | None = None,
        subject_id: str | None = None,
        limit: int | None = 100,
        request_options: RequestOptionsOrDict | None = None,
    ) -> ApiResult[list[LedgerEntry], LedgerErrorBody]:
        """Proof Ledger entries, newest first. Each entry's hash covers the previous one.

        Args:
            kind: Entry kind: event, decision, agent_step, approval or note
            subject_id: What this is about: an invoice, dispute or email id
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/ledger"),
            query_params=[
                param[str | None]("kind", kind),
                param[str | None]("subject_id", subject_id),
                param[int | None]("limit", limit),
            ],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[list[LedgerEntry]],
            error_mapper=ledger_error_mapper,
            request_options=request_options,
        )

    async def ledger_verify(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[ChainVerify, LedgerVerifyErrorBody]:
        """Recompute every hash in the chain and report the first entry that no longer matches.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/ledger/verify"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[ChainVerify],
            error_mapper=ledger_verify_error_mapper,
            request_options=request_options,
        )

    async def login(
        self, body: LoginBody | LoginBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Me, LoginErrorBody]:
        """Check a username and password and set a 12-hour session cookie.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/login"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[LoginBody | LoginBodyDict](body),
            decoder=async_json_decoder[Me],
            error_mapper=login_error_mapper,
            request_options=request_options,
        )

    async def logout(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Ok, LogoutErrorBody]:
        """Clear the session cookie.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/logout"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Ok],
            error_mapper=logout_error_mapper,
            request_options=request_options,
        )

    async def me(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Me, MeErrorBody]:
        """Who is logged in, and whether they are the seller (dev) or a read-mostly judge.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/me"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[Me],
            error_mapper=me_error_mapper,
            request_options=request_options,
        )

    async def plans_cancel(
        self, plan_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Ok, PlansCancelErrorBody]:
        """Seller cancels a planned action. Sealed in the ledger.

        Args:
            plan_id: plan_id
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/plans/{plan_id}/cancel"),
            path_params=[param[str]("plan_id", plan_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[Ok],
            error_mapper=plans_cancel_error_mapper,
            request_options=request_options,
        )

    async def plans_list(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[Plan], PlansListErrorBody]:
        """What the agents have scheduled: planned, done, held, blocked and cancelled actions.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/plans"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[list[Plan]],
            error_mapper=plans_list_error_mapper,
            request_options=request_options,
        )

    async def plans_move(
        self, plan_id: str, body: PlanMove | PlanMoveDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Plan, PlansMoveErrorBody]:
        """Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.

        Args:
            plan_id: plan_id
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="PATCH",
            url_template=self._server.default("/api/plans/{plan_id}"),
            path_params=[param[str]("plan_id", plan_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[PlanMove | PlanMoveDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[Plan],
            error_mapper=plans_move_error_mapper,
            request_options=request_options,
        )

    async def post_killswitch(
        self, body: KillSwitchBody | KillSwitchBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[KillSwitch, PostKillswitchErrorBody]:
        """Turn the kill switch on or off. While on, the gateway denies every agent action.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/killswitch"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[KillSwitchBody | KillSwitchBodyDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[KillSwitch],
            error_mapper=post_killswitch_error_mapper,
            request_options=request_options,
        )

    async def runs(
        self, *, limit: int | None = 20, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[list[AgentRun], RunsErrorBody]:
        """Recent agent runs with their steps and structured output.

        Args:
            limit: Maximum number of items to return
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/runs"),
            query_params=[param[int | None]("limit", limit)],
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[list[AgentRun]],
            error_mapper=runs_error_mapper,
            request_options=request_options,
        )

    async def shipments(
        self, body: ShipmentBody | ShipmentBodyDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[ShipmentResult, ShipmentsErrorBody]:
        """Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/shipments"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[ShipmentBody | ShipmentBodyDict](body),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[ShipmentResult],
            error_mapper=shipments_error_mapper,
            request_options=request_options,
        )

    async def summary(
        self, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Summary, SummaryErrorBody]:
        """Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain state.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/summary"),
            auth_scheme=self._auth.http_basic,
            decoder=async_json_decoder[Summary],
            error_mapper=summary_error_mapper,
            request_options=request_options,
        )
