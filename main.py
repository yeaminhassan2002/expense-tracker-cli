expenses = []

def show_menu():
    print("\n=== Expense Tracker ===")
    print("1. Add expense")
    print("2. View expense")
    print("3. Exit")

def add_expense():
    amount = input("Enter Amount:")
    category = input("Enter Category:")
    note = input("Enter Note (optional):")
    
    expense = {
        "amount": amount,
        "category": category,
        "note": note
    }
    
    expenses.append(expense)
    print("Expense added successfully!")
    
def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return
    
    print("\n--- Expenses ---")
    for i, expense in enumerate(expenses, start=1):
        print(
            f"{i}. Amount: {expense['amount']} |"
            f" Category: {expense['category']} |"
            f" Note: {expense['note']}"
        )
    
def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Exiting the program. GoodBye!")
            break
        else:
            print("Invalid choice. Please try again.")

            
if __name__ == "__main__":
    main()  