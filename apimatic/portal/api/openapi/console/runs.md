# Runs (/docs/api/openapi/console/runs)

`GET /api/runs`

Recent agent runs with their steps and structured output.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/runs:
    get:
      tags:
        - console
      summary: Runs
      description: Recent agent runs with their steps and structured output.
      operationId: runs
      security:
        - HTTPBasic: []
      parameters:
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            default: 20
            description: Maximum number of items to return
          description: Maximum number of items to return
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/AgentRun"
                title: Response 200 Runs
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
                  var response = await client.ConsoleApi.Runs(
                      new RunsRequest());
                  // TODO: Handle 'response' of type IReadOnlyList<AgentRun>
              }
              catch (ApiException<RunsError> ex)
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
                  response = client.console.runs()
                  # TODO: Handle 'response' of type list[AgentRun]
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RunsErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.runs();
                // TODO: Handle 'response' of type AgentRun[]
              } catch (err) {
                // TODO: Handle 'err' of type Console.RunsError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    AgentRun:
      properties:
        id:
          type: string
          description: Unique id
        agent:
          type: string
          description: "Agent name: sentinel, defender, guardian or collector"
        event_type:
          type: string
          description: Event that started the run, e.g. dispute.created
        status:
          type: string
          description: Current status
        steps:
          items: {}
          type: array
          description: Each step the agent took
        output:
          anyOf:
            - type: object
              description: Agent's structured result
            - type: "null"
              description: Not set
          description: Agent's structured result
        started_at:
          type: string
          format: date-time
          description: When the run started (ISO 8601)
      type: object
      required:
        - id
        - agent
        - event_type
        - status
        - steps
        - started_at
      title: AgentRun
      description: AgentRun object
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