# Plans List (/docs/api/openapi/console/plans_list)

`GET /api/plans`

What the agents have scheduled: planned, done, held, blocked and cancelled actions.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/plans:
    get:
      tags:
        - console
      summary: Plans List
      description: "What the agents have scheduled: planned, done, held, blocked and
        cancelled actions."
      operationId: plans_list
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                items:
                  $ref: "#/components/schemas/Plan"
                type: array
                title: Response 200 Plans List
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
                  var response = await client.ConsoleApi.PlansList();
                  // TODO: Handle 'response' of type IReadOnlyList<Plan>
              }
              catch (ApiException<PlansListError> ex)
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
                  response = client.console.plans_list()
                  # TODO: Handle 'response' of type list[Plan]
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type PlansListErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.plansList();
                // TODO: Handle 'response' of type Plan[]
              } catch (err) {
                // TODO: Handle 'err' of type Console.PlansListError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
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
info:
  title: AegisFleet
  version: 1.0.0
```