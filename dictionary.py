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
print(t5.index(1))   # index() returns the index of an element
print(t5.count(1))   # count() returns number of occurrences of an element


# Dictionary:-

# Properties
# 1. Built-in data type
# 2. Stores elements in the form of key-value pairs
# 3. Unordered collection of elements
# 4. Does not support indexing like list, string, or tuple
# 5. Uses {} curly braces to define a dictionary

d1 = {}
print(d1)
print(type(d1))

d2 = {
    "id": 101,
    "name": "abc",
    "marks": 504.4,
    "sub_code": [101, 102, 103]
}
print(d2)

# Keys are unique; values can be duplicated
d3 = {
    101: "C",
    102: "C++",
    103: "Java",
    104: "Python"
}
print(d3)

d4 = {
    101: "C",
    "name": "abc",
    3.0: "Python",
    "Reg_num": 23045
}
print(d4)

# Accessing dictionary elements
print(d2["name"])       # Access value by key
print(d3[104])          # Access value by numeric key

# Adding new key-value pair
d2["college"] = "ABC Institute"
print(d2)

# Updating a value
d2["marks"] = 550
print(d2)

# Deleting a key-value pair
del d2["id"]
print(d2)

# Dictionary methods examples
print(d2.keys())        # Returns all keys
print(d2.values())      # Returns all values
print(d2.items())       # Returns all key-value pairs
