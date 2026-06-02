import pandas as pd
import csv
import os
from tabulate import tabulate

FILE_NAME = "expense.csv"

# Function To Add Expense
def add_expense():
    while True:
        try:
            expense_id = int(input("Enter Expense ID (e.g. 1,2,3...) : "))
            break
        except ValueError:
            print("Invalid ID Entered.")

    purchase_date = input(
        "Enter the date of purchase (e.g. 12.02.2026) : "
    ).title()

    purchase_category = input(
        "Enter the category of purchase (e.g. Food) : "
    ).title()

    while True:
        try:
            purchase_amount = float(
                input("Enter the amount of purchase : ₹")
            )
            break
        except ValueError:
            print("Invalid Amount Entered.")

    description_of_purchase = input(
        "Enter the description of purchase : "
    ).title()

    row = [
        expense_id,
        purchase_date,
        purchase_category,
        purchase_amount,
        description_of_purchase
    ]

    return row


# Function To View Expense
def view_expense(datafile):
    if datafile.empty:
        print("No expenses found.")
    else:
        print(tabulate(
            datafile,
            headers="keys",
            tablefmt="grid",
            showindex=False
        ))


# Function To View Total Expense
def total_expense(datafile):
    return datafile["Purchase Amount"].sum()


# Function To View Category Summary
def view_summary(datafile):
    summary = datafile.groupby(
        "Purchase Category"
    )["Purchase Amount"].sum().reset_index()

    print(tabulate(
        summary,
        headers="keys",
        tablefmt="grid",
        showindex=False
    ))


# Function To Search Expense
def search_expense(datafile):
    category = input(
        "Enter category to search (e.g. Food) : "
    ).title()

    filtered_data = datafile[
        datafile["Purchase Category"] == category
    ]

    if filtered_data.empty:
        print("No expenses found for that category.")
    else:
        print(tabulate(
            filtered_data,
            headers="keys",
            tablefmt="grid",
            showindex=False
        ))


# Function To Delete Expense
def delete_expense(datafile):
    try:
        expense_id = int(
            input("Enter Expense ID to delete : ")
        )

        if expense_id not in datafile["ID"].values:
            print("Expense ID not found.")
            return

        updated_data = datafile[
            datafile["ID"] != expense_id
        ]

        updated_data.to_csv(FILE_NAME, index=False)

        print("Expense Deleted Successfully.")

    except ValueError:
        print("Invalid ID Entered.")


# Create CSV if not exists
fields = [
    "ID",
    "Purchase Date",
    "Purchase Category",
    "Purchase Amount",
    "Description of Purchase"
]

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)


# Main Program
while True:

    print("\n")
    print("========================================")
    print("          THE EXPENSE TRACKER")
    print("========================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. View Total Amount Spent")
    print("4. View Category Summary")
    print("5. Search Expenses")
    print("6. Delete Expense")
    print("7. Exit")
    print("========================================")

    try:
        data = pd.read_csv(FILE_NAME)
    except:
        print("Error reading CSV file.")
        break

    user_choice = input("Enter your choice: ")

    if user_choice == "1":

        expense_row = add_expense()

        with open(FILE_NAME, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(expense_row)

        print("Expense Added Successfully.")

    elif user_choice == "2":

        view_expense(data)

    elif user_choice == "3":

        total_amount = total_expense(data)

        print(f"Total Amount Spent: ₹{total_amount:.2f}")

    elif user_choice == "4":

        view_summary(data)

    elif user_choice == "5":

        search_expense(data)

    elif user_choice == "6":

        delete_expense(data)

    elif user_choice == "7":

        print("Thank You For Using Expense Tracker.")
        break

    else:

        print("Invalid Choice. Please Try Again.")
