#!/usr/bin/env sh
# Prompt Refine — hook gate (POSIX).
# Emits the refine reminder ONLY when the toggle flag `.refine-active` exists.
# This is what makes `/refine off` real: removing the flag stops enforcement.
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
[ -f "$DIR/.refine-active" ] && cat "$DIR/reminder.txt"
exit 0
