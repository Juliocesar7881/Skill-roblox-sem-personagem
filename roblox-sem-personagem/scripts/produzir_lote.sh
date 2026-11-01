#!/bin/bash
# Records, edits and renders the Shorts in order (one line per project start/end), via fazer_short.py (lint, audit,
# record, edit, render). Skips projects that already have final-*/*.mp4 unless FORCAR=1. Touches LOTE/heartbeat
# so a scheduled continuation knows a session is still working.
# Usage (from anywhere): bash produzir_lote.sh LOTE_DIR/NN-project [LOTE_DIR/NN-project ...]
FS="$(dirname "$(readlink -f "$0")")/fazer_short.py"
for p in "$@"; do
  p=${p%/}
  touch "$(dirname "$p")/heartbeat" 2>/dev/null
  if [ -z "$FORCAR" ] && ls "$p"/final-*/*.mp4 >/dev/null 2>&1; then echo "SKIP $p (already rendered)"; continue; fi
  echo "START $p $(date +%H:%M)"
  if PYTHONIOENCODING=utf-8 python "$FS" "$p" > "$p/producao.log" 2>&1; then
    echo "OK $p $(date +%H:%M)"
  else
    echo "FAIL $p $(date +%H:%M): $(grep -v '^\s*$' "$p/producao.log" | tail -2 | tr '\n' ' ' | cut -c1-300)"
  fi
  touch "$(dirname "$p")/heartbeat" 2>/dev/null
done
echo "DONE $(date +%H:%M)"
