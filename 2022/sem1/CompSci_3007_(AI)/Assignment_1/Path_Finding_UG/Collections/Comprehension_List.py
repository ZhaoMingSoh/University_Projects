# 1. Multiple items in a list
# 2. you want to perform some action to the items
# 3. store the result in a new list

## Problem 1:
number = [1,2,3]
# The old ways of multiplying each element of the list by 2
double = []
for num in number:
    double.append(num*2)
print(double)

# Comprehension list method of the above problem
com_double = [num*2 for num in number]
print(com_double)

## Problem 2:
users = [{'name':'Ming', 'age':23}, {'name':'Jojo', 'age':25}, {'name':'Jonathan', 'age':28}]
select_user = []
for user in users:
    if user['age'] >= 25:
        select_user.append(user['name'])
print(select_user)
# or in the comprehension list format
user_name = [user['name'] for user in users if user['age'] >= 25]
print(user_name)

## Problem 3 : Nested comprehension list - multiple for loops
user_groups = [
    [
        {'name':'Eren Jeager', 'age': 25},
        {'name':'Mikasa Ackerman', 'age':23}
    ],
    [
        {'name':'Naruto Uzumaki', 'age': 33},
        {'name':'Hinata', 'age':30}
    ]
]

# Let say we want to store the name into another list
name = []
for i in user_groups:
    for j in i:
        name.append(j['name'])
print(f'name : {name}')
# or in the comprehension list method
select_name = [j['name'] for i in user_groups for j in i]
print(f'select_name : {select_name}')

# Problem 4: Flattening of List
a = [[1,12],[55],[6,7,8,10]]
flat_a = [item for r in a for item in r]
print(f'flat_a : {flat_a}')

# Problem 5: List of different sizes
nums = [1,2,3]
fruits = ['Peache', 'Orange', 'Banana', 'Apple']
combine = [[i,j] for i in nums for j in fruits]
print(f'combine : {combine}')