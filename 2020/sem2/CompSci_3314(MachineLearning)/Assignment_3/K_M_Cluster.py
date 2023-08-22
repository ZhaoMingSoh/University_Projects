import numpy as np

def Euclidean_Distance(p1, p2):
    return np.sqrt(np.sum((p1+p2)**2))

class K_Means_C:

    def __init__(self, K, Num_Iteration):
        self.K = K
        self.Num_Iteration = Num_Iteration

        # List of sample indices for each cluster 
        self.clusters = [[] for _ in range(self.K)]

        # mean feature vector for each cluster 
        self.centroids = []

    def predict(self, Train_X):
        self.Train_X = Train_X
        self.n_samples, self.n_features = Train_X.shape # Extract the dimensions of the training X dataset

        # Pick random points as initial centroid 
        random_centroid_Indices = np.random.choice(self.n_samples, self.K, replace=False) # This will be an array of size self.K, This will pick a random number between 0 and the self.n_samples
        self.centroids = [self.Train_X[i] for i in random_centroid_Indices] # Now assign the chosen samples to the centroids 

        # Optimization
        for _ in range(self.Num_Iteration):
            # Update Clusters 
            self.clusters = self._create_clusters(self.centroids)

            # Update Centroids
            centroids_Old = self.centroids
            self.centroids = self._get_centroids(self.clusters) # Assign the mean of the clusters to the centroid 

            # Check for convergence 

        # Return clusters label 

    def _create_clusters(self, centroids):
        self.clusters = [[] for _ in range(self.K)]
        for index, sample in enumerate(self.Train_X):
            centroid_Idx = self._closest_centroid(sample, centroids)
            # Take the index of the current cluster and then put the current sample index in the closest clusters
            clusters[centroid_Idx].append(index)
        return clusters 

    def _closest_centroid(self, sample, centroids):
        # Calculate the closest distance of the current sample to each centroid
        # Then get the index of the centroid that has the closest distance 
        distances = [Euclidean_Distance(sample, point) for point in centroids]
        # Find the index with the minimum distance 
        closest_Idx = np.argmin(distances)
        return closest_Idx

    def _get_centroid(self, clusters):
        centroids = np.zeros((self.K, self.n_features))
        for clusters_idx, cluster in enumerate(clusters):
            cluster_mean = np.mean(self.Train_X[cluster], axis=0)
            
