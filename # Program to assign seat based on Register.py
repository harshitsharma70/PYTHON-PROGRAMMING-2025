# Program to assign seat based on Registration Number

reg_no = int(input("Enter your Registration Number (1 - 61): "))

if 1 <= reg_no <= 61:
    row = (reg_no - 1) // 10 + 1
    print(f" Your Seat is in Row {row}")
else:
    print(" Invalid Registration Number! Please enter between 1 and 61.")