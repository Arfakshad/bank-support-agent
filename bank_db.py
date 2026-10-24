
"""Mock bank backend for the support agent (demo data only)."""

import copy
import itertools
from datetime import datetime

CURRENCY = "AED"
MAX_PIN_ATTEMPTS = 3

CUSTOMERS = {
    "C1001": {
        "name": "Ahmed Khan",
        "pin": "1234",
        "accounts": [
            {"number": "****4521", "type": "Savings", "balance": 54230.75},
            {"number": "****9902", "type": "Current", "balance": 8120.00},
        ],
        "cards": [
            {"last4": "7788", "type": "Debit", "status": "active"},
            {"last4": "3310", "type": "Credit", "status": "active"},
        ],
        "transactions": [
            {"ref": "TXN1001", "date": "2026-10-21", "desc": "Carrefour Dubai Mall", "amount": -312.40, "status": "completed"},
            {"ref": "TXN1002", "date": "2026-10-20", "desc": "Salary - ACME LLC", "amount": 18500.00, "status": "completed"},
            {"ref": "TXN1003", "date": "2026-10-19", "desc": "UPI/IMPS transfer to Sara", "amount": -1500.00, "status": "failed - amount debited, reversal pending"},
            {"ref": "TXN1004", "date": "2026-10-18", "desc": "Du Mobile bill", "amount": -249.00, "status": "completed"},
            {"ref": "TXN1005", "date": "2026-10-16", "desc": "ATM withdrawal", "amount": -1000.00, "status": "completed"},
        ],
    },
    "C1002": {
        "name": "Fatima Ali",
        "pin": "5678",
        "accounts": [
            {"number": "****1180", "type": "Savings", "balance": 129400.10}
        ],
        "cards": [
            {"last4": "5521", "type": "Debit", "status": "active"}
        ],
        "transactions": [
            {"ref": "TXN2001", "date": "2026-10-22", "desc": "Amazon.ae", "amount": -459.90, "status": "completed"},
            {"ref": "TXN2002", "date": "2026-10-20", "desc": "Rent transfer", "amount": -6500.00, "status": "completed"},
            {"ref": "TXN2003", "date": "2026-10-15", "desc": "Freelance payment", "amount": 3200.00, "status": "completed"},
        ],
    },
}

COMPLAINTS: list[dict] = []
_failed_pins: dict[str, int] = {}
_complaint_ids = itertools.count(5001)


def verify_login(customer_id: str, pin: str) -> str | None:
    customer_id = customer_id.strip().upper()
    customer = CUSTOMERS.get(customer_id)

    if _failed_pins.get(customer_id, 0) >= MAX_PIN_ATTEMPTS:
        raise PermissionError("locked")

    if customer is None or customer["pin"] != pin.strip():
        if customer is not None:
            _failed_pins[customer_id] = _failed_pins.get(customer_id, 0) + 1
        return None

    _failed_pins.pop(customer_id, None)
    return customer["name"]


def get_customer(customer_id: str) -> dict:
    """Return a copy so callers cannot mutate stored data accidentally."""
    customer_id = customer_id.strip().upper()
    if customer_id not in CUSTOMERS:
        raise KeyError("Unknown customer")
    return copy.deepcopy(CUSTOMERS[customer_id])


def update_card_status(
    customer_id: str, card_last4: str, status: str = "blocked"
) -> dict | None:
    """Update a card in the in-memory demo database."""
    customer_id = customer_id.strip().upper()
    card_last4 = str(card_last4).strip()

    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return None

    for card in customer["cards"]:
        if card["last4"] == card_last4:
            card["status"] = status
            return copy.deepcopy(card)

    return None


def add_complaint(customer_id: str, category: str, description: str) -> str:
    if customer_id not in CUSTOMERS:
        raise KeyError("Unknown customer")

    complaint_id = f"CMP{next(_complaint_ids)}"
    COMPLAINTS.append({
        "id": complaint_id,
        "customer": customer_id,
        "category": category,
        "description": description,
        "created": datetime.now().isoformat(timespec="seconds"),
    })
    return complaint_id
