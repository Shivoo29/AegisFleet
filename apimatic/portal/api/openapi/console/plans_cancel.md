# Plans Cancel (/docs/api/openapi/console/plans_cancel)

`POST /api/plans/{plan_id}/cancel`

Seller cancels a planned action. Sealed in the ledger.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/plans/{plan_id}/cancel:
    post:
      tags:
        - console
      summary: Plans Cancel
      description: Seller cancels a planned action. Sealed in the ledger.
      operationId: plans_cancel
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
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Ok"
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
                  var response = await client.ConsoleApi.PlansCancel(
                      new PlansCancelRequest
                      {
                          PlanId = "some example string",
                      });
                  // TODO: Handle 'response' of type Ok
              }
              catch (ApiException<PlansCancelError> ex)
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
                  response = client.console.plans_cancel(
                      "some example string"
                  )
                  # TODO: Handle 'response' of type Ok
              except ApiError as e:
                  # TODO: Handle 'e.error' of type PlansCancelErrorBody
                  ...
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.plansCancel({
                  planId: "some example string",
                });
                // TODO: Handle 'response' of type Ok
              } catch (err) {
                // TODO: Handle 'err' of type Console.PlansCancelError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Ok:
      properties:
        ok:
          type: boolean
          description: True on success
      type: object
      required:
        - ok
      title: Ok
      description: Ok object
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