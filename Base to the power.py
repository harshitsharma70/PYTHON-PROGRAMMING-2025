# Program to calculate base to the power using while loop

# Taking input from user
base = int(input("Enter the base number: "))
power = int(input("Enter the power: "))

result = 1
i = 1

# Using while loop to calculate power
while i <= power:
    result *= base
    i += 1  # This must be inside the loop

print(f"{base} raised to the power {power} is {result}")
