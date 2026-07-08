# Resource

Category:
Core / Foundation

## Purpose

A Resource represents any physical, digital, virtual, remote, or logical asset that Jarvis can access, reference, read, write, synchronize, monitor, or control.

Resources are independent of their storage location, provider, or current availability.

A Resource represents an identity, not merely a file.

---

## Guiding Principle

Resources answer one question:

"What is available to me?"

---

## Definition

A Resource is a permanent object representing an asset within the Jarvis ecosystem.

Resources may exist locally, remotely, virtually, or physically.

Resources remain the same object even when moved between storage providers.

Only their Provider, Location, Version, or Availability changes.

---

## Resource Types

Examples include:

- Files
- Folders
- Drawings
- PDFs
- Excel Workbooks
- Images
- Videos
- Databases
- APIs
- AI Models
- Git Repositories
- Docker Containers
- Local Applications
- Printers
- Cameras
- Microphones
- GPUs
- Home Automation Devices
- Cloud Services
- Nextcloud
- NAS
- OneDrive
- Google Drive

Future resource types can be added through plugins.

---

## Ownership

Resources may belong to:

- Global Jarvis
- Organization
- User
- Project

Resources are referenced by Workspaces.

Workspaces never own Resources.

---

## Identity

Every Resource has a permanent identity.

Changing the storage location, provider, or filename does not create a new Resource.

The Resource Identity remains unchanged.

---

## Provider

A Provider determines where the Resource is accessed.

Examples:

- Local Storage
- Nextcloud
- NAS
- OneDrive
- Google Drive
- AWS S3
- REST API
- Database

Changing Providers does not create a new Resource.

---

## Versioning

A Resource maintains its identity while supporting multiple versions.

Example:

Resource

Hospital Drawing

↓

Revision A

↓

Revision B

↓

Revision C

Jarvis recognizes these as versions of the same Resource.

---

## Relationships

A Resource may:

- Belong to a Project
- Belong to a User
- Belong to an Organization
- Be referenced by one or more Workspaces
- Be used by multiple Skills
- Be accessed by multiple Capabilities
- Be indexed by Knowledge
- Be remembered by Memory

---

## Permissions

Resources do not determine access.

The Security Engine determines whether access is permitted.

Ownership defines scope.

Permissions define accessibility.

---

## States

- Discovered
- Registered
- Available
- In Use
- Read Only
- Locked
- Synchronizing
- Archived
- Offline
- Unavailable
- Deleted

---

## Lifecycle

Created

↓

Registered

↓

Referenced

↓

Used

↓

Versioned

↓

Archived

↓

Deleted

---

## Future Expansion

Resources may eventually support:

- Live synchronization
- Distributed storage
- Automatic versioning
- Resource health monitoring
- Resource dependency graphs
- Resource streaming
- Digital twins

---

## Architecture Notes

- Resources are permanent identities.
- Providers determine where Resources live.
- Workspaces reference Resources.
- Projects own Resources.
- Security controls access.
- Resources are independent of storage technologies.