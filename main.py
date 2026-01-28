import csv
import os
from datetime import date


FILE_NAME = "expenses.csv"
expenses = []

def normalize_category(category: str) -> str:
    c = category.strip().lower()

    # Standardize common variants
    mapping = {
        "saving": "savings",
        "savings": "savings",
        "current": "current",
        "default": "default",
    }

    return mapping.get(c, c)  # unknown categories stay as-is

def show_menu():
    print("\n=== Expense Tracker ===")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Summary")
    print("4. Monthly Summary")
    print("5. Exit")

def read_amount():
    while True:
        raw = input("Enter amount (e.g., 12.50): ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number (e.g., 10 or 10.5).")


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Backward compatibility: if old rows exist without date
            d = row.get("date", "").strip()
            if not d:
                d = "unknown"

            row["date"] = d
            row["amount"] = str(float(row["amount"]))
            row["category"] = normalize_category(row.get("category", ""))
            row["note"] = row.get("note", "").strip()

            expenses.append(row)




def save_expense_to_csv(expense):
    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as f:
        fieldnames = ["date", "amount", "category", "note"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists or os.path.getsize(FILE_NAME) == 0:
            writer.writeheader()

        writer.writerow(expense)


def add_expense():
    d = date.today().isoformat()  # YYYY-MM-DD
    amount = read_amount()
    category = normalize_category(input("Enter category: "))
    note = input("Enter note: ").strip()

    expense = {
        "date": d,
        "amount": str(amount),
        "category": category,
        "note": note
    }

    expenses.append(expense)
    save_expense_to_csv(expense)
    print(f"Expense added and saved with date {d}.")




def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return

    print("\n--- Expenses ---")
    for i, expense in enumerate(expenses, start=1):
        print(
            f"{i}. Date: {expense['date']} | " 
            f"Amount: {expense['amount']} | "
            f"Category: {expense['category']} | "
            f"Note: {expense['note']}"
        )

def show_summary():
    if not expenses:
        print("No expenses recorded.")
        return

    total = 0.0
    by_category = {}

    for expense in expenses:
        amount = float(expense["amount"])
        total += amount

        cat = expense["category"]
        by_category[cat] = by_category.get(cat, 0.0) + amount

    print("\n--- Summary ---")
    print(f"Total spent: {total:.2f}")

    print("\nBy category:")
    for cat, amt in sorted(by_category.items()):
        print(f"- {cat}: {amt:.2f}")




def migrate_csv_if_needed():
    if not os.path.exists(FILE_NAME):
        return

    backup_name = "expenses_backup.csv"

    # Make backup once (don’t overwrite if it already exists)
    if not os.path.exists(backup_name):
        with open(FILE_NAME, "r", encoding="utf-8") as src, open(backup_name, "w", encoding="utf-8") as dst:
            dst.write(src.read())

    # Rewrite a cleaned version of expenses.csv
    cleaned = []

    with open(FILE_NAME, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                amount = float(row.get("amount", "").strip())
            except ValueError:
                continue  # skip broken rows

            category = normalize_category(row.get("category", ""))
            note = row.get("note", "").strip()
            d = row.get("date", "").strip() or "unknown"
            cleaned.append({
                "date": d,
                "amount": str(amount),
                "category": category,
                "note": note
            })

    # Write cleaned file
    with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["date","amount", "category", "note"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)

def monthly_summary():
    month = input("Enter month (YYYY-MM): ").strip()

    filtered = [e for e in expenses if e["date"].startswith(month)]
    if not filtered:
        print("No expenses found for that month.")
        return

    total = 0.0
    by_category = {}

    for e in filtered:
        amt = float(e["amount"])
        total += amt
        cat = e["category"]
        by_category[cat] = by_category.get(cat, 0.0) + amt

    print(f"\n--- Monthly Summary: {month} ---")
    print(f"Total spent: {total:.2f}")
    print("\nBy category:")
    for cat, amt in sorted(by_category.items()):
        print(f"- {cat}: {amt:.2f}")



def main():
    migrate_csv_if_needed()
    load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")




if __name__ == "__main__":
    main()
