# Healthz (/docs/api/openapi/ops/healthz)

`GET /healthz`

Liveness probe for Render and the keep-alive ping. No auth.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /healthz:
    get:
      summary: Healthz
      description: Liveness probe for Render and the keep-alive ping. No auth.
      operationId: healthz
      responses:
        "200":
          description: Successful Response
          content:
            application/json:
              schema:
                type: object
                title: Response Healthz
      tags:
        - ops
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.Ops.Healthz();
                  // TODO: Handle 'response' of type object
              }
              catch (ApiException<RawError> ex)
              {
                  // TODO: Handle 'ex.Error' of type RawError
              }
        - lang: python
          label: Python
          sources:
            Example: |-
              try:
                  response = client.ops.healthz()
                  # TODO: Handle 'response' of type Any
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RawError
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.ops.healthz();
                // TODO: Handle 'response' of type Record<string, unknown>
              } catch (err) {
                // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
info:
  title: AegisFleet
  version: 1.0.0
```