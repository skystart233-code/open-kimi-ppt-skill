# Security policy

## Supported version

Security fixes are applied to the current `main` branch. No older release line
is currently maintained.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting feature for this repository when
available. If private reporting is unavailable, open an issue containing only
a minimal description and request a private contact channel; do not publish
credentials, private documents, or a working exploit.

## Security model

- The local server listens on `127.0.0.1` by default.
- PPTD projects are processed locally by the bundled runtime.
- The browser reads or writes a project directory only after user selection.
- A presentation may still request remote images or fonts from URLs contained
  in that presentation.
- Generated PPTD, PPTX, and downloaded media are untrusted files and should be
  reviewed before sharing or opening in privileged environments.
