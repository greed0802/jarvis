# Object: Project

Category:
Core / Workspace

Definition:

A Project is the permanent source of truth for a body of work.

It represents all engineering data, documents, configurations, history, and outputs related to a single real-world project.

Unlike a Workspace, which represents an active working session, a Project exists independently of users, devices, and sessions.

Projects are designed to be portable, versionable, referenceable, and shareable while preserving the integrity of their data.

---

Owner

User
Organization (Future)

---

Purpose

The Project serves as the permanent database for all information related to one engineering project.

Everything that represents long-term knowledge or work belongs to the Project.

The Workspace merely interacts with it.

---

Project Owns

• Drawings

• BOQs

• Workbooks

• Reports

• Cost Databases

• Rate Libraries

• Formula Libraries

• Project Notes

• Project Knowledge

• Outputs

• Versions

• Snapshots

• Attachments

• Metadata

• AI Artifacts

• History

---

Project Does NOT Own

• Current Conversation

• Open Windows

• Current Workflow State

• User Interface Layout

• Active AI Context

• Temporary Memory

• Temporary Cache

Those belong to the Workspace.

---

Relationship with Workspace

A Project may have multiple Workspaces.

Example

Project ABC

├── Estimating Workspace

├── QA Workspace

├── Review Workspace

├── Coding Workspace

└── Site Coordination Workspace

Each Workspace represents a different active context while sharing the same Project data.

---

Reference Projects

Projects may reference other Projects.

Reference Projects are always read-only unless explicitly promoted.

Reference Projects are intended for:

• Previous tenders

• Historical pricing

• Similar projects

• Lessons learned

• Engineering references

Referenced data never automatically overrides Project data.

Whenever conflicts occur, Jarvis asks the user for confirmation.

---

Portability

Projects should be fully portable.

A Project should be exportable into a single package.

Example:

Project.jarvisproject

The package should contain:

• Project Database

• Documents

• Drawings

• BOQs

• Resources

• Knowledge

• History

• Metadata

User-specific settings are excluded unless explicitly requested.

---

Jarvis Viewer

Projects should be viewable without the full Jarvis application.

Jarvis Viewer provides:

• Read-only viewing

• Navigation

• Searching

• Drawing viewing

• BOQ viewing

• Reports

• Attachments

Editing requires the full Jarvis application and appropriate permissions.

---

Synchronization

Projects should synchronize across:

• Desktop

• Laptop

• NAS

• Nextcloud

• Cloud

Synchronization should preserve:

• Version History

• Snapshots

• References

• Metadata

• Permissions

---

States

• Created

• Active

• Synced

• Archived

• Read Only

• Locked

• Restoring

• Deleted

---

Events

• Project Created

• Project Imported

• Project Exported

• Project Saved

• Project Synced

• Project Archived

• Project Restored

• Project Shared

• Project Locked

• Project Deleted

---

Relationships

User
owns
Project

Project
contains
Engineering Data

Project
contains
Knowledge

Project
contains
Resources

Project
contains
Versions

Project
creates
Workspaces

Workspace
uses
Project

Project
references
Projects