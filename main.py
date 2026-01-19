import csv
import os

FILE_NAME = "expenses.csv"
expenses = []


def show_menu():
    print("\n=== Expense Tracker ===")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Summary")
    print("4. Exit")

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
            expenses.append(row)


def save_expense_to_csv(expense):
    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as f:
        fieldnames = ["amount", "category", "note"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists or os.path.getsize(FILE_NAME) == 0:
            writer.writeheader()

        writer.writerow(expense)


def add_expense():
    amount = read_amount()
    category = input("Enter category: ").strip().lower()
    note = input("Enter note: ").strip()

    expense = {
        "amount": str(amount),   # store as string for CSV
        "category": category,
        "note": note
    }

    expenses.append(expense)
    save_expense_to_csv(expense)
    print("Expense added and saved.")



def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return

    print("\n--- Expenses ---")
    for i, expense in enumerate(expenses, start=1):
        print(
            f"{i}. Amount: {expense['amount']} | "
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


def main():
    load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
