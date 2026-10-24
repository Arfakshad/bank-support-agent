#!/usr/bin/env bash
# Mac / Linux launcher.  Usage:  bash run_bank_agent.sh
cd "$(dirname "$0")" || exit 1

PY=$(command -v python3 || command -v python)
[ -z "$PY" ] && { echo "Python 3.10+ install karein (python.org)."; exit 1; }

"$PY" -m pip install -q -r requirements.txt || { echo "Packages install nahi hue. Internet check karein."; exit 1; }

if [ -z "$GEMINI_API_KEY" ] && [ ! -f .env ]; then
  read -r -s -p "Apni Gemini API key paste karein: " GEMINI_API_KEY; echo
  read -r -p "Agli baar ke liye .env mein save karein? [y/N]: " SAVE
  if [ "$SAVE" = "y" ] || [ "$SAVE" = "Y" ]; then
    printf 'GEMINI_API_KEY=%s\n' "$GEMINI_API_KEY" > .env && chmod 600 .env
  fi
  export GEMINI_API_KEY
fi

(sleep 3; (xdg-open http://127.0.0.1:5000 || open http://127.0.0.1:5000) >/dev/null 2>&1) &
exec "$PY" bank_web_app.py
