import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

def check_symmetric(a, rtol=1e-05, atol=1e-08):
    return np.allclose(a, a.T, rtol=rtol, atol=atol)

class PCA:
    def __init__ (self, desired_Number_Components):
        self.desired_Number_Components = desired_Number_Components
        self.principal_Components = None
        self.mean_Values = None

    def construct_PC(self, Train_X):
        # Calculate the Mean and subtract the Mean from each of the 
        self.mean_Values = np.mean(Train_X, axis=0)
        Centered_Train_X = Train_X - self.mean_Values

        # Calculate the Covariance Matrix 
        covariance_Matrix = np.cov(Centered_Train_X.T)
        # covariance_Matrix = pd.DataFrame(covariance_Matrix)
        # covariance_Matrix.replace(np.nan, 0)
        print("Covariance_Matrix :", np.iscomplexobj(covariance_Matrix))
        print(check_symmetric(covariance_Matrix))

        # Use the Covariance Matrix to calculate the Eigenvectors and Eigenvalues 
        EigenValues, EigenVectors = np.linalg.eig(covariance_Matrix)

        # Sort the Eigenvectors descendingly (Highest -> Lowest)
        EigenVectors = EigenVectors.T
        Index =  np.argsort(EigenValues)
        Index = np.flip(Index, axis=0)
        EigenValues = EigenValues[Index]
        EigenVectors = EigenVectors[Index]

        # Store the Eigenvectors with the highest Eigenvalues into the principal_Components 
        self.principal_Components = EigenVectors[0:self.desired_Number_Components]

    def Projection(self, Train_X):
        Centered_Train_X = Train_X - self.mean_Values
        return np.dot(Centered_Train_X, self.principal_Components.T)

# Import The Dataset 
Training_dataset = pd.read_csv("mnist_train.csv")
Testing_dataset = pd.read_csv("mnist_test.csv") 
Training_Y = np.squeeze(np.asarray(Training_dataset.iloc[:,[0]]))
Testing_Y = np.squeeze(np.asarray(Testing_dataset.iloc[:,[0]]))
Train_X = Training_dataset.iloc[:, 1::]
Test_X = Testing_dataset.iloc[:, 1::]

print("Test_X :", Test_X.shape)

# print("Training_X :", Training_X.shape)
# print("Training_Y :", Training_Y.shape)
# print("Testing_X :", Testing_X.shape)
# print("Testing_Y :", Testing_Y.shape)

# # Standaridize the dataset 
# st_Scaler = StandardScaler()
# st_Scaler.fit(Training_X.iloc[:, 1::])

# Scaled_Train_X = st_Scaler.transform(Training_X.iloc[:, 1::])
# Scaled_Test_X = st_Scaler.transform(Testing_X.iloc[:, 1::])

# print("Scaled_Train_X :", Scaled_Train_X.shape)
# print("Scaled_Test_X :", Scaled_Test_X.shape)

# # Run the PCA on the training_X dataset 
# pca_1 = PCA(2)
# pca_1.construct_PC(Scaled_Train_X)
# PC_Training_X = pca_1.Projection(Scaled_Train_X)


# # pca_2 = PCA(2)
# # pca_2.construct_PC(Scaled_Test_X)
# PC_Testing_X = pca_2.Projection(Scaled_Test_X)

number_Of_reduced_Dimension = 20
starting_reduced_Dimension = 10
KNN_Accuracy = []
# num_X, num_Y = np.shape(Scaled_Test_X)
num_X, num_Y = np.shape(Test_X)
temp_Accuracy = np.full(num_X, 0)

# print(Scaled_Test_X.shape)
# print(temp_Accuracy.shape)
# 1-Nearest Neighbour Classifier 
# for i in range(starting_reduced_Dimension, number_Of_reduced_Dimension+1):
# Use PCA on both the testing data and training data
pca_1 = PCA(256)
pca_1.construct_PC(Train_X)
PC_Training_X = pca_1.Projection(Train_X)
PC_Training_X = PC_Training_X.real

pca_2 = PCA(256)
pca_2.construct_PC(Test_X)
PC_Testing_X = pca_2.Projection(Test_X)
PC_Testing_X = PC_Testing_X.real

# print("Scaled_Test_X :", np.iscomplexobj(Scaled_Train_X))
print("PC_Training_X :", np.iscomplexobj(PC_Training_X))

# print("Scaled_Test_X :", np.iscomplexobj(Scaled_Test_X))
print("PC_Testing_X :", np.iscomplexobj(PC_Testing_X))

KNN = KNeighborsClassifier(n_neighbors=1)
KNN.fit(PC_Training_X, np.ravel(Training_Y))
predict_Label = KNN.predict(PC_Testing_X)

print("predict_Label :", predict_Label.shape)

# print("predict_Label :",predict_Label.shape)
# print("Temp_Accuracy :", temp_Accuracy.shape)
# print("Testing_Y :", Testing_Y.shape)

# Calculate the accuracy rate 
for iterator in range(len(predict_Label)):
    if predict_Label[iterator] == Testing_Y[iterator]:
        temp_Accuracy[iterator] = 1

print(temp_Accuracy.shape)
print(len(Testing_Y))
print(np.sum(temp_Accuracy)/len(Testing_Y))
# KNN_Accuracy.append(np.sum(temp_Accuracy)/len(Testing_Y))

# print(KNN_Accuracy)

# print("predict_Label", predict_Label.shape)
# print(PC[:,[0]])
# print(PC[:,[1]])
# plt.scatter(PC[:,[0]], PC[:,[1]], edgecolor='none', alpha=0.8, cmap=plt.cm.get_cmap('viridis', 3))
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.show()






    