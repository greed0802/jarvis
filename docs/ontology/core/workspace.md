# Object: Workspace

Category:
Core / Workspace

Definition:

A Workspace is the active engineering environment for a single project.

It represents everything required to perform work on that project, including its current state, context, memory, resources, workflow progress, user preferences, and open tools.

A Workspace is temporary while active but can be saved, synchronized, restored, and resumed across devices.

A Workspace does not own plugins or global platform resources. Those belong to the User.

---

Owner

User

---

Contains

- One Project
- Project Context
- Workspace Memory
- Active Tasks
- Open Resources
- Active Drawings
- Active Workbooks
- Active Conversations
- AI Session
- Workflow State
- Temporary Files
- Auto-save State
- Workspace Settings

---

Can Reference

- Other Projects
- Knowledge Base
- Engineering Standards
- Rate Libraries
- Company Templates
- User Memory

Referenced information should never automatically become the source of truth.

Whenever conflicting information exists, Jarvis should request confirmation from the user.

---

Does NOT Own

- Plugins
- Skills
- User Account
- Global Settings
- Licenses
- System Resources

These belong to the User or the Platform.

---

Settings

Workspace settings override global defaults but never permanently modify them unless explicitly requested.

Examples include:

- Measurement Units
- Active Standards
- Cost Database
- AI Behaviour
- Formatting Rules
- Default Output Folder

---

Memory

Every Workspace has its own isolated memory.

Workspace Memory includes:

- Current conversation
- Decisions made
- Assumptions
- Engineering notes
- Active workflow state
- Temporary knowledge

Workspace Memory may reference User Knowledge but remains independent from it.

---

Synchronization

A Workspace should support synchronization across multiple devices.

Synchronization includes:

- Current progress
- Open resources
- Active tasks
- Workspace memory
- Layout
- Auto-save state

---

Recovery

A Workspace should support:

- Auto-save
- Manual save
- Backup
- Snapshot
- Restore
- Version History
- Crash Recovery

Recovery should minimize loss of engineering work.

---

States

- Creating
- Loading
- Active
- Idle
- Syncing
- Saving
- Restoring
- Archived
- Closed

---

Events

- Workspace Created
- Workspace Opened
- Workspace Saved
- Workspace Auto-Saved
- Workspace Synced
- Workspace Closed
- Workspace Archived
- Workspace Restored
- Workspace Crashed
- Workspace Recovered

---

Relationships

User
owns
Workspace

Workspace
contains
Project

Workspace
uses
Knowledge

Workspace
uses
Resources

Workspace
creates
Tasks

Workspace
coordinates
Workflows