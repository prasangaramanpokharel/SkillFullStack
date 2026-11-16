# Generative UI Client Component Mapping Patterns

1. **State-Driven Rendering**:
   Every `toolInvocation` provides a `state` property:
   - `'call'`: The LLM decided to invoke the tool and provided arguments (`toolInvocation.args`), but execution is still running. Render an interactive skeleton or loading card.
   - `'result'`: The tool execution finished on the server and returned `toolInvocation.result`. Render the full interactive component with buttons and actions.
2. **User Interaction from Components**:
   When a user clicks "Confirm" or "Select Seat" inside a Generative UI card, use the client's `addToolResult({ toolCallId, result })` method to feed the user's action back to the LLM agent without starting a new conversation.
