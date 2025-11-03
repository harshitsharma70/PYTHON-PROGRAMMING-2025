# Program to calculate factorial using while loop

# Taking input from the user
num = int(input("Enter a number: "))

factorial = 1
i = 1

# Using while loop
while i <= num:
    factorial *= i
    i += 1  # This must be indented inside the loop

print(f"Factorial of {num} is {factorial}")
