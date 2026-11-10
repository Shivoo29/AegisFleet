# Shipments (/docs/api/openapi/console/shipments)

`POST /api/shipments`

Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian).

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/shipments:
    post:
      tags:
        - console
      summary: Shipments
      description: "Seller adds tracking: store it, then fire shipment.created (sealed
        + routed to Guardian)."
      operationId: shipments
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ShipmentBody"
        required: true
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ShipmentResult"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
        "422":
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
      security:
        - HTTPBasic: []
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.Shipments(
                      new ShipmentsRequest { Body = new ShipmentBody() });
                  // TODO: Handle 'response' of type ShipmentResult
              }
              catch (ApiException<ShipmentsError> ex)
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
                  response = client.console.shipments(ShipmentBody())
                  # TODO: Handle 'response' of type ShipmentResult
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type ShipmentsErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.shipments({
                  body: {},
                });
                // TODO: Handle 'response' of type ShipmentResult
              } catch (err) {
                // TODO: Handle 'err' of type Console.ShipmentsError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    ShipmentBody:
      properties:
        invoice_id:
          anyOf:
            - type: string
              description: Invoice id, e.g. INV-0007
            - type: "null"
              description: Not set
          examples:
            - INV-0007
          description: Invoice id, e.g. INV-0007
        tracking_number:
          anyOf:
            - type: string
              description: Carrier tracking number
            - type: "null"
              description: Not set
          examples:
            - 1Z999AA10123456784
          description: Carrier tracking number
        carrier:
          type: string
          default: OTHER
          examples:
            - UPS
          description: Shipping carrier, e.g. UPS
      type: object
      title: ShipmentBody
      description: ShipmentBody object
    ShipmentResult:
      properties:
        ok:
          type: boolean
          description: True on success
        sealed:
          type: boolean
          description: True once the event is in the ledger
        run_id:
          anyOf:
            - type: string
              description: Agent run id
            - type: "null"
              description: Not set
          description: Agent run id
      type: object
      required:
        - ok
        - sealed
      title: ShipmentResult
      description: ShipmentResult object
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