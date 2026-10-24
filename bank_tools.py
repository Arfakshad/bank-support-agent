"""Tools the support agent can call. Author: Arfakshad

SECURITY: tools are built per signed-in customer (make_tools). The model never
chooses whose account to touch - the customer id is bound here, in code, after
the PIN login. Tools only ever see that customer's data.
"""

import logging

import bank_db

log = logging.getLogger("bank_agent.audit")


def make_tools(customer_id: str) -> list:
    customer = bank_db.get_customer(customer_id)

    def get_account_summary() -> dict:
        """Get the signed-in customer's name, bank accounts with balances, and cards."""
        log.info("%s get_account_summary", customer_id)
        return {
            "name": customer["name"],
            "currency": bank_db.CURRENCY,
            "accounts": customer["accounts"],
            "cards": customer["cards"],
        }

    def get_recent_transactions(limit: int = 5) -> dict:
        """Get the signed-in customer's most recent transactions (newest first).

        Args:
            limit: How many transactions to return, 1 to 10.
        """
        log.info("%s get_recent_transactions %s", customer_id, limit)
        limit = max(1, min(int(limit), 10))
        return {"currency": bank_db.CURRENCY, "transactions": customer["transactions"][:limit]}

    def get_transaction_status(reference: str) -> dict:
        """Look up one transaction by its reference number, for example TXN1003.

        Args:
            reference: The transaction reference number the customer gives.
        """
        log.info("%s get_transaction_status %s", customer_id, reference)
        for txn in customer["transactions"]:
            if txn["ref"].lower() == reference.strip().lower():
                return {"currency": bank_db.CURRENCY, "transaction": txn}
        return {"error": "No transaction with that reference was found on this customer's account."}

    def block_card(card_last4: str, customer_confirmed: bool) -> dict:
        """Block one of the customer's cards. Irreversible from chat.

        Only call this with customer_confirmed=true AFTER the customer has explicitly
        confirmed in their latest message that they want this exact card blocked.

        Args:
            card_last4: Last 4 digits of the card to block.
            customer_confirmed: True only if the customer explicitly confirmed.
        """
        log.info("%s block_card %s confirmed=%s", customer_id, card_last4, customer_confirmed)
        if not customer_confirmed:
            return {"error": "Not blocked. Ask the customer to confirm which card to block, then call again."}
        for card in customer["cards"]:
            if card["last4"] == card_last4.strip():
                card["status"] = "blocked"
                return {"result": "blocked", "card": card}
        return {"error": "No card with those last 4 digits was found on this customer's account."}

    def create_complaint(category: str, description: str) -> dict:
        """Register a complaint or dispute for the customer (for example a failed
        transaction, unauthorised transaction, or a service issue).

        Args:
            category: Short category such as failed_transaction, fraud, card, loan, other.
            description: A clear description of the issue in English.
        """
        log.info("%s create_complaint %s", customer_id, category)
        complaint_id = bank_db.add_complaint(customer_id, category, description)
        return {"complaint_id": complaint_id, "status": "registered"}

    return [
        get_account_summary,
        get_recent_transactions,
        get_transaction_status,
        block_card,
        create_complaint,
    ]
