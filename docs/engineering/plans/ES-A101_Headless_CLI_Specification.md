# ES-A101: Headless CLI Command Specification

**Status:** Active
**Date:** 2026-07-30
**Paired Plan:** EP-A101
**Evidence:** EV-A101
**Owner:** Product Engineering

---

## 1. CLI Interface

```
jarvis [global_options] <command> [command_options]
jarvis --version
jarvis --help
```

### Global Options
- `--version` — Show platform, presentation, evaluation, and CLI milestone versions
- `--help` — Show help and subcommand list

---

## 2. Commands

### 2.1 `jarvis workbench`
Run workbench pipeline headlessly.
```
jarvis workbench run [--project <path>] [--format text|json|markdown]
```
Exit codes: 0 (success), 5 (project load/execution failure), 1 (internal error)

### 2.2 `jarvis eval`
Execute evaluation profile against platform state.
```
jarvis eval --profile smoke|regression|release|research [--format text|json|markdown]
```
Exit codes: 0 (gates passed), 3 (gates failed), 4 (dataset invalid), 1 (internal error)

### 2.3 `jarvis datasets`
List golden datasets, validate case structure.
```
jarvis datasets list
```
Exit codes: 0 (success), 4 (invalid dataset), 1 (internal error)

### 2.4 `jarvis report`
Export evaluation report from a previous run.
```
jarvis report export --format json|markdown [--output <path [default: stdout]>]
```
Exit codes: 0 (success), 1 (internal error)

### 2.5 `jarvis doctor`
Run system diagnostic and output structured report.
```
jarvis doctor [--format text|json|markdown]
```
Exit codes: 0 (HEALTHY), 1 (ERROR/DEGRADED)

---

## 3. Exit Code Mapping

| Code | Name | Meaning |
|---|---|---|
| 0 | EXIT_SUCCESS | Operation completed successfully |
| 1 | EXIT_INTERNAL_ERROR | Unhandled exception or unexpected error |
| 2 | EXIT_INVALID_ARGS | Invalid/missing arguments |
| 3 | EXIT_EVAL_GATE_FAILED | Evaluation finished but gates failed |
| 4 | EXIT_DATASET_INVALID | Dataset discovery or validation failed |
| 5 | EXIT_PROJECT_LOAD_FAILED | Evidence/project loading failed |

---

## 4. Doctor Report Sections

The `jarvis doctor` command MUST output:
- **Platform:** Version and boot status
- **Presentation:** M10.6 version + protocol status
- **Evaluation:** M11.0 version, evaluators (EVA-1..EVA-5), profiles
- **Datasets:** Gold dataset summary, baseline status
- **Python:** Runtime version, OS, path
- **Configuration:** Active flags, env vars
- **Status:** HEALTHY / DEGRADED / ERROR