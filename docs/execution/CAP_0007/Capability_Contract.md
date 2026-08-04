# Capability Contract

## Immutable Attributes
Capabilities must expose:
- `capability_id`
- `name`
- `version`
- `input_schema`
- `output_schema`

## Lifecycle
Capabilities self-register into the `CapabilityRegistry`.
The `CapabilityRuntime` executes them dynamically passing `ExecutionContext`.
