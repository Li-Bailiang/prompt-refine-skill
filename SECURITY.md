# Security Policy

Prompt Refine is a single, plain-Markdown Agent Skill. It has **no runtime, no
dependencies, and makes no network calls on its own**. The only executable artifact is one
**optional, opt-in** shell hook under `hooks/`, gated by a `.refine-active` flag.

## Supported Versions

Only the latest released version receives fixes.

| Version | Supported |
| ------- | --------- |
| 2.2.x   | ✅        |
| < 2.2   | ❌        |

## Reporting a Vulnerability

Please report security issues **privately — do not open a public issue**.

- **Preferred:** use GitHub's **"Report a vulnerability"** button under this repository's
  **Security** tab (private security advisory). This opens a confidential channel with the
  maintainer.
- **Alternative:** contact the maintainer [@Li-Bailiang](https://github.com/Li-Bailiang)
  directly on GitHub.

Please include the affected file(s), a description of the issue, and steps to reproduce.
You can expect an initial response within a few days, and a status update as the report is
triaged.

## Scope

Because the skill ships only Markdown instructions plus one optional hook, the most
relevant concerns are:

- the optional `hooks/` script (only runs if you install and enable it);
- instruction content that could cause a host agent to behave in an unintended or unsafe
  way.

Reports about either are welcome. General prompt-quality feedback is **not** a security
issue — please open a normal issue or pull request for that.
