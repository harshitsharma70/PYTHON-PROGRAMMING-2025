# Tuple:-

# 1. Built-in data type
# 2. Immutable (cannot change once initialized)
# 3. Stores elements in an ordered sequence
# 4. Supports index methods (Python 3 onwards)
# 5. Uses () parentheses to denote a tuple
# 6. t = ()  -> empty tuple
# 7. Predefined methods for tuple:
#    a. index()
#    b. count()

# Example Program

t1 = ()
print(t1)
print(type(t1))

t2 = (1)
print(t2)
print(type(t2))   # Not a tuple, it's an int

t3 = (1,)
print(t3)
print(type(t3))   # This is a tuple with one element

t4 = (1.1,)
print(t4)
print(type(t4))   # This is a tuple with one float element

t5 = ("abc", 1, 1.1, True, 'a')
print(t5)
print(t5[0])      # Tuple supports indexing

# t5[0] = 'bbb'  # ❌ Not allowed — tuple is immutable
