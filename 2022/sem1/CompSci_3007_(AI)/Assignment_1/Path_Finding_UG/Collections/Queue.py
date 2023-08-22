# Priority Queue
# l = []
# l.append([2,1,0])
# l.append([0,0,0])
# l.sort(reverse = True)
# l.pop()
# print(f'l : {l}')
# l.append([1,1,1])
# l.append([2,0,1])
# l.sort(reverse = True)
# l.pop()
# print(f'l : {l}')
# l.append([1,2,2])
# l.sort(reverse = True)
# print(f'l : {l}')
# l.append([2,2,2])
# l.append([1,2,3])
# l.sort(reverse = True)
# print(f'l : {l}')

# from queue import PriorityQueue
# q = PriorityQueue()

# q.put([2,"1 0", 1])
# q.put([0,"0 0", 2])
# q.get()
# q.put([2,"2 0", 3])
# q.put([1,"1 1", 4])
# q.put([3,"3 0", 5])
# q.get()
# q.put(1, "2 1", 6)
# print(q.queue)

# Sort according to the number in which sth comes in.
# Sort the smallest to the biggest
# l_2 = []
# l_2.append([2, "1 0", 1])
# l_2.append([0, "0 0", 2])
# l_2.sort(reverse = True)
# l_2.pop()
# l_2.append([2, "2 0", 3])
# l_2.append([1, "1 1", 4])
# l_2.append([3, "3 0", 5])
# l_2.sort(key = lambda x: x[2])
# l_2.sort(reverse = True)
# print(l_2)
# l_2.append([1, "2 1", 6])
# l_2.sort(key = lambda x: x[2])
# l_2.sort(reverse = True)
# print(l_2)
l_2 = []
l_2.insert(0, [5.23606797749979, 2.23606797749979, '4 5'])
l_2.insert(0, [6.23606797749979, 2.23606797749979, '6 5'])
l_2.insert(0, [4.0, 3.0, '5 4'])
l_2.sort(key = lambda x: (x[0], -x[1]))
# l_2.sort(key = lambda x:x[1])
print(f"l_2 sort in terms of the order with which the elements were discovered : {l_2}")
# l_2.sort(key = lambda y: y[0])
# print(f"l_2 sort in terms of f_cost : {l_2}")
# # l_2 = [i for i in l_2 if i[2] != "4 4"]
# print(f'l_2 sort in terms of h(n) : {l_2}')