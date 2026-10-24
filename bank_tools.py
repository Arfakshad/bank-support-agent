"""Tools for the Bank Customer Support Agent.

Author: Arfakshad

DEMO ONLY:
- Tools must be created for an authenticated customer.
- Customer identity is bound by the application, not selected by Gemini.
- Operations use fictional, in-memory demo data.
- Replace in-memory operations with secure bank APIs before production.
"""

import logging
import re

import bank_db

log = logging.getLogger("bank_agent.audit")

ALLOWED_COMPLAINT_CATEGORIES = {
    "failed_transaction",
    "fraud",
    "card",
    "loan",
    "other",
    "account",
    "service",
}


def make_tools(customer_id: str) -> list:
    """Build tools scoped to one authenticated demo customer.

    IMPORTANT:
    The calling application must authenticate the customer before calling
    this function. A customer ID by itself is not proof of authorization.
    """
    customer_id = bank_db._normalize_customer_id(customer_id)

    # Verify the customer exists before creating customer-scoped tools.
    bank_db.get_customer(customer_id)

    def get_account_summary() -> dict:
        """Get the signed-in customer's accounts, balances and card statuses."""
        log.info("Account summary requested")
        customer = bank_db.get_customer(customer_id)
        return {
            "name": customer["name"],
            "currency": bank_db.CURRENCY,
            "accounts": customer["accounts"],
            "cards": customer["cards"],
        }

    def get_recent_transactions(limit: int = 5) -> dict:
        """Get recent transactions for the signed-in customer.

        Args:
            limit: Number of transactions to return, from 1 to 10.
        """
        try:
            limit = int(limit)
        except (TypeError, ValueError, OverflowError):
            limit = 5

        limit = max(1, min(limit, 10))
        log.info("Recent transactions requested; limit=%d", limit)
        customer = bank_db.get_customer(customer_id)
        return {
            "currency": bank_db.CURRENCY,
            "transactions": customer["transactions"][:limit],
        }

    def get_transaction_status(reference: str) -> dict:
        """Look up a transaction belonging to this customer.

        Args:
            reference: Transaction reference, such as TXN1003.
        """
        if not isinstance(reference, str):
            return {"error": "Please provide a valid transaction reference."}

        reference = reference.strip()
        if not re.fullmatch(r"TXN[A-Za-z0-9]{1,20}", reference, re.IGNORECASE):
            return {"error": "Invalid transaction reference format."}

        log.info("Transaction status lookup requested")
        customer = bank_db.get_customer(customer_id)

        for transaction in customer["transactions"]:
            if transaction["ref"].casefold() == reference.casefold():
                return {
                    "currency": bank_db.CURRENCY,
                    "transaction": transaction,
                }

        return {
            "error": (
                "No transaction with that reference was found "
                "on this customer's account."
            )
        }

    def block_card(card_last4: str, customer_confirmed: bool) -> dict:
        """Block the customer's card after explicit confirmation.

        Args:
            card_last4: The last four digits of the customer's card.
            customer_confirmed: True only after explicit confirmation.
        """
        if not isinstance(card_last4, str):
            return {"error": "Please provide the card's last four digits."}

        card_last4 = card_last4.strip()
        if not re.fullmatch(r"\d{4}", card_last4):
            return {"error": "Enter exactly four digits for the card."}

        if customer_confirmed is not True:
            return {
                "error": (
                    "Card not blocked. Ask the customer to explicitly "
                    "confirm blocking this specific card first."
                )
            }

        # Check the latest stored record, not a stale snapshot.
        customer = bank_db.get_customer(customer_id)
        matching_card = next(
            (card for card in customer["cards"] if card["last4"] == card_last4),
            None,
        )
        if matching_card is None:
            return {
                "error": (
                    "No card with those last four digits was found "
                    "on this customer's account."
                )
            }

        if matching_card["status"] == "blocked":
            return {
                "result": "already_blocked",
                "message": "This demo card is already blocked.",
                "card": {
                    "last4": matching_card["last4"],
                    "type": matching_card["type"],
                    "status": matching_card["status"],
                },
            }

        try:
            bank_db.update_card_status(customer_id, card_last4, "blocked")
        except ValueError:
            log.warning("Demo card-block operation could not be completed")
            return {
                "error": (
                    "The card could not be blocked. "
                    "Please verify the card and try again."
                )
            }

        updated_customer = bank_db.get_customer(customer_id)
        updated_card = next(
            (card for card in updated_customer["cards"] if card["last4"] == card_last4),
            None,
        )
        if updated_card is None or updated_card["status"] != "blocked":
            log.error("Demo card-block verification failed")
            return {"error": "The card-block operation could not be verified."}

        log.info("Demo card-block operation completed")
        return {
            "result": "blocked",
            "card": {
                "last4": updated_card["last4"],
                "type": updated_card["type"],
                "status": updated_card["status"],
            },
            "message": (
                "The card is now marked as blocked in demo memory. "
                "This is not a real bank card operation."
            ),
        }

    def create_complaint(category: str, description: str) -> dict:
        """Register a complaint for the authenticated demo customer.

        Args:
            category: failed_transaction, fraud, card, loan, other,
                account or service.
            description: Description of the issue, up to 2000 characters.
        """
        if not isinstance(category, str):
            return {"error": "Complaint category must be text."}
        if not isinstance(description, str):
            return {"error": "Complaint description must be text."}

        category = category.strip().lower()
        description = description.strip()

        if category not in ALLOWED_COMPLAINT_CATEGORIES:
            return {
                "error": (
                    "Invalid category. Choose from: "
                    + ", ".join(sorted(ALLOWED_COMPLAINT_CATEGORIES))
                )
            }
        if not description or len(description) > 2000:
            return {
                "error": (
                    "Complaint description must contain "
                    "1 to 2000 characters."
                )
            }

        log.info("Demo complaint creation requested; category=%s", category)
        try:
            complaint_id = bank_db.add_complaint(
                customer_id,
                category,
                description,
            )
        except (ValueError, TypeError):
            log.warning("Demo complaint creation failed")
            return {
                "error": (
                    "The complaint could not be registered. "
                    "Please verify the details and try again."
                )
            }

        return {
            "complaint_id": complaint_id,
            "status": "registered",
            "message": (
                "The complaint was registered in demo memory. "
                "It is not a real bank complaint."
            ),
        }

    return [
        get_account_summary,
        get_recent_transactions,
        get_transaction_status,
        block_card,
        create_complaint,
    ]
