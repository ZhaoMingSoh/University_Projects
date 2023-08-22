import string

file = open('pg100.txt', 'r')
file_3 = open('3399.txt', 'r')

file_p1_100 = open('pg100_lower.txt', 'w')
file_p1_3399 = open('pg3399_lower.txt','w')

file_2 = open('pg100_no_punct.txt', 'w')
file_4 = open('3399_no_punct.txt', 'w')

try:
    pg100 = file.read()
    pg3399 = file_3.read()

    # Exercise 4 - Part 1
    temp_1 = pg100.lower()
    temp_2 = pg3399.lower()

    file_p1_100.write(temp_1)
    file_p1_3399.write(temp_2)

    # Exercise 4 - Part 3
    out100 = pg100.translate(str.maketrans('','',string.punctuation)).lower()
    file_2.write(out100)

    out3399 = pg3399.translate(str.maketrans('','',string.punctuation)).lower()
    file_4.write(out3399)

finally:
    file.close()
    file_2.close()
    file_3.close()
    file_4.close()