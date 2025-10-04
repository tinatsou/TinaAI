"""
Personal Expense Tracker
------------------------

This script implements a simple command‑line based personal expense tracker.
Users can log their daily expenses with a date, category, amount, and
description; view a list of all recorded expenses; set a monthly budget and
track spending against it; and save or load expenses from a CSV file. The
program presents an interactive, menu‑driven interface to simplify use.

Usage
~~~~~

Run the script from a terminal with Python 3.9+::

    python personal_expense_tracker.py

When the program starts it will automatically attempt to load any existing
expenses from the default CSV file (``expenses.csv``). If no such file
exists, the expense list will start empty. Choose actions from the menu by
entering the corresponding number.

Implementation Notes
~~~~~~~~~~~~~~~~~~~~

* Expense entries are stored in a list of dictionaries with the following keys:
  ``date`` (string, ISO format ``YYYY‑MM‑DD``), ``category`` (string),
  ``amount`` (float), and ``description`` (string).
* Expenses are persisted in a CSV file using Python’s built‑in ``csv`` module.
  When loading, the script will silently skip incomplete rows (missing any
  required field).
* Basic validation is performed on user input: the date must follow the
  ``YYYY‑MM‑DD`` format and the amount must be a number greater than zero.
  Invalid entries will prompt the user to re‑enter the value.
* The budget tracker calculates the total spend across all loaded and newly
  added expenses. If the spend exceeds the budget, a warning message is shown;
  otherwise the remaining balance for the month is displayed.

"""

from __future__ import annotations

import csv
import os
import sys
from datetime import datetime
from typing import List, Dict


Expense = Dict[str, object]

def load_expenses(filename: str) -> List[Expense]:
    """Load expenses from a CSV file.

    Each row in the file is expected to have four columns: ``date``,
    ``category``, ``amount``, and ``description``. Rows missing any of these
    fields will be skipped.

    Args:
        filename: The path to the CSV file.

    Returns:
        A list of expense dictionaries.
    """
    expenses: List[Expense] = []
    if not os.path.isfile(filename):
        return expenses
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=["date", "category", "amount", "description"])
            for row in reader:
                # Skip rows with any missing fields
                if not all(row.get(field) for field in ("date", "category", "amount", "description")):
                    continue
                date_str = row["date"]
                category = row["category"]
                amount_str = row["amount"]
                description = row["description"]
                try:
                    amount = float(amount_str)
                except ValueError:
                    # Skip rows with non‑numeric amount values
                    continue
                expense: Expense = {
                    "date": date_str,
                    "category": category,
                    "amount": amount,
                    "description": description,
                }
                expenses.append(expense)
    except IOError as exc:
        print(f"Error reading file {filename}: {exc}", file=sys.stderr)
    return expenses


def save_expenses(filename: str, expenses: List[Expense]) -> None:
    """Save expenses to a CSV file.

    Args:
        filename: The path to the CSV file.
        expenses: A list of expense dictionaries to save.
    """
    try:
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for exp in expenses:
                writer.writerow([exp["date"], exp["category"], f"{exp['amount']:.2f}", exp["description"]])
        print(f"Saved {len(expenses)} expense(s) to {filename}.")
    except IOError as exc:
        print(f"Error writing file {filename}: {exc}", file=sys.stderr)


def prompt_date() -> str:
    """Prompt the user for a date in YYYY‑MM‑DD format and validate it."""
    while True:
        date_str = input("Enter the date (YYYY‑MM‑DD): ").strip()
        try:
            # Validate format by attempting to parse
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY‑MM‑DD.")


def prompt_category() -> str:
    """Prompt the user for an expense category."""
    while True:
        category = input("Enter the category (e.g. Food, Travel): ").strip()
        if category:
            return category
        print("Category cannot be empty.")


def prompt_amount() -> float:
    """Prompt the user for the amount spent and validate it is a positive number."""
    while True:
        amount_str = input("Enter the amount spent: ").strip()
        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError
            return amount
        except ValueError:
            print("Invalid amount. Please enter a positive number.")


def prompt_description() -> str:
    """Prompt the user for a brief description."""
    return input("Enter a brief description: ").strip()

def add_expense(expenses: List[Expense]) -> None:
    """Add a new expense to the list by prompting the user for details."""
    print("\nAdd a New Expense")
    date_str = prompt_date()
    category = prompt_category()
    amount = prompt_amount()
    description = prompt_description()
    expense: Expense = {
        "date": date_str,
        "category": category,
        "amount": amount,
        "description": description,
    }
    expenses.append(expense)
    print("Expense added successfully.\n")


def view_expenses(expenses: List[Expense]) -> None:
    """Display all recorded expenses in a readable format."""
    print("\nRecorded Expenses")
    if not expenses:
        print("No expenses recorded yet.\n")
        return
    for idx, exp in enumerate(expenses, start=1):
        print(f"{idx}. Date: {exp['date']} | Category: {exp['category']} | Amount: ${exp['amount']:.2f} | Description: {exp['description']}")
    print("")


def track_budget(expenses: List[Expense], budget: float) -> None:
    """Calculate total expenses and compare to the user's budget."""
    total_spent = sum(exp["amount"] for exp in expenses)
    print(f"\nTotal spent so far: ${total_spent:.2f}")
    if budget is None:
        print("No budget set for this session.\n")
        return
    print(f"Monthly budget: ${budget:.2f}")
    remaining = budget - total_spent
    if remaining < 0:
        print(f"You have exceeded your budget by ${abs(remaining):.2f}!\n")
    else:
        print(f"You have ${remaining:.2f} left for the month.\n")


def set_budget() -> float:
    """Prompt the user to input a monthly budget and return it as a float."""
    while True:
        budget_str = input("Enter your monthly budget: ").strip()
        try:
            budget = float(budget_str)
            if budget < 0:
                raise ValueError
            return budget
        except ValueError:
            print("Invalid budget. Please enter a positive number.")


def display_menu() -> None:
    """Display the main menu options."""
    print("Personal Expense Tracker Menu")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Track budget")
    print("4. Save expenses")
    print("5. Exit")


def main() -> None:
    """Main entry point for the expense tracker program."""
    FILENAME = "expenses.csv"
    expenses = load_expenses(FILENAME)
    budget: float | None = None
    if expenses:
        print(f"Loaded {len(expenses)} existing expense(s) from {FILENAME}.\n")
    while True:
        display_menu()
        choice = input("Choose an option (1‑5): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            if budget is None:
                budget = set_budget()
            track_budget(expenses, budget)
        elif choice == "4":
            save_expenses(FILENAME, expenses)
        elif choice == "5":
            # Save before exiting
            if expenses:
                save_expenses(FILENAME, expenses)
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please select a number between 1 and 5.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting without saving.")
