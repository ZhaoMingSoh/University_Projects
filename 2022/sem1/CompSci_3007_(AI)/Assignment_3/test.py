import numpy as np
# neighbours = [[1,0],[0,1],[0,0]]
# d = {1:{"index":[1,0], "bit_seq":[1,0,1,1]}, 2:{"index":[0,1], "bit_seq":[1,1,0,1]}, 3:{"index":[0,0], "bit_seq":[0,0,1,1]}}
# actual = {(0,0):[1,1,0,1], (0,1):[1,0,0,1], (1,0):[0,1,1,0]}


# for key, val in d.items():
#     for key, val in val.items():
#         print(key, val)

# d[1]["Hi"] = 1
# print()

# for key, val in d.items():
#     for key, val in val.items():
#         print(key, val)

# d2 = [[1,1,2,3],[2,3,4,5],[4,5,6,7]]


# d[1]["Hey"] = 1
# print(d)
debug_output = []
data = np.load('debug_output.npz')
lst = data.files
for item in lst:
    print(item)
    debug_output.append(data[item])
    print(data[item])

# output = []
# data_2 = np.load('output.npz')
# lst_2 = data.files
# for item in lst_2:
#     print(item)
#     output.append(data[item])

# for i in range(len(debug_output)):
#     print(f"array = {i}")
#     for j in range(len(debug_output[0])):
#         for k in range(len(debug_output[0][0])):
#             if output[i][j][k] != debug_output[i][j][k]:
#                 print(f"diff at arr[{i}][{j}][{k}] :")
#                 print(f"output[{i}][{j}][{k}] = {output[i][j][k]}, debug_output[{i}][{j}][{k}] = {debug_output[i][j][k]}")

