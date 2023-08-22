import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances

# Import The Dataset 
Training_dataset = pd.read_csv("mnist_train.csv", header=None)
Testing_dataset = pd.read_csv("mnist_test.csv", header=None) 
Train_Y = np.squeeze(np.asarray(Training_dataset.iloc[:,[0]]))
Test_Y = np.squeeze(np.asarray(Testing_dataset.iloc[:,[0]]))
Train_X = Training_dataset.iloc[:, 1::]
Test_X = Testing_dataset.iloc[:, 1::]

# Task 3
def K_Means_Clustering(Train_X, K, max_iterations, Optimisation):
    Train_X = Train_X.values

    # Generate Random Initial Centroids (Step 1)
    random_Centroids_Indices = np.random.choice(Train_X.shape[0], K, replace=False)
    Centroids = Train_X[random_Centroids_Indices, :]

    # Calculate the Euclidean Distance of each data point in X from every Centroids (Step 2)
    dist_Between_Data_Centroids = pairwise_distances(Train_X, Centroids, 'euclidean')

    # Extract the indices of the data points with the smallest Euclidean distance (Step 3)
    Cluster_Indices = np.argmin(dist_Between_Data_Centroids, axis=1)
    Temp_Sum = 0
    max_iterations_Clusters = []

    # Run the above Step 2 and Step 3 repeatedly for max_iterations (Step 4)
    for _ in range(max_iterations):
        for i in range(K):
                Centroids[i] = Train_X[Cluster_Indices==i,:].mean(axis=0)
      
        New_dist_Between_Data_Centroids = pairwise_distances(Train_X, Centroids, 'euclidean')
        New_Cluster_Indices = np.argmin(New_dist_Between_Data_Centroids, axis=1)

        if Optimisation == True:
            for row in range(Cluster_Indices.shape[0]):
                    if(Cluster_Indices[row] == New_Cluster_Indices[row]):
                        Temp_Sum += 1
            if(Temp_Sum/(Cluster_Indices.shape[0]) == 1): 
                break
            Temp_Sum = 0

        max_iterations_Clusters.append(New_Cluster_Indices)
        Cluster_Indices = New_Cluster_Indices
    return Cluster_Indices, Centroids, max_iterations_Clusters

def Sum_Of_Squares_In_Each_Cluster(Cluster_Indices, Centroids, Train_X):
    Train_X = Train_X.values
    Individual_Clusters_Train_X = []
    Temp_Sum = 0
    Temp_Arr = []
    Variances = []
    for i in range(Centroids.shape[0]):
        Individual_Clusters_Train_X.append(Train_X[Cluster_Indices==i, :])

    for each in range(len(Individual_Clusters_Train_X)):
        Temp_Arr = Individual_Clusters_Train_X[each]
        Temp_Sum = np.sum((Temp_Arr - Centroids[each])**2)
        Variances.append(Temp_Sum)
        Temp_Sum = 0

    return Variances

Variances = []
Iterations = []

Iterations_2 = []
Clusters_2 = []
Centroids_2 = []
Var_2 = []

# Running a range of K and checking out the different variances of each K
for k in range(1, 151):
    Clusters, Centroids, Iterations = K_Means_Clustering(Train_X, k, 100, True)
    Variance = Sum_Of_Squares_In_Each_Cluster(Clusters, Centroids, Train_X)
    Variances.append(np.sum(Variance))

# Check the Sum of Squares Deviation for K=10
Clusters_2, Centroids_2, Iterations_2 = K_Means_Clustering(Train_X, 10, 100, False)
for num in range(len(Iterations_2)):
    Var_2.append(np.sum(Sum_Of_Squares_In_Each_Cluster(Iterations_2[num], Centroids_2, Train_X)))

fig_1 = plt.figure(figsize=(10,10))
first_Plot = fig_1.add_subplot(111)
first_Plot.plot(Variances)
first_Plot.set_ylabel("Sum Of Squares Deviations (Error/Cost)")
first_Plot.set_xlabel("Value of K")

fig_2 = plt.figure(figsize=(10,10))
sec_Plot = fig_2.add_subplot(111)
sec_Plot.plot(Var_2)
sec_Plot.set_ylabel("Sum Of Squares Deviations (Error/Cost)")
sec_Plot.set_xlabel("Number of Iterations")

plt.show()

