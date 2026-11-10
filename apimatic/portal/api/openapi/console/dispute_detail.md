# Dispute Detail (/docs/api/openapi/console/dispute_detail)

`GET /api/disputes/{dispute_id}`

One dispute with Defender's evidence pack and the pending approval to submit it.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/disputes/{dispute_id}:
    get:
      tags:
        - console
      summary: Dispute Detail
      description: One dispute with Defender's evidence pack and the pending approval
        to submit it.
      operationId: dispute_detail
      security:
        - HTTPBasic: []
      parameters:
        - name: dispute_id
          in: path
          required: true
          schema:
            type: string
            description: PayPal dispute id, e.g. PP-D-12345
          description: PayPal dispute id, e.g. PP-D-12345
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DisputeDetail"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
        "404":
          description: No such dispute
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
                  var response = await client.ConsoleApi.DisputeDetail(
                      new DisputeDetailRequest
                      {
                          DisputeId = "some example string",
                      });
                  // TODO: Handle 'response' of type DisputeDetail
              }
              catch (ApiException<DisputeDetailError> ex)
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
                  response = client.console.dispute_detail(
                      "some example string"
                  )
                  # TODO: Handle 'response' of type DisputeDetail
              except ApiError as e:
                  # TODO: Handle 'e.error' of type DisputeDetailErrorBody
                  ...
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.disputeDetail({
                  disputeId: "some example string",
                });
                // TODO: Handle 'response' of type DisputeDetail
              } catch (err) {
                // TODO: Handle 'err' of type Console.DisputeDetailError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    DisputeDetail:
      properties:
        dispute:
          $ref: "#/components/schemas/Dispute"
          description: The dispute
        evidence_pack:
          anyOf:
            - type: object
              description: Defender's evidence pack, every fact citing a ledger id
            - type: "null"
              description: Not set
          description: Defender's evidence pack, every fact citing a ledger id
        approval_id:
          anyOf:
            - type: string
              description: Id of the pending approval for this action
            - type: "null"
              description: Not set
          description: Id of the pending approval for this action
      type: object
      required:
        - dispute
      title: DisputeDetail
      description: DisputeDetail object
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
    Dispute:
      properties:
        id:
          type: string
          description: Unique id
        invoice_id:
          anyOf:
            - type: string
              description: Invoice id, e.g. INV-0007
            - type: "null"
              description: Not set
          description: Invoice id, e.g. INV-0007
        reason:
          type: string
          description: Why
        status:
          type: string
          description: Current status
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
        buyer_name:
          anyOf:
            - type: string
              description: Buyer's name as PayPal reports it
            - type: "null"
              description: Not set
          description: Buyer's name as PayPal reports it
        created_at:
          type: string
          format: date-time
          description: When it was created (ISO 8601)
        due_by:
          anyOf:
            - type: string
              description: Seller response deadline (ISO 8601)
            - type: "null"
              description: Not set
          description: Seller response deadline (ISO 8601)
      type: object
      required:
        - id
        - reason
        - status
        - created_at
      title: Dispute
      description: Dispute object
info:
  title: AegisFleet
  version: 1.0.0
```