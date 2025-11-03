start = int(input(Enter start of range:))
end = int(input(Enter end of range:))

for num in range(start, end + 1):
    if num % 5 == 0:
        print(f"\nTable of {i}:)
        for i in range(1, 11):
            print(f"{num} * {i} = {num * i}")
            
print("\nThis program helps to understand f-strings.") 
