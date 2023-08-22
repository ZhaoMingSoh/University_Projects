import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

# Task 1
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

# Import The Dataset 
Training_dataset = pd.read_csv("mnist_train.csv", header=None)
Testing_dataset = pd.read_csv("mnist_test.csv", header=None) 
Train_Y = np.squeeze(np.asarray(Training_dataset.iloc[:,[0]]))
Test_Y = np.squeeze(np.asarray(Testing_dataset.iloc[:,[0]]))
Train_X = Training_dataset.iloc[:, 1::]
Test_X = Testing_dataset.iloc[:, 1::]

fig = plt.figure(figsize=(10,10))
ax0 = fig.add_subplot(111)

max_PC = 254
Error_Container = []

# Task 2
for index in range(10, max_PC+1):
    # Compute the PCA for the traning_X data  
    PC = PCA(Train_X, index)
    Train_Centered_X = Train_X - np.mean(Train_X, axis=0)   # Compute the mean value of each feature and subtract the computed mean from each of the data corresponding to that feature 
    Scaled_Train_X = np.dot(Train_Centered_X, PC).real      # Projecting the Centered Traning_X data onto the PC

    # Handling the test dataset 
    Test_Centered_X = Test_X - np.mean(Test_X, axis=0)
    Scaled_Test_X = np.dot(Test_Centered_X, PC).real # Project the Centered Test_X data onto the Train_X data Principal Component 

    # 1-Nearest Neighbour Classifier 
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(Scaled_Train_X, Train_Y)
    y_pred = classifier.predict(Scaled_Test_X)

    temp_Accuracy = np.full(len(Test_X),0)

    for iterator in range(len(y_pred)):
        if y_pred[iterator] == Test_Y[iterator]:
            temp_Accuracy[iterator] = 1

    Error_Container.append(1-(np.sum(temp_Accuracy)/len(Test_Y)))

# 1-Nearest Neighbour Performance with different number of principal component 
ax0.plot(range(len(Error_Container)), Error_Container, '-b')
ax0.set_xlabel('Number of Principal Components')
ax0.set_ylabel('1-Nearest-Neighbours Accuracy')
ax0.set_title('1-Nearest Neighbour Performance with different number of principal component')

plt.show()