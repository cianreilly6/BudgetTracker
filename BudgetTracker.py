import json
import os
from datetime import datetime

# File to store budget data
data_file = 'budget_data.json'

# Check if the data file exists, if not create it
if not os.path.exists(data_file):
    with open(data_file, 'w') as file:
        json.dump({}, file)

# Load existing data from the file
def load_data():
    with open(data_file, 'r') as file:
        return json.load(file)

# Save data to the file
def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

# Add income or expense entry
def add_entry(data, entry_type, amount, category, description):
    date = datetime.now().strftime('%Y-%m-%d')
    if date not in data:
        data[date] = {"income": 0, "expenses": {}}
    
    # Add income or expense to the correct category
    if entry_type == 'income':
        data[date]["income"] += amount
    elif entry_type == 'expense':
        if category not in data[date]["expenses"]:
            data[date]["expenses"][category] = 0
        data[date]["expenses"][category] += amount
    
    # Save updated data
    save_data(data)

# View monthly summary
def view_summary(data):
    current_month = datetime.now().strftime('%Y-%m')
    total_income = 0
    total_expenses = 0
    expense_categories = {}
    
    for date, entry in data.items():
        if date.startswith(current_month):  # Filter by current month
            total_income += entry["income"]
            for category, amount in entry["expenses"].items():
                total_expenses += amount
                if category not in expense_categories:
                    expense_categories[category] = 0
                expense_categories[category] += amount
    
    print(f"\n--- Monthly Summary for {current_month} ---")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print("Expenses by Category:")
    for category, amount in expense_categories.items():
        print(f"  {category}: ${amount:.2f}")
    print(f"Remaining Balance: ${total_income - total_expenses:.2f}\n")

# Display main menu
def display_menu():
    print("Personal Budget Tracker")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Monthly Summary")
    print("4. Exit")
    
def main():
    data = load_data()
    
    while True:
        display_menu()
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            amount = float(input("Enter income amount: $"))
            description = input("Enter description: ")
            add_entry(data, 'income', amount, 'General', description)
            print("Income added successfully.\n")
        
        elif choice == '2':
            amount = float(input("Enter expense amount: $"))
            category = input("Enter expense category (e.g., Food, Transport, etc.): ")
            description = input("Enter description: ")
            add_entry(data, 'expense', amount, category, description)
            print("Expense added successfully.\n")
        
        elif choice == '3':
            view_summary(data)
        
        elif choice == '4':
            print("Exiting the Personal Budget Tracker. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
