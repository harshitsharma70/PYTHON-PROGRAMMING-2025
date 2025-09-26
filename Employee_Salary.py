# Q1. Employee Salary Slip Generator
basic = float(input("Enter Basic Salary: "))

hra = 0.20 * basic
da = 0.10 * basic
pf = 0.12 * basic
gross = basic + hra + da
net = gross - pf

if net >= 80000:
    category = "High Earner"
elif net >= 50000:
    category = "Mid Earner"
else:
    category = "Low Earner"

print(f"Basic: {basic}, HRA: {hra}, DA: {da}, PF: {pf}")
print(f"Gross Salary = {gross}, Net Salary = {net}")
print("Category:", category)
