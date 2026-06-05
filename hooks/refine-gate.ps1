# Prompt Refine — hook gate (Windows PowerShell).
# Emits the refine reminder ONLY when the toggle flag `.refine-active` exists.
# This is what makes `/refine off` real: removing the flag stops enforcement.
$dir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$flag = Join-Path $dir '.refine-active'
if (Test-Path $flag) { Get-Content (Join-Path $dir 'reminder.txt') -Raw }
