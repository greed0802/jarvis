# Object: Skill

Category:
Core / Platform

---

# Purpose

Skills provide Jarvis with modular, reusable, and extensible abilities to accomplish work.

A Skill encapsulates the implementation of one or more Capabilities while remaining independent of planning, workflow orchestration, and user interaction.

Skills allow Jarvis to continuously grow by acquiring new abilities without requiring modifications to the Platform Kernel.

---

# Guiding Principle

Skill answers the question:

> **"What can Jarvis do, and how can those abilities be extended?"**

---

# Guiding Philosophy

Skills are Jarvis's abilities.

Just as a craftsman selects the appropriate tool for a task, Jarvis equips the most suitable Skill to accomplish a user's objective.

Skills are modular, reusable, replaceable, and continuously expandable.

Jarvis should never impose an artificial limit on the number of Skills or Capabilities it can acquire.

Every new Skill increases Jarvis's usefulness without requiring changes to the Platform Kernel.

Skills never decide when they execute.

They simply provide abilities.

The Planner decides **what** should be done.

The Workflow decides **when** and **how** it should be executed.

The Skill is responsible only for performing its capabilities reliably, securely, and consistently.

---

# Definition

A Skill is a modular software component that provides one or more Capabilities to the Jarvis Platform.

Skills implement how work is performed.

They do not determine whether work should be performed, nor do they manage execution order.

A Skill may represent anything from a simple utility to a complete engineering system.

Examples include:

- Excel Skill
- OCR Skill
- CostX Skill
- Cubit Skill
- BOQ Builder Skill
- QA Checker Skill
- Description Generator Skill
- Email Skill
- Music Skill
- Home Automation Skill

---

# Responsibilities

A Skill may:

- Provide one or more Capabilities.
- Read and write Resources.
- Consume Context.
- Use Memory and Knowledge as references.
- Request additional Capabilities through the Platform.
- Validate its own outputs.
- Return deterministic or AI-assisted results.
- Expose configurable settings.
- Declare required permissions.
- Report execution status and errors.

A Skill should perform one logical responsibility exceptionally well.

---

# Ownership

Built-in Skills belong to the Jarvis Platform.

Users and Organizations may:

- Install Skills.
- Create custom Skills.
- Modify their own Skills.
- Disable Skills.
- Remove Skills.
- Share Skills.

Marketplace and Plugin repositories distribute verified Skills but do not own them.

Ownership follows the Jarvis hierarchy.

---

# Installation Sources

Skills may originate from:

- Built-in Platform Skills
- Marketplace
- Organization Repositories
- GitHub
- Local Folder
- Personal Skill Library
- Third-party Packages
- Future Skill Store

Jarvis should remain open to future installation sources.

---

# Capabilities

A Skill may expose one or many Capabilities.

There is no architectural limit to the number of Capabilities a Skill can provide.

Examples:

Excel Skill

- Read Workbook
- Create Workbook
- Write Workbook
- Compare Workbook
- Format Workbook
- Export Workbook

Capabilities are discovered automatically through the Capability Registry.

---

# Collaboration

Skills may collaborate with other Skills.

However, Skills should never directly depend on or invoke another Skill.

Instead, a Skill requests another Capability through the Platform.

The Platform determines which Skill should satisfy that request.

This architecture prevents circular dependencies while allowing unlimited collaboration.

---

# Configuration

Every Skill may define:

- Name
- Version
- Description
- Author
- Configuration
- Permissions
- Supported Capabilities
- Resource Requirements
- AI Support
- Compatibility
- Dependencies
- License

Configuration should remain simple and self-contained.

---

# Permissions

Skills declare every permission they require before execution.

Examples include:

- File System
- Network
- Internet
- Camera
- Microphone
- GPU
- Email
- Calendar
- Home Automation
- Cloud Storage

Sensitive permissions always require explicit user approval.

---

# Artificial Intelligence

Skills may use AI as an assistant.

AI may assist by:

- Generating suggestions.
- Improving reasoning.
- Interpreting ambiguous requests.
- Producing drafts.
- Performing semantic analysis.

The Skill remains responsible for validating the final result before returning it to the Workflow.

AI never becomes the owner of a Skill.

---

# Relationships

Skill

provides

→ Capability

Skill

consumes

→ Context

Skill

accesses

→ Resources

Skill

references

→ Memory

Skill

references

→ Knowledge

Skill

requests

→ Capabilities

Skill

returns

→ Result

---

# Lifecycle

Installed

↓

Registered

↓

Capability Discovery

↓

Configured

↓

Available

↓

Selected by Planner

↓

Executed by Workflow

↓

Result Returned

↓

Idle

↓

Updated or Removed

---

# States

- Installing
- Registered
- Available
- Disabled
- Updating
- Busy
- Waiting
- Error
- Deprecated
- Uninstalled

---

# Skill Manifest

Every Skill should provide a manifest describing itself.

Example information includes:

- Name
- Version
- Author
- Description
- Capabilities
- Permissions
- Dependencies
- Configuration
- License
- Supported Platforms
- Required Resources
- AI Support
- Compatibility

The Platform uses this information for discovery, validation, installation, updates, and dependency resolution.

---

# Skill is NOT

A Skill is not a Planner.

A Skill is not a Workflow.

A Skill is not an Engine.

A Skill is not a Project.

A Skill is not a Resource.

A Skill is not a Capability.

A Skill does not decide what to execute.

A Skill only provides the ability to perform work.

---

# Future Expansion

Future versions of Jarvis may support:

- Skill Marketplace
- Skill Bundles
- Skill Packages
- Remote Skills
- Cloud Skills
- Skill Sandboxing
- Skill Composition
- Skill Chaining
- Skill Rating
- Skill Telemetry
- Skill Version Management
- Automatic Skill Updates
- Organization Skill Libraries
- AI-generated Skills
- Community Skill Repository

---

# Architecture Notes

Skills are one of the primary extension points of the Jarvis Platform.

The Platform Kernel should remain stable while Skills evolve independently.

Whenever possible, new functionality should be implemented as a Skill rather than modifying the Platform Kernel.

This philosophy allows Jarvis to grow indefinitely while maintaining a clean, modular, and maintainable architecture.