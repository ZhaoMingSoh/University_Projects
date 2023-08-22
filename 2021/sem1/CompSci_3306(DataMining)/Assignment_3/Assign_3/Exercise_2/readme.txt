Description About the K_Means Algorithm: 
-----------------------------------------------------------------------------------------------------
Step 1: Randomly assign k=3 iris data points as the initial centroids.
Step 2: Assign each and every data points in the iris dataset to one of the k clusters such that the Euclidean distance is the smallest between the data point and all k centroids of the k clusters. 
Step 3: Recompute the centroids of k clusters.
Step 4: Repeat Step 2 and 3 until the centroids converge. How? The convergence is determined by the treshold, "difference between the old_centroids and the new_centroids". 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To run the K_Means_Algorithm.py:

1. Key in "python K_Means_Algroithm.py" in the terminal command interface and click enter. 
2. Outputs: 
	a) 2 two-dimensional plots: "one is the plot of the first 2 features/dimension of the iris dataset before K_means" and "one is the plot of convergence after K-means"
	b) In the command, you will be given the number of rounds that it takes for that particular iteration of initial centroids to converge and a table of all the centroids in each round. 
		 