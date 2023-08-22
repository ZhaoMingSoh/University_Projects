# print("Hello World!")

# # Variables and Data Type
# ## You can store all different types of data into a variable in python
# character_Age = "25"
# character_Item = "Sunfire"

# print(character_Age+" and "+character_Item)

# -------------------------------------------------------------------------------

# # Working with Strings
# phrase = "Giraffe Animal"
# print(phrase.lower().islower())
# # String length
# print(len(phrase))
# # String Indexing
# print(phrase[0])

# -------------------------------------------------------------------------------

# #Working With Numbers
# # Modulo 
# print(10%3)

# # Convert Number to strings
# print(str(25))

# # Built-in Functions in Python
# from math import *
# print(abs(-5))
# print(pow(3,2))
# print(ceil(3.1))
# print(floor(3.9))

# -------------------------------------------------------------------------------

# # Input from User
# name = input("Enter Your Name: ")
# print(name)

# -------------------------------------------------------------------------------

# # Calculator 
# num_1 = input("Enter the First Number : ")
# num_2 = input("Enter the Second Number : ")
# result = float(num_1) + float(num_2)
# print(str(result))

# -------------------------------------------------------------------------------

# # Lists 
# Champions = ["Ahri", "Lissandra", "Olaf", "Kha Zix", "Nasus"]
# # Upto not including 3
# print(Champions[1:3])

# -------------------------------------------------------------------------------

# # List Functions
# Movies = ["Up", "Lion King", "Avengers", "Thor", "Black Widow"]
# Numbers = [1,2,3,4,5,6,1,1]

# # Add two lists together
# Numbers.extend(Movies)

# # Add new item to end of the list
# Numbers.append(10)

# # Insert new item to any position in the list
# Numbers.insert(0,100)

# # Delete an item from the list 
# Numbers.remove(1)

# # Count the number of items in a list
# print(Numbers.count(1))
# print(Numbers)

# -------------------------------------------------------------------------------

# # Tuples
# # Very similar to list but Cannot be changed (Immutable)
# coordinates = (4, 5)

# # I can access the elements in a Tuple
# print(coordinates[0])

# -------------------------------------------------------------------------------

# # Functions
# def Add(num_1,num_2):
#     result = num_1 + num_2
#     print(result)

# Add(1,2)

# -------------------------------------------------------------------------------

# # Return Statement 
# def cube(num):
#     result = num*num*num
#     return result

# print(cube(3))

# -------------------------------------------------------------------------------

# # If Statement
# is_male = False
# is_tall = True

# if is_male and is_tall:
#     print("You are a tall male")
# elif is_male and not(is_tall):
#     print("You are a short male")
# elif not(is_male) and is_tall:
#     print("You are tall but not a male")
# else:
#     print("You are neither male or tall")

# -------------------------------------------------------------------------------

# # Dictionaries

# monthConversions = {
#     "Jan" : "January",
#     "Feb" : "Febuary",
#     "Mar" : "March",
#     "Apr" : "April",
#     "May" : "May",
#     "Jun" : "June",
#     "Jul" : "July",
#     "Aug" : "August",
#     "Sep" : "September",
#     "Oct" : "October",
#     "Nov" : "November",
#     "Dec" : "December"
#  }

# print(monthConversions["Mar"])

# -------------------------------------------------------------------------------

# # WhileLoop

# i = 1

# while i <= 10:
#     print(i)
#     i += 1

# -------------------------------------------------------------------------------

# # ForLoop
# Champs = ["Renekton", "Nasus", "Darius"]
# for index in Champs:
#     print(index)

# # or 

# for i in range(len(Champs)):
#     print(Champs[i])

# -------------------------------------------------------------------------------
# # 2-D Lists

# number_grid = [
#     [1,2,3],
#     [4,5,6],
#     [7,8,9]
# ]

# for row in number_grid:
#     for col in row:
#         print(col)

# -------------------------------------------------------------------------------

# # Classes and Objects

# class student:
#     def __init__(self, name, major, gpa, is_On_Probation):
#         self.name = name
#         self.major = major
#         self.gpa = gpa
#         self.is_On_Probation = is_On_Probation


# stu_1 = student("Annie", "Computer Science", 6.5, False)
# print(stu_1.name)

# -------------------------------------------------------------------------------




















