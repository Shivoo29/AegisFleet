import { buildAuthSchemes, type AuthSchemes } from "./auth-schemes.js";
import type { ClientOptions } from "./client-options.js";
import { buildCoreClientOptions } from "./core/client-options.js";
import { RawClient } from "./core/raw-client.js";
import * as host from "./core/runtime-environment.js";
import * as s from "./core/validation/index.js";
import { Console } from "./resources/console.js";
import { Demo } from "./resources/demo.js";
import { Ops } from "./resources/ops.js";
import { Webhooks } from "./resources/webhooks.js";
import { buildServers, type Servers } from "./servers.js";

/**
 * Seller console API for AegisFleet: AI agents that guard a PayPal seller's payments, disputes,
 * invoices and shipments. Agents never call PayPal directly; every action passes a guardrail
 * gateway (kill switch, allowlist, caps, human approval) and is sealed into a hash-chained Proof
 * Ledger.
 *
 * Authenticate with HTTP Basic (`dev` or `judge`) or the session cookie set by `POST /api/login`.
 */
export class AegisFleetClient {
  readonly #rawClient: RawClient;
  readonly #servers: Servers;
  readonly #auth: AuthSchemes;
  #console?: Console;
  #demo?: Demo;
  #ops?: Ops;
  #webhooks?: Webhooks;

  constructor(options: ClientOptions = {}) {
    this.#rawClient = new RawClient({
      ...buildCoreClientOptions(options, "AEGIS_FLEET_CLIENT_LOG"),
      defaultHeaders: [
        { name: "User-Agent", value: "AegisFleetClient/1.0.0 TypeScript", schema: s.string() },
        { name: "X-APIMatic-Lang", value: "TypeScript", schema: s.string() },
        { name: "X-APIMatic-Package-Version", value: "1.0.0", schema: s.string() },
        { name: "X-APIMatic-Gen-Version", value: "4.0.0", schema: s.string() },
        { name: "X-APIMatic-OS", value: host.operatingSystem(), schema: s.optional(s.string()) },
        { name: "X-APIMatic-Runtime", value: host.runtimeDescription(), schema: s.optional(s.string()) },
      ],
      defaultQuery: [],
      defaultPathParams: [],
    });

    this.#servers = buildServers(options);

    this.#auth = buildAuthSchemes(options);
  }

  /**
   * Summary, Proof Ledger, approvals, agent runs, disputes, invoices, health.
   */
  get console(): Console {
    return (this.#console ??= new Console(this.#rawClient, this.#servers, this.#auth));
  }

  /**
   * One-click story beats for judges (demo mode only).
   */
  get demo(): Demo {
    return (this.#demo ??= new Demo(this.#rawClient, this.#servers, this.#auth));
  }

  /**
   * Liveness probe.
   */
  get ops(): Ops {
    return (this.#ops ??= new Ops(this.#rawClient, this.#servers));
  }

  /**
   * PayPal webhook receiver; signatures are verified with PayPal before routing.
   */
  get webhooks(): Webhooks {
    return (this.#webhooks ??= new Webhooks(this.#rawClient, this.#servers));
  }
}
