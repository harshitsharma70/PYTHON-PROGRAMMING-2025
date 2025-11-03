letters = ['a', 'b', 'a', 'c']
print("Count of 'a':", letters.count('a'))
print("Index of 'c':", letters.index('c'))

letters2 = ['d', 'e']
letters.extend(letters2)
print("After extend:", letters)

letters.pop(1)
print("After pop:", letters)

letters.clear()
print("After clear:", letters)
