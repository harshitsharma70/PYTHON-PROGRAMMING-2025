# Q8. ATM Transaction Simulation
balance = float(input("Enter Account Balance: "))
withdraw = float(input("Enter Amount to Withdraw: "))
account_type = input("Enter Account Type (Saving/Current): ").lower()
day = input("Enter Day (weekday/weekend): ").lower()

min_balance = 1000
limit = 25000 if account_type == "saving" else 50000
fee = 50 if day == "weekend" else 0

if withdraw > limit:
    print("Failure: Exceeds daily limit")
elif balance < withdraw + min_balance + fee:
    print("Failure: Insufficient balance")
else:
    balance -= (withdraw + fee)
    print("Withdrawal Successful")
    print("Updated Balance =", balance)
