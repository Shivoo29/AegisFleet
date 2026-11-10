# Health (/docs/api/openapi/console/health)

`GET /api/health`

Score and factors are recomputed from the ledger on every call, so a dispute that
arrived after Guardian's last run still counts. Guardian's AI recommendations are
reused only while the factors they were written for still hold.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/health:
    get:
      tags:
        - console
      summary: Health
      description: >-
        Score and factors are recomputed from the ledger on every call, so a
        dispute that

        arrived after Guardian's last run still counts. Guardian's AI
        recommendations are

        reused only while the factors they were written for still hold.
      operationId: health
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Health"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
      security:
        - HTTPBasic: []
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.Health();
                  // TODO: Handle 'response' of type Health
              }
              catch (ApiException<HealthError> ex)
              {
                  if (ex.Error.TryGetNoContent(out var error))
                  {
                      // TODO: Handle 'error' of type RawError
                  }
              }
        - lang: python
          label: Python
          sources:
            Example: |-
              try:
                  response = client.console.health()
                  # TODO: Handle 'response' of type Health
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type HealthErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.health();
                // TODO: Handle 'response' of type Health
              } catch (err) {
                // TODO: Handle 'err' of type Console.HealthError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Health:
      properties:
        score:
          type: integer
          description: Health score, 0-100
        factors:
          items:
            $ref: "#/components/schemas/HealthFactor"
          type: array
          description: What the health score is made of
        recommendations:
          items:
            type: string
          type: array
          description: Steps that would raise the score
        appeal_pack:
          anyOf:
            - type: string
              description: Draft appeal text Guardian wrote for PayPal, if the account is
                limited
            - type: "null"
              description: Not set
          description: Draft appeal text Guardian wrote for PayPal, if the account is
            limited
      type: object
      required:
        - score
        - factors
        - recommendations
      title: Health
      description: Health object
    HealthFactor:
      properties:
        name:
          type: string
          description: Factor name
        value:
          description: Measured value
        impact:
          type: string
          description: How this factor moves the score
        note:
          type: string
          description: Free-text note
      type: object
      required:
        - name
        - value
        - impact
        - note
      title: HealthFactor
      description: HealthFactor object
info:
  title: AegisFleet
  version: 1.0.0
```