# C# SDK (/docs/sdks/csharp)

[Download SDK](/docs/__downloads/sdk/csharp.zip)

## Intro [#intro]

The AegisFleet SDK provides access to the AegisFleet REST APIs.

Seller console API for AegisFleet: AI agents that guard a PayPal seller's payments, disputes, invoices and shipments. Agents never call PayPal directly; every action passes a guardrail gateway (kill switch, allowlist, caps, human approval) and is sealed into a hash-chained Proof Ledger.

Authenticate with HTTP Basic (`dev` or `judge`) or the session cookie set by `POST /api/login`.

## Installation [#installation]

Add the SDK as a project reference into your solution:

```bash
dotnet add reference <path-to-sdk>/src/AegisFleet/AegisFleet.csproj
```

The project takes its build settings from the files around it, so reference it in place.

## Quick Start [#quick-start]

### Dependency Injection [#dependency-injection]

Register the client with `IServiceCollection` and resolve it from the container. The `HttpClient` is managed by `IHttpClientFactory`. Configure the client's behavior through `AegisFleetClientOptions`.

```csharp
services.AddAegisFleetClient(options =>
{
    options.HttpBasic = new BasicAuthCredentials { Username = "YOUR_USERNAME", Password = "YOUR_PASSWORD" };
    options.Environment = ServerEnvironment.Production;
    // TODO: configure more client options here
});
```

### Direct Instantiation [#direct-instantiation]

Create the client by passing an `HttpClient` you manage yourself. Configure the client's behavior through `AegisFleetClientOptions`.

```csharp
var httpClient = new HttpClient();
// TODO: configure more client options here
var options = new AegisFleetClientOptions
{
    HttpBasic = new BasicAuthCredentials { Username = "YOUR_USERNAME", Password = "YOUR_PASSWORD" },
    Environment = ServerEnvironment.Production,
};
var client = new AegisFleetClient(httpClient, options);
```