import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rd

# Import The Dataset 
Training_dataset = pd.read_csv("mnist_train.csv", header=None)
Testing_dataset = pd.read_csv("mnist_test.csv", header=None) 
Train_Y = np.squeeze(np.asarray(Training_dataset.iloc[:,[0]]))
Test_Y = np.squeeze(np.asarray(Testing_dataset.iloc[:,[0]]))
Train_X = Training_dataset.iloc[:, 1::]
Test_X = Testing_dataset.iloc[:, 1::]

Num_Sam = Train_X.shape[0]
Num_Feature = Train_X.shape[1]

class K_Means_Clustering:

    def __init__(self, K, Train_X):
        self.K = K
        self.Train_X = Train_X
        self.Centroids = np.array([]).reshape(Num_Feature,0)
        self.Results = {}

    def Construct_Centroid(self, K, Train_X):
        # Initialise random points from the data as the initial centroids
        i=rd.randint(0,Num_Sam)
        random_centroid_Indices = np.random.choice(Num_Sam, K, replace=False) 
        Temp_Centroid = np.array([Train_X[random_centroid_Indices]])

    def Print(self):
        print(self.Centroids.shape)

K_Means = K_Means_Clustering(3, Train_X)
K_Means.Construct_Centroid(3, Train_X)
K_Means.Print()