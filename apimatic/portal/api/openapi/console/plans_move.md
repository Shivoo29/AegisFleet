# Plans Move (/docs/api/openapi/console/plans_move)

`PATCH /api/plans/{plan_id}`

Seller moves a planned action to a new time (drag on the Timeline). Sealed in the ledger.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/plans/{plan_id}:
    patch:
      tags:
        - console
      summary: Plans Move
      description: Seller moves a planned action to a new time (drag on the Timeline).
        Sealed in the ledger.
      operationId: plans_move
      security:
        - HTTPBasic: []
      parameters:
        - name: plan_id
          in: path
          required: true
          schema:
            type: string
            description: Plan id
          description: plan_id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PlanMove"
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Plan"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
        "404":
          description: No planned action with this id
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
                  var response = await client.ConsoleApi.PlansMove(
                      new PlansMoveRequest
                      {
                          PlanId = "some example string",
                          Body = new PlanMove
                          {
                              DueAt = DateTimeOffset.Parse(
                                  "2024-01-15T09:30:00Z"),
                          },
                      });
                  // TODO: Handle 'response' of type Plan
              }
              catch (ApiException<PlansMoveError> ex)
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
                  response = client.console.plans_move(
                      "some example string",
                      PlanMove(
                          due_at=datetime(
                              2024, 1, 15, 9, 30, 0, tzinfo=timezone.utc
                          ),
                      ),
                  )
                  # TODO: Handle 'response' of type Plan
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type PlansMoveErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.plansMove({
                  planId: "some example string",
                  body: {
                    dueAt: new Date(Date.UTC(2024, 0, 15, 9, 30, 0)),
                  },
                });
                // TODO: Handle 'response' of type Plan
              } catch (err) {
                // TODO: Handle 'err' of type Console.PlansMoveError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    PlanMove:
      properties:
        due_at:
          type: string
          format: date-time
          description: New time to run it (ISO 8601)
      type: object
      required:
        - due_at
      title: PlanMove
      description: PlanMove object
    Plan:
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
        title:
          type: string
          description: Title
        subject_id:
          type: string
          description: "What this is about: an invoice, dispute or email id"
        due_at:
          type: string
          format: date-time
          description: Due at
        status:
          type: string
          enum:
            - planned
            - running
            - done
            - held
            - blocked
            - cancelled
          description: Current status
        outcome:
          anyOf:
            - type: object
              description: allow, hold or deny
            - type: "null"
              description: Not set
          description: allow, hold or deny
        created_at:
          type: string
          format: date-time
          description: When it was created (ISO 8601)
        updated_at:
          type: string
          format: date-time
          description: Updated at
      type: object
      required:
        - id
        - agent
        - tool
        - args
        - reason
        - title
        - subject_id
        - due_at
        - status
        - created_at
        - updated_at
      title: Plan
      description: Plan object
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