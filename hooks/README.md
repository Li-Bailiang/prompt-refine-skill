# Optional: hard session enforcement with a real on/off toggle (Claude Code)

By default, Prompt Refine is **conversation-scoped best-effort** — it keeps refining while
the activation stays in context, which is portable across every tool. On a long, compacted
conversation that can lapse until you re-run `/prompt-refine`.

If you're on **Claude Code** and want refine mode enforced on every turn, add a
`UserPromptSubmit` hook. Unlike a naive "always-on" hook, this setup is **gated by a
toggle flag file**, so `/refine off` genuinely turns it off.

> ⚠️ Hooks are a **Claude Code** feature (configured in `settings.json`). Other tools
> ignore this; there, rely on re-invoking `/prompt-refine`.

## How it works

```
user prompt ─▶ UserPromptSubmit hook ─▶ refine-gate(.sh/.ps1)
                                              │
                    .refine-active exists? ──┤── yes ─▶ prints reminder.txt ─▶ injected as context
                                              └── no  ─▶ prints nothing ─▶ normal behavior
```

- [`refine-gate.sh`](refine-gate.sh) / [`refine-gate.ps1`](refine-gate.ps1) emit
  [`reminder.txt`](reminder.txt) **only when** the flag file `.refine-active` exists.
- **Enabling** = create the flag. **Disabling** (`/refine off`) = remove the flag.
- The flag is local state and is git-ignored.

## 1. Register the hook

Add to `.claude/settings.json` (project) or `~/.claude/settings.json` (global). Adjust the
path if you installed the skill elsewhere.

**macOS / Linux:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command",
        "command": "sh .claude/skills/prompt-refine/hooks/refine-gate.sh" } ] }
    ]
  }
}
```

**Windows (PowerShell):**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command",
        "command": "powershell -NoProfile -File .claude/skills/prompt-refine/hooks/refine-gate.ps1" } ] }
    ]
  }
}
```

## 2. Toggle it on / off

Create or delete the flag file `hooks/.refine-active`:

| | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| **On** | `touch .claude/skills/prompt-refine/hooks/.refine-active` | `New-Item -ItemType File .claude/skills/prompt-refine/hooks/.refine-active` |
| **Off** | `rm .claude/skills/prompt-refine/hooks/.refine-active` | `Remove-Item .claude/skills/prompt-refine/hooks/.refine-active` |

If the agent has shell access, you can let it manage the flag: on `/prompt-refine` it
creates the flag, on `/refine off` it deletes it — so the chat commands and the hook stay
in sync. Otherwise toggle manually with the commands above.

## Why a flag instead of always-on

An ungated always-on hook re-injects "refine is active" every turn, so a typed
`/refine off` can't actually stop it. Gating on `.refine-active` keeps the off switch
honest while still surviving context compaction.
