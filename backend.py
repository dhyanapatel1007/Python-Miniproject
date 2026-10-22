
import json
import os
from datetime import datetime


class ExpenseTracker:
    """Handles transactions, calculations, and file storage."""

    def __init__(self, filename="expenses.json"):
        folder = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(folder, filename)
        self.transactions = []
        self.load_data()

    def load_data(self):
        """Load saved transactions from the JSON file."""
        if not os.path.exists(self.filename):
            self.transactions = []
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.transactions = data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            self.transactions = []

    def save_data(self):
        """Save all transactions to the JSON file."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.transactions, file, indent=4)

    def add_transaction(
        self, title, amount, category, transaction_type, date
    ):
        """Validate and add a new transaction."""
        title = title.strip()
        category = category.strip()
        transaction_type = transaction_type.strip()
        date = date.strip()

        if not title:
            raise ValueError("Please enter a transaction description.")

        if not category:
            raise ValueError("Please select a category.")

        if transaction_type not in ("Income", "Expense"):
            raise ValueError("Select Income or Expense.")

        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a valid number.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must use YYYY-MM-DD format.")

        next_id = max(
            (item.get("id", 0) for item in self.transactions),
            default=0
        ) + 1

        transaction = {
            "id": next_id,
            "title": title,
            "amount": round(amount, 2),
            "category": category,
            "type": transaction_type,
            "date": date
        }

        self.transactions.append(transaction)

        try:
            self.save_data()
        except OSError:
            self.transactions.pop()
            raise

        return transaction

    def delete_transaction(self, transaction_id):
        """Delete a transaction using its ID."""
        original = self.transactions[:]

        self.transactions = [
            item for item in self.transactions
            if item.get("id") != transaction_id
        ]

        if len(self.transactions) == len(original):
            raise ValueError("The selected transaction was not found.")

        try:
            self.save_data()
        except OSError:
            self.transactions = original
            raise

    def get_transactions(self, search_text=""):
        """Return transactions, newest first, matching the search."""
        search_text = search_text.strip().lower()

        results = [
            item for item in self.transactions
            if search_text == ""
            or search_text in item.get("title", "").lower()
            or search_text in item.get("category", "").lower()
            or search_text in item.get("type", "").lower()
            or search_text in item.get("date", "").lower()
        ]

        return sorted(
            results,
            key=lambda item: (item.get("date", ""), item.get("id", 0)),
            reverse=True
        )

    def get_summary(self):
        """Calculate total income, expenses, and balance."""
        income = sum(
            float(item["amount"])
            for item in self.transactions
            if item.get("type") == "Income"
        )

        expenses = sum(
            float(item["amount"])
            for item in self.transactions
            if item.get("type") == "Expense"
        )

        return {
            "income": round(income, 2),
            "expenses": round(expenses, 2),
            "balance": round(income - expenses, 2),
            "count": len(self.transactions)
        }
