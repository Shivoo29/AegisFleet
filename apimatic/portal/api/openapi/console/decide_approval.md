# Decide Approval (/docs/api/openapi/console/decide_approval)

`POST /api/approvals/{approval_id}/{action}`

Approve (the gateway then executes the held action) or reject it. Both are sealed.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/approvals/{approval_id}/{action}:
    post:
      tags:
        - console
      summary: Decide Approval
      description: Approve (the gateway then executes the held action) or reject it.
        Both are sealed.
      operationId: decide_approval
      security:
        - HTTPBasic: []
      parameters:
        - name: approval_id
          in: path
          required: true
          schema:
            type: string
            description: Id of the pending approval for this action
          description: Id of the pending approval for this action
        - name: action
          in: path
          required: true
          schema:
            enum:
              - approve
              - reject
            type: string
            description: approve or reject
          description: approve or reject
      requestBody:
        content:
          application/json:
            schema:
              anyOf:
                - $ref: "#/components/schemas/ApprovalBody"
                - type: "null"
              title: Body
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ApprovalResult"
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
                  var response = await client.ConsoleApi.DecideApproval(
                      new DecideApprovalRequest
                      {
                          ApprovalId = "some example string",
                          Action = ActionEnum.Approve,
                      });
                  // TODO: Handle 'response' of type ApprovalResult
              }
              catch (ApiException<DecideApprovalError> ex)
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
                  response = client.console.decide_approval(
                      "some example string", Action.APPROVE
                  )
                  # TODO: Handle 'response' of type ApprovalResult
              except ApiError as e:
                  # TODO: Handle 'e.error' of type DecideApprovalErrorBody
                  ...
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.decideApproval({
                  approvalId: "some example string",
                  action: Action.Approve,
                });
                // TODO: Handle 'response' of type ApprovalResult
              } catch (err) {
                // TODO: Handle 'err' of type Console.DecideApprovalError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    ApprovalBody:
      properties:
        note:
          type: string
          description: Optional reason, sealed into the ledger with the decision
          default: ""
      type: object
      title: ApprovalBody
      description: ApprovalBody object
    ApprovalResult:
      properties:
        status:
          type: string
          enum:
            - approved
            - rejected
          description: Current status
        decision:
          anyOf:
            - $ref: "#/components/schemas/Decision"
              description: Gateway decision for the executed action
            - type: "null"
              description: Not set
          description: Gateway decision for the executed action
      type: object
      required:
        - status
      title: ApprovalResult
      description: ApprovalResult object
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
    Decision:
      properties:
        outcome:
          type: string
          enum:
            - allow
            - hold
            - deny
          description: allow, hold or deny
        reason:
          type: string
          description: Why
        approval_id:
          anyOf:
            - type: string
              description: Id of the pending approval for this action
            - type: "null"
              description: Not set
          description: Id of the pending approval for this action
        result:
          anyOf:
            - type: object
              description: What the executed tool returned
            - type: "null"
              description: Not set
          description: What the executed tool returned
        ledger_entry_id:
          type: integer
          description: Ledger entry that seals this
      type: object
      required:
        - outcome
        - reason
        - ledger_entry_id
      title: Decision
      description: Decision object
info:
  title: AegisFleet
  version: 1.0.0
```