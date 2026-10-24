"""Bank Support Agent - web chat UI with account tools.

Author: Arfakshad

Usage:
    pip install google-genai flask
    $env:GEMINI_API_KEY="your-key"
    python bank_web_app.py          then open http://127.0.0.1:5000

Demo logins (mock data in bank_db.py):  C1001 / 1234   and   C1002 / 5678
"""

import logging
import os
import sys
import uuid
from pathlib import Path

from flask import Flask, jsonify, request
from google import genai
from google.genai import errors

import bank_db
from bank_support_agent import AUTHOR, LANGUAGES, make_chat
from bank_tools import make_tools

def load_dotenv(path: Path) -> None:
    """Tiny .env reader (KEY=VALUE lines). Real environment variables win."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv(Path(__file__).parent / ".env")

if not os.environ.get("GEMINI_API_KEY"):
    sys.exit(
        "GEMINI_API_KEY set nahi hai.\n"
        "Options: (1) run_bank_agent.bat / run_bank_agent.sh use karein,\n"
        '(2) is folder mein .env file banayein:  GEMINI_API_KEY=your-key\n'
        '(3) PowerShell: $env:GEMINI_API_KEY="your-key"  phir dobara chalayein.'
    )

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

app = Flask(__name__)
client = genai.Client()
# session id -> {"chat": Chat, "customer_id": str | None, "name": str | None}
sessions: dict[str, dict] = {}
MAX_MESSAGE_CHARS = 2000

PAGE = (Path(__file__).parent / "bank_ui.html").read_text(encoding="utf-8").replace("__AUTHOR__", AUTHOR)


def get_session(session_id: str) -> dict:
    state = sessions.get(session_id)
    if state is None:
        state = sessions[session_id] = {"chat": make_chat(client), "customer_id": None, "name": None}
    return state


def rebuild_chat(state: dict) -> None:
    """Recreate the chat with the right tools for the current login state, keeping history."""
    history = state["chat"].get_history()
    customer_id = state["customer_id"]
    state["chat"] = make_chat(
        client,
        tools=make_tools(customer_id) if customer_id else None,
        customer_name=state["name"],
        history=history,
    )


@app.get("/")
def index():
    return PAGE


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    session_id = str(data.get("session") or "")
    customer_id = str(data.get("customer_id", "")).strip().upper()
    pin = str(data.get("pin", ""))
    if not session_id or not customer_id or not pin:
        return jsonify(error="Customer ID and PIN required. / المعرّف ورقم PIN مطلوبان."), 400
    try:
        name = bank_db.verify_login(customer_id, pin)
    except PermissionError:
        return jsonify(error="Account locked after too many wrong PINs. / تم قفل الحساب بعد محاولات خاطئة كثيرة."), 423
    if name is None:
        return jsonify(error="Wrong Customer ID or PIN. / المعرّف أو رقم PIN غير صحيح."), 401

    state = get_session(session_id)
    state["customer_id"], state["name"] = customer_id, name
    rebuild_chat(state)
    return jsonify(name=name)


@app.post("/logout")
def logout():
    data = request.get_json(silent=True) or {}
    state = sessions.get(str(data.get("session") or ""))
    if state:
        state["customer_id"], state["name"] = None, None
        rebuild_chat(state)
    return jsonify(ok=True)


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()[:MAX_MESSAGE_CHARS]
    session_id = str(data.get("session") or uuid.uuid4())
    if not message:
        return jsonify(error="Empty message."), 400

    state = get_session(session_id)
    language = LANGUAGES.get(data.get("lang"))
    prompt = f"(Reply in {language}.)\n{message}" if language else message
    try:
        response = state["chat"].send_message(prompt)
    except errors.APIError as e:
        if e.code in (401, 403) or "API key" in str(e.message):
            return jsonify(error="Gemini API key galat hai ya allowed nahi hai. Sahi GEMINI_API_KEY ke saath dobara start karein."), 401
        if e.code == 429:
            return jsonify(error="Gemini quota/limit khatam ho gayi hai, thodi der baad try karein."), 429
        return jsonify(error=f"Gemini API error {e.code}: {e.message}"), 502
    except Exception as e:  # network etc.
        return jsonify(error=f"Gemini se connect nahi ho paya: {e}"), 503

    return jsonify(reply=response.text or "Maaf kijiye, main jawab nahi de paaya. Dobara poochiye.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    print(f"\nBank Support Agent chal raha hai: http://127.0.0.1:{port}  (band karne ke liye Ctrl+C)\n")
    app.run(host="127.0.0.1", port=port)
