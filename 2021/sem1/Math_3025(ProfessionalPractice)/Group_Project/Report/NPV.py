import matplotlib.pyplot as plt

Year = range(2021,2031)
Max_P_Aus = 6.224447*pow(10,6)
Max_P_Cad_2021_25 = 5.368300*pow(10,6)
Max_P_Cad_2025 = 6910900
Max_P_Ind = 9.276735*pow(10,6)
discount_rate = 0.08
n_year = 10

temp_Aus = 0
temp_Cad = 0
temp_Ind = 0

NPV_Aus = []
NPV_Cad = []
NPV_Ind = []

for i in range(n_year):
    temp_Aus = temp_Aus+(Max_P_Aus/pow(1+discount_rate,i))
    NPV_Aus.append(temp_Aus)
    temp_Ind = temp_Ind+(Max_P_Ind/pow(1+discount_rate,i))
    NPV_Ind.append(temp_Ind)
    if i<5:
        temp_Cad = temp_Cad+(Max_P_Cad_2021_25/pow(1+discount_rate,i))
        NPV_Cad.append(temp_Cad)
    else:
        temp_Cad = temp_Cad+(Max_P_Cad_2025/pow(1+discount_rate,i))
        NPV_Cad.append(temp_Cad)

fig = plt.figure(figsize=(10, 7))
plt.plot(Year, NPV_Aus, color="blue", marker='o')
plt.plot(Year, NPV_Cad, color="red", marker='o')
plt.plot(Year, NPV_Ind, color="brown", marker='o')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Net Present Value (NPV) in AUD', fontsize=14)
plt.legend(labels=['Australia', 'Canada', 'Indonesia'])


plt.show()



