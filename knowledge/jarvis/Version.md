# Jarvis Release Versions

## Current Release
- **Version**: 0.1.0-beta.1
- **Release Status**: Product Baseline Beta
- **Effective**: 2026-08-04

## Version History
- **v0.1.0-beta.1**: Established Product Baseline. Built WorkspaceShell, WorkspaceAssistant `resolve()` ResolverChain, and GroundingEngine.
- **v0.0.1-alpha.17**: Platform configuration and core stabilizers.
- **v0.0.1-alpha.16**: Ingestion contract definitions and checkmate tests.

## Semantic Rules
- Major version promotions reflect framework changes.
- Minor version promotions indicate new Capability Packages (CPs).
- Patch version promotions indicate bug fixing and stabilization.

## Release Hygiene Verification Gates
Prior to human check review/acceptance of any milestone version checkpoint, release check processes verify the following hygiene parameters:
1. **API Parity**: Confirming Route counts and Middleware counts remain identical.
2. **Hash Parity**: Enforcing exact hash matches on protected runtime assets.
3. **Safety Parity**: Validating workbook builder export kill switches are fully closed during all stages of preparation. *Source Code Alignment: LK_S0009*

*Lightweight Source References: LK_S0009*
