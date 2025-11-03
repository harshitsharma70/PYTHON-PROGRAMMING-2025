# Program to check Armstrong number using while loop

# Taking input from the user
num = int(input("Enter a number: "))
original_num = num  # store original number
result = 0

# Count digits
n = len(str(num))

# Using while loop to calculate Armstrong sum
while num > 0:
    digit = num % 10
    result += digit ** n
    num //= 10   # remove last digit (this line should be inside the loop)

# Check Armstrong condition
if result == original_num:
    print(original_num, "is an Armstrong number")
else:
    print(original_num, "is NOT an Armstrong number")
