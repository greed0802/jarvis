# Object: Capability

Category:
Core / Platform

---

# Definition

A Capability represents a standardized function that Jarvis can perform.

Capabilities define **what** can be accomplished.

They never define **how** it is accomplished.

The implementation is provided by one or more Skills.

Capabilities act as contracts between the Planner, Workflow Engine, and Skills.

---

# Purpose

Capabilities decouple planning from implementation.

The Planner should never know which Skill performs a task.

Instead, it requests the required Capability.

The Capability Registry identifies the most appropriate Skill to fulfill that request.

---

# Capability Answers

"What can be done?"

Not

"How is it done?"

---

# Examples

Engineering

• Build BOQ

• Generate Formula

• Validate Formula

• Compare BOQs

• Generate Description

• QA Check

---

Documents

• Read Excel

• Write Excel

• Read PDF

• OCR Image

• Generate Report

---

Development

• Execute Python

• Execute SQL

• Read Git Repository

• Run Tests

---

Artificial Intelligence

• Summarize

• Translate

• Reason

• Plan

• Explain

• Research

---

Automation

• Send Email

• Schedule Task

• Notify User

• Synchronize Resources

---

# Capability Does NOT

A Capability does not:

• Execute code

• Store data

• Own files

• Choose Skills

• Plan Workflows

• Remember Context

Capabilities describe available functions.

---

# Capability Provider

Every Capability is provided by one or more Skills.

Example

Capability

Read Excel

Providers

• OpenPyXL Skill

• LibreOffice Skill

• Microsoft Excel Skill

The Capability Registry determines which provider should execute.

---

# Capability Registry

Capabilities are registered when Skills are installed.

The Registry maintains:

• Name

• Description

• Version

• Provider

• Requirements

• Dependencies

• Permissions

• Confidence

• Availability

---

# Capability Requirements

A Capability may require:

• Resources

• Knowledge

• Context

• User Approval

• Specific Permissions

• Installed Skills

Execution cannot begin until all requirements are satisfied.

---

# Capability Lifecycle

Registered

↓

Available

↓

Selected

↓

Executing

↓

Completed

or

Unavailable

or

Failed

---

# Relationships

Planner

requests

Capability

Workflow

uses

Capability

Capability

provided by

Skill

Capability

requires

Resources

Capability

uses

Knowledge

Capability

operates within

Context

Capability

produces

Result

---

# Guiding Principle

Capabilities define what Jarvis can do.

Skills define how Jarvis performs it.

The Planner decides when it should happen.

The Workflow decides the execution order.

The Capability Registry decides who performs it.