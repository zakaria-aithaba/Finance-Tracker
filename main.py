import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_date, get_description, get_amount, get_category


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=("date", "amount", "category", "description"))
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtred_df = df[mask]

        if filtred_df.empty:
            print("No transactions found")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)})")
            print(filtred_df.to_string(index=False, formatters={"date" : lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtred_df[filtred_df ["category"]=="Income"] ["amount"].sum()
            total_expense = filtred_df[filtred_df["category"]=="Expense"] ["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings : ${total_income - total_expense:.2f}")

        return filtred_df


def add():
    date = get_date("Enter the date of the transaction (dd-mm-yyyy)or enter today's date", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

def plot_transactions(df):
    df.set_index("date", inplace=True)
    income_df = df[df["category"]=="Income"].resample("D").sum().reindex(df.index,fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="red")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="green")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("your Income and Expense Over Time")
    plt.legend()
    plt.show()
    plt.grid()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. Get transactions and summary")
        print("3. Exit")
        choice = input("enter your choice: ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("enter the start date of the transaction (dd-mm-yyyy):")
            end_date = get_date("enter the end date of the transaction:")
            df = CSV.get_transaction(start_date, end_date)
            if input("do you want to see the plot? y/n: ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Thank you for using this program")
            break
        else:
            print("Invalid choice. Choose 1, 2, or 3")

if __name__ == "__main__":
    main()



