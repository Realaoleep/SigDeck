# Contributing

Small project, few rules:

- `make test` before every push - CI mirrors it.
- One topic per PR; keep diffs focused.
- Pure stdlib in `sigdeck/` is a hard rule - no new dependencies.
- RFC 8032 vectors must stay green in `tests/test_ed25519.py`.
- Commit style: `area: change` prefixes, present tense.

Security bugs: use private vulnerability reporting, see SECURITY.md.
