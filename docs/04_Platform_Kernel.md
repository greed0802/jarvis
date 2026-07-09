# Platform Kernel

Version: 2.0

---

## Definition

The Platform Kernel is the central runtime coordinator and **Control Plane** of the Jarvis Platform.

It creates, manages, protects, and maintains the execution environment in which every component of Jarvis operates.

The Platform Kernel does **not** perform business logic, reasoning, planning, workflow execution, skill execution, or result generation. Instead, it provides the runtime ecosystem that enables Engines, Frameworks, Services, Skills, Integrations, and Intelligence to operate together as a single, coherent platform.

---

## Purpose

The Platform Kernel exists to provide a stable, secure, modular, and extensible runtime environment for the Jarvis Platform.

It coordinates the platform lifecycle, initializes platform components, provisions shared platform services, enforces platform policies, and provides the infrastructure required for every subsystem to operate safely.

---

## Scope

The Platform Kernel manages the platform itself, never the user's work.

It does not create Context, detect Intent, generate Plans, execute Workflows, execute Skills, produce Results, or learn Knowledge. Those responsibilities belong to the appropriate Engines and Frameworks.

---

## Control Plane Philosophy

The Platform Kernel represents the **Control Plane** of the Jarvis Platform.

The Control Plane manages the platform.

The Data Plane performs the work.

```text
                Jarvis Platform

        +--------------------------+
        |      Control Plane       |
        |     Platform Kernel      |
        +--------------------------+

        +--------------------------+
        |        Data Plane        |
        | Context -> Planner ->    |
        | Workflow -> Skills ->    |
        | Result                   |
        +--------------------------+
```

---

## Responsibilities

- Platform lifecycle
- Component registration
- Service registration
- Dependency resolution
- Configuration management
- Platform policy enforcement
- Security initialization
- Storage initialization
- Health monitoring

### Platform Lifecycle

The Platform Kernel manages the runtime lifecycle through a deterministic state machine:

- **UNINITIALIZED** — Initial state before any lifecycle activity begins.
- **INITIALIZING** — Transitioning from UNINITIALIZED to READY. Components are initialized in registration order.
- **READY** — All components initialized. Platform is prepared but not yet running.
- **RUNNING** — All components started. Platform is actively operating.
- **SHUTTING_DOWN** — Transitioning from RUNNING or READY to SHUTDOWN. Components are shut down in reverse order.
- **SHUTDOWN** — Terminal state. All components have been shut down.

Runtime-managed services participate in the lifecycle through the **LifecycleAware** contract, which defines three asynchronous methods:

- `initialize()` — Called once during platform startup, in registration order.
- `start()` — Called after all components are initialized, in registration order.
- `shutdown()` — Called during platform shutdown, in reverse registration order.

The LifecycleAware contract also exposes a read-only `state` property reflecting the component's current lifecycle state.

The Platform Kernel enforces state transitions. Components cannot be registered after initialization has begun. Failed initialization transitions the platform directly to SHUTDOWN. Failed startup triggers emergency shutdown of already-started components in reverse order.

### Component Management
- Engine Registration
- Framework Registration
- Skill Registration
- Plugin Registration
- Integration Registration
- Service Registration
- AI Provider Registration

### Control Plane Management
- Lifecycle Management
- Dependency Resolution
- Configuration Management
- Platform Policy Enforcement
- Permission Enforcement
- Error Recovery Coordination

### Configuration Ownership

Configuration is a **Control Plane** concept owned by the Platform Kernel.

- **Ownership**: The Platform Kernel holds the platform Configuration. The Application creates the Configuration instance and passes it to the Kernel during construction.
- **Lifetime**: Configuration exists for the entire lifetime of the platform instance. It is created during bootstrap and remains accessible through the Kernel for the platform's duration.
- **Immutability**: Configuration is immutable after construction. It is implemented as a frozen dataclass to prevent runtime modifications. This ensures deterministic behavior — platform settings cannot change during operation.
- **Scope**: Configuration contains only platform-level settings (e.g., log level). It does not contain user data, business logic, or runtime state. This follows YAGNI — only actively used fields are included.
- **The Kernel never constructs runtime components from Configuration.** Configuration informs platform behavior; the Application is responsible for component construction.

### Platform Service Provisioning
- Event Bus Provisioning
- Service Container Provisioning
- Logging Service Provisioning
- Security Service Provisioning
- Storage Service Provisioning

### Platform Protection
- Isolation
- Resource Protection
- Fault Containment
- Platform Integrity

---

## Ownership

The Platform Kernel belongs exclusively to the Jarvis Platform. Users and extensions may integrate through supported interfaces but never directly modify the Platform Kernel.

---

## Lifetime

Each Platform Instance owns exactly one Platform Kernel for its entire runtime lifecycle.

---

## Communication

The Platform Kernel provisions and configures shared communication services such as the Event Bus and Service Container.

It does not route business events itself.

---

## Extensibility

The Platform Kernel remains minimal and stable. Extensions occur through Engines, Frameworks, Services, Skills, Plugins, and Providers.

---

## Failure Management

The Platform Kernel isolates failures, preserves platform stability, coordinates recovery, requests user intervention when required, and prevents cascading failures.

---

## Relationships

The Platform Kernel hosts and coordinates the runtime environment for Core Runtime Engines, Cross-Cutting Frameworks, Core Platform Services, Skills, Plugins, Infrastructure, and External Integrations.

The Platform Kernel is created and owned by the **Application** (Composition Root). The Application constructs the Kernel, registers components, and then yields control for runtime coordination.

---

## Related Documents

- 02_System_Blueprint.md
- 03_Core_Ontology_Relationships.md
- 05_Data_Flow.md
- 06_Context_Engine.md
- 07_Planner_Engine.md
- 08_Workflow_Engine.md

---

## Information Boundaries

### Information entering the Platform Kernel

Only Control Plane information:

- Registration
- Configuration
- Dependency Resolution
- Lifecycle Events
- Health Information
- Platform Policies

### Information that never enters the Platform Kernel

- User Queries
- Intent
- Context
- Plans
- Workflows
- Tasks
- Resources
- Knowledge
- Results

These belong to the Data Plane.

---

## Golden Rule

The Platform Kernel creates the environment where work can happen.

It never performs the work itself.

---

## Guiding Principle

> **How can every part of Jarvis operate together safely, consistently, and as one platform?**
