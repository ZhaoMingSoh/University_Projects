data = {1:'data', 2:'Imperial', 3:'Ouroboros'}
print(data)
# to fetch a particular value using key
print(data[1])
print(data[2])
# or we can use get(key) in to avoid throwing 
# for keys that are not present in the dict
print(data.get(3))
print(data.get(4, "Key Not Found"))
data[4] = 'DAG'
print(data)

# You can have dictionary within a dictionary or list within a dictionary or
# dictionary within a list
prog = {'JS':'ATOM', 'CS':'VS', 'Python':['Pycharm', 'Sublime'], 'Java':{'JSE':'Netbeans', 'JEE':'Eclipse'}}
print(prog)
print(prog["Python"][0])
print(prog["Java"]["JSE"]) # Example of how to select the values in the nested list/dict