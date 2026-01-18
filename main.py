import csv
import os

FILE_NAME = "expenses.csv"
expenses = []


def show_menu():
    print("\n=== Expense Tracker ===")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Exit")


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
    amount = input("Enter amount: ").strip()
    category = input("Enter category: ").strip()
    note = input("Enter note: ").strip()

    expense = {
        "amount": amount,
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


def main():
    load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
