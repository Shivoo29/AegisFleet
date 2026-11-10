# Approvals (/docs/api/openapi/console/approvals)

`GET /api/approvals`

Agent actions the gateway held for a human decision (over the money cap).

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/approvals:
    get:
      tags:
        - console
      summary: Approvals
      description: Agent actions the gateway held for a human decision (over the money cap).
      operationId: approvals
      security:
        - HTTPBasic: []
      parameters:
        - name: status
          in: query
          required: false
          schema:
            type: string
            default: pending
            description: Current status
          description: Current status
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Approval"
                title: Response 200 Approvals
        "401":
          description: "Login required: HTTP Basic or the session cookie"
        "422":
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.Approvals(
                      new ApprovalsRequest());
                  // TODO: Handle 'response' of type IReadOnlyList<Approval>
              }
              catch (ApiException<ApprovalsError> ex)
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
                  response = client.console.approvals()
                  # TODO: Handle 'response' of type list[Approval]
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type ApprovalsErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.approvals();
                // TODO: Handle 'response' of type Approval[]
              } catch (err) {
                // TODO: Handle 'err' of type Console.ApprovalsError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Approval:
      properties:
        id:
          type: string
          description: Unique id
        agent:
          type: string
          description: "Agent name: sentinel, defender, guardian or collector"
        tool:
          type: string
          description: Gateway tool the agent called
        args:
          type: object
          description: Tool arguments the agent asked the gateway to run
        reason:
          type: string
          description: Why
        summary:
          anyOf:
            - type: string
              description: One-line summary
            - type: "null"
              description: Not set
          description: One-line summary
        amount_cents:
          anyOf:
            - type: integer
              description: Amount in minor units (cents)
            - type: "null"
              description: Not set
          description: Amount in minor units (cents)
        currency:
          anyOf:
            - type: string
              description: ISO 4217 currency code
            - type: "null"
              description: Not set
          description: ISO 4217 currency code
        status:
          type: string
          enum:
            - pending
            - approved
            - rejected
          description: Current status
        created_at:
          type: string
          format: date-time
          description: When it was created (ISO 8601)
      type: object
      required:
        - id
        - agent
        - tool
        - args
        - reason
        - status
        - created_at
      title: Approval
      description: Approval object
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: "#/components/schemas/ValidationError"
          type: array
          description: Validation errors
      type: object
      title: HTTPValidationError
      description: HTTPValidationError object
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          description: Where the invalid value is
        msg:
          type: string
          description: Error message
        type:
          type: string
          description: Error type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
      description: ValidationError object
info:
  title: AegisFleet
  version: 1.0.0
```