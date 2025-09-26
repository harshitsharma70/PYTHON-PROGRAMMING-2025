# Q2. Loan Eligibility System
age = int(input("Enter Age: "))
income = float(input("Enter Monthly Income: "))
existing_loan = float(input("Enter Existing Loan Amount: "))
cibil = int(input("Enter CIBIL Score: "))

if not (21 <= age <= 60):
    print("Rejected due to age criteria")
elif income < 25000:
    print("Rejected due to low income")
elif existing_loan > 0.5 * income:
    print("Rejected due to high existing loan")
elif cibil < 700:
    print("Rejected due to low CIBIL score")
else:
    print("Eligible for Loan")
