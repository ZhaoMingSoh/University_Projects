import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from tabulate import tabulate

def euclidean_distance(one,two):
    return np.sqrt(np.sum(np.square(one-two)))

def Assigning_Data_Points(data, centroid):
    cluster = np.zeros(len(data))
    for i in range(len(data)):
        temp = []
        for j in range(len(centroid)):
            temp.append(euclidean_distance(data[i], centroid[j]))
        idx = np.argmin(temp) # returns the index of the smallest euclidean distance out of the 3 cluster 0, 1 and 2
        cluster[i] = idx

    return cluster

iris = load_iris()
data = iris.data[:,:2] #Slice the iris dataset of 150x4 to 150x2 (pick the first 2 features)

Store_All_Centroid = []

def K_Means(data, k):

    # Step 1: Randomly Assign K data points as the Initiali Centroids.
    random = np.random.choice(len(data), k, replace=False)
    centroid = data[random,:2]
    Store_All_Centroid.append(centroid)

    # Step 2: Compare the distance of all the data points to each of the centroid, and assign the data points to one of the k cluster that has the smallest euclidean distance between itself and one of the k centroids
    cluster = Assigning_Data_Points(data, centroid)

    iter = 1
    difference_In_Centroid = 100 

    # Step 4: Repeat Step 2 to 3 untill the difference between the old centroid and the new centroids are less than 0.0001 
    while difference_In_Centroid > 0.0001:
        # Step 3: Calculate the new Centroid of each of the k clusters
        New_Centroid = []
        temp_Diff = 0 # variable for storing the euclidean distance between the old and new centroids
        
        ## For each cluster k, find all the mean of all the data points that correspond to that cluster k.  
        for k_ in range(k):
            temp_sum = 0
            temp_tracker = 0
            for x in range(len(cluster)):
                if k_ == cluster[x]:
                    temp_sum += data[x];
                    temp_tracker += 1
            New_Centroid.append(temp_sum/temp_tracker) 
        
        # Find the best number of Rounds where the difference between the old and new centroids are at the minimum 
        for old, new in zip(centroid, New_Centroid):
            temp_Diff += euclidean_distance(old,new)
        difference_In_Centroid = temp_Diff

        Store_All_Centroid.append(New_Centroid)
        centroid = New_Centroid
        cluster = Assigning_Data_Points(data, centroid)
        iter+=1

    return cluster, centroid, iter
        
# The Main
# Plot - iris data before K-Means Clustering 
fig_1 = plt.figure(figsize=(8,8))
Iris_Before =  fig_1.add_subplot(111)
Iris_Before.scatter(data[:,0],data[:,1])
Iris_Before.set_xlabel('Sepal length')
Iris_Before.set_ylabel('Sepal width')

# Run the K_Means on the iris dataset
final_Cluster, final_Centroid, number_Rounds = K_Means(data, 3)

print("Number of Rounds: ",number_Rounds)
print(tabulate(Store_All_Centroid,headers=['Centroid 1', 'Centroid 2', 'Centroid 3']))

# Plot - iris data after clustering 
fig_2 = plt.figure(figsize=(8,8))
Iris_After = fig_2.add_subplot(111)
for j in range(3):
    Iris_After.scatter(data[final_Cluster == j , 0] , data[final_Cluster == j , 1] , label = j)

# Due to the centroid being a nested list multi-dimensional slicing does not work, centroid[:,1] == Error.
# Instead, we convert the nested list into an N-dimensional datasey via np.array()
final_Centroid = np.array(final_Centroid)
Iris_After.scatter(final_Centroid[:,0], final_Centroid[:,1], marker="D")
Iris_After.set_xlabel('Sepal length')
Iris_After.set_ylabel('Sepal width')
Iris_After.legend(['setosa: 0', 'versicolor: 1', 'virginica: 2'])

plt.show()