import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.neighbors import KNeighborsClassifier

def PCA(Train_X, number_Component):
    # Compute the mean value of each feature and subtract the computed mean from each of the data corresponding to that feature 
    Centered_X = Train_X - np.mean(Train_X, axis=0)

    # Calculate the Covariance Matrix 
    covariance_Matrix = np.cov(Centered_X.T)

    # Use the Covariance Matrix to calculate the Eigenvectors and Eigenvalues 
    eigenvalues, eigenvectors = np.linalg.eig(covariance_Matrix)

    # Sort the Eigenvectors descendingly (Highest -> Lowest)
    sort_Index = np.argsort(eigenvalues)
    sort_Index = np.flip(sort_Index, axis=0)
    Eigenvalues = eigenvalues[sort_Index]
    S_Eigenvectors = eigenvectors[:, sort_Index]

    # Store the Eigenvectors with the highest Eigenvalues into the principal_Components 
    principal_Components = S_Eigenvectors[:, :number_Component]
    
    return principal_Components

def K_Means_Clustering(Train_X, K, Fixed_Centroids_Indices, max_iterations, Optimisation):
    # Set a fix centroid 
    Centroids = Train_X[Fixed_Centroids_Indices, :]

    # Calculate the Euclidean Distance of each data point in X from every Centroids (Step 2)
    dist_Between_Data_Centroids = pairwise_distances(Train_X, Centroids, 'euclidean')

    # Extract the indices of the data points with the smallest Euclidean distance (Step 3)
    Cluster_Indices = np.argmin(dist_Between_Data_Centroids, axis=1)
    Temp_Sum = 0

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

        Cluster_Indices = New_Cluster_Indices
    return Cluster_Indices, Centroids

def Check_Percentage_Of_Labels_In_Clusters(Fixed_Centroids_Indices, K, Clusters, Centroids, Scaled_X):
    train_Y = []
    Fixed_Y = []
    Percentage_In = []
    Average_Percent = 0
    Temp_Sum = 0
    
    for i in range(K):
        train_Y.append(Scaled_X[Clusters == i])
    
    for i_2 in Fixed_Centroids_Indices:
        Fixed_Y.append(Scaled_X[i_2])

    for iter in range(len(train_Y)):
        Temp_Y = train_Y[iter]
        Temp_Fixed_Y = Fixed_Y[iter]
        for num in range(Temp_Y.shape[0]):
            for num_2 in range(Temp_Y.shape[1]):
                if Temp_Y[num, num_2] == Temp_Fixed_Y[num_2]:
                    Temp_Sum += 1
        Percentage_In.append(Temp_Sum/Temp_Y.shape[0])
        Temp_Sum = 0

    Average_Percent = np.sum(Percentage_In)/K

    return Average_Percent

# Import The Dataset 
Training_dataset = pd.read_csv("mnist_train.csv", header=None)
Testing_dataset = pd.read_csv("mnist_test.csv", header=None) 
Train_Y = np.squeeze(np.asarray(Training_dataset.iloc[:,[0]]))
Test_Y = np.squeeze(np.asarray(Testing_dataset.iloc[:,[0]]))
Train_X = Training_dataset.iloc[:, 1::]
Test_X = Testing_dataset.iloc[:, 1::]


Percentage = []
K = 10
Error_Container = []
# # Set a random but fixed centroids 
random_Centroids_Indices = np.random.choice(Train_X.shape[0], K, replace=False)

for index in range(10, 256+1):
    # Compute the PCA for the traning_X data  
    PC = PCA(Train_X, index)
    Train_Centered_X = Train_X - np.mean(Train_X, axis=0)   # Compute the mean value of each feature and subtract the computed mean from each of the data corresponding to that feature 
    Scaled_Train_X = np.dot(Train_Centered_X, PC).real      # Projecting the Centered Traning_X data onto the PC

    # Handling the test dataset 
    Test_Centered_X = Test_X - np.mean(Test_X, axis=0)
    Scaled_Test_X = np.dot(Test_Centered_X, PC).real # Project the Centered Test_X data onto the Train_X data Principal Component 

    #Perform PCA on the Training X data 
    Centered_X = Train_X - np.mean(Train_X, axis=0)
    PCA_X = PCA(Train_X, index)
    Scaled_X = np.dot(Centered_X, PCA_X).real
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(Scaled_Train_X, Train_Y)
    y_pred = classifier.predict(Scaled_Test_X)

    # Perform K_Means_Clustering on each of the reduced dimension data
    Clusters, Centroids = K_Means_Clustering(Scaled_X, K, random_Centroids_Indices, 100, True)

    Percent = Check_Percentage_Of_Labels_In_Clusters(random_Centroids_Indices, K, Clusters, Centroids, Scaled_X)
    Percentage.append(Percent)

    temp_Accuracy = np.full(len(Test_X),0)

    for iterator in range(len(y_pred)):
        if y_pred[iterator] == Test_Y[iterator]:
            temp_Accuracy[iterator] = 1

    Error_Container.append((np.sum(temp_Accuracy)/len(Test_Y)-0.4589))

fig_1 = plt.figure(figsize=(10,10))
ax0 = fig_1.add_subplot(111)
ax0.plot(range(len(Error_Container)), Error_Container, '-b')
ax0.set_ylabel("Average Percentage of Labels in each Clusters")
ax0.set_xlabel("Number of dimensions")

plt.show()