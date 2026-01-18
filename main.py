def show_menu():
    print("\n=== Expense Tracker ===")
    print("1. Add expense")
    print("2. View expense")
    print("3. Exit")
    
def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            print("Add expense selected (not implemented yet)")
        elif choice == "2":
            print("View expense selected (not implemented yet)")
        elif choice == "3":
            print("Exiting the program. GoodBye!")
            break
        else:
            print("Invalid choice. Please try again.")

            
if __name__ == "__main__":
    main()  