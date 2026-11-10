import type { BasicAuthCredentials } from "./core/auth/credentials.js";
import type { CoreClientOptions } from "./core/client-options.js";

export type ClientOptions = SdkClientOptions & CoreClientOptions;

type SdkClientOptions = ServerOptions & {
  readonly httpBasic?: BasicAuthCredentials | undefined;
};

type ServerOptions = {
  /** Live demo (PayPal sandbox) */
  readonly serverOptions?: {
    baseUrl?: string;
  };
};
