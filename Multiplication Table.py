# Program to generate multiplication table of a given number

# Taking input from user
num = int(input("Enter a number: "))

print(f"\nMultiplication Table of {num}:")

# Using for loop to generate table from 1 to 10
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")
