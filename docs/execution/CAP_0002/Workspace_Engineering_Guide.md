# Workspace Engineering Guide

- Do not add methods that mutate state. Use `replace()` or factory methods.
- IDs should be strings, ideally UUIDs.
- Validation happens strictly in `__post_init__`.
- Use `jarvis.domain` imports strictly downstream.
