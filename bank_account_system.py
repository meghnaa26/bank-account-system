import json
import random
import datetime

accounts=[]

choice=""


def create_account():
    name = input("Enter your name: ")
    pin = int(input("Please enter a 4 digit Pin : "))
    amount = float(input("Enter your initial deposit: "))
    account_number = random.randint(10000,99999)
    account = { 
        "name" : name,
        "account_number" :account_number,
        "pin" : pin,
        "balance": amount,
        "transactions": []
    }
    accounts.append(account)
    save_data()

    print("=== ACCOUNT CREATED ===")
    print("Welcome ", name ,"!")
    print("Your Account Number: ",account_number)
    print("Please remember your PIN.")
    print("Initial Balnace: ",amount)


def logged_in(account):
    user_choice=""
    while user_choice !="6":
        print("=== MY ACCOUNT ===")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Transfer")
        print("6. Logout")

        user_choice= input("Enter your choice: ")

        if user_choice == "1":
           deposit(account)
        elif user_choice == "2":
           withdraw(account)
        elif user_choice == "3":
           check_balance(account)
        elif user_choice == "4":
            view_transactions(account)
        elif user_choice =="5":
            transfer(account)
        elif user_choice == "6":
            print("Thank you for banking with us.")
        else:
            print("Invalid choice")

        
def deposit(account):
    amount=float(input("Enter the amount to deposit: "))
    account["balance"] += amount
    transaction = {
        "type" : "Deposit",
        "amount" : amount,
        "date" : str(datetime.datetime.now()),
        "balance after" : account["balance"]
    }
    account["transactions"].append(transaction)
    save_data()
    print("Deposited Rs ",amount)
    print("New Balance: ",account["balance"])


def withdraw(account):
    amount = float(input("Enter the amount to withdraw: "))
    if account["balance"] < amount:
        print("Balance is not sufficient")
    else:
        account["balance"] -= amount
        transaction = {
            "type" : "Withdraw",
            "amount" : amount,
            "date" : str(datetime.datetime.now()),
            "balance after" : account["balance"]
        }
        account["transactions"].append(transaction)
        save_data()
        print("Withdraw Rs ",amount)
        print("New Balance: ",account["balance"])


def check_balance(account):
    print(account["balance"])


def view_transactions(account):
    if len(account["transactions"]) == 0:
        print("No transactions yet.")
        return
    
    for t in account["transactions"]:
        if t["type"] == "Transfer Sent":
            print(t["date"], "→ Sent Rs", t["amount"],
                  "to", t["to_account"])
        elif t["type"] == "Transfer Received":
            print(t["date"], "→ Received Rs", t["amount"],
                  "from", t["from_account"])
        else:
            print(t["date"], t["type"],
                  "Rs", t["amount"])


def login():
    account_number=int(input("Enter your account number: "))
    found=False
    for account in accounts: 
        if account["account_number"] == account_number:
            found = True
            pin= int(input("Enter your PIN number: "))
            if account["pin"] == pin:
                logged_in(account)
            else :
                print("Wrong PIN! Please try again.")

    if found == False:
        print("Account is not found.")
        

def transfer(account):
    reciepeint_account_number = int(input("Enter recepient's account number: "))
    receiver = None
    for acc in accounts:
        if acc["account_number"] == reciepeint_account_number:
            receiver = acc

    
    if receiver is None:
        print("Account not found.")
    else:
        amount = float(input("Enter the amount to transfer: "))
        if account["balance"] < amount:
            print("Insufficient balance.")
        else:
            account["balance"] -= amount
            receiver["balance"] += amount
           
            print("Transfer successful!")
            print("Transferred Rs", amount, "to", receiver["name"])
            print("New Balance: Rs", account["balance"])
    
            transaction = {
               "type" : "Transfer Sent",
               "amount" : amount,
                "to_account" : receiver["account_number"],
                "date" : str(datetime.datetime.now()),
                "balance after": account["balance"]
            }
            account["transactions"].append(transaction)
            save_data()

            transaction = {
                "type": "Transfer Received",
                "amount": amount,
                "from_account":account["account_number"],
                "date": str(datetime.datetime.now()),
                "balance after": receiver["balance"]
            }
            receiver["transactions"].append(transaction)
            save_data()


def save_data():
    with open("accounts.json","w") as file:
        json.dump(accounts, file)


def load_data():
    global accounts
    try: 
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
    except:
        pass


load_data()
while choice != "3":
    print("=== BANK SYSTEM ===")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()
    elif choice == "2":
        login()
    elif choice == "3":
        print("Thank you for banking with us.")
    else:
        print("Invalid choice.")


