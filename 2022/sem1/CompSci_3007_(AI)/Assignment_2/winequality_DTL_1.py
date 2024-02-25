import pandas as pd
import numpy as np
from collections import Counter
import sys

# Create a node class for DTL
class Node:
    def __init__(self, obj_feature_idx=None, split_val=None, left_subtree=None, right_subtree=None, information_gain=None, value=None):
        self.obj_feature_idx = obj_feature_idx
        self.split_val = split_val
        self.left_subtree = left_subtree
        self.right_subtree = right_subtree
        self.information_gain = information_gain
        self.value = value

    def is_leaf_node(self):
        return self.value is not None
    
class DecisionTreeLearning:
    '''
    Stopping Criteria :
        min_sample_split : minimum number of samples to allow for splitting
        max_depth : max depth of the decsion tree

    n_feats : either loop over all the features or loop over a subset of features that are randomly selected.
        In our case -
            we choose to do the greedy search
    '''
    def __init__(self, min_sample_split=2, max_depth=100, n_feats=None, random_forest=False):
        # Stopping critieria of the algo
        self.min_sample_split = min_sample_split
        self.max_depth = max_depth
        self.n_feats = n_feats
        self.root = None # keeping track of the root node in order to transverse the decision tree in the future
        self.random_forest = random_forest
    

    # 1 - Fit the given training dataset into a decision tree
    def model_fitting(self, train_X, train_Y):
        self.n_feats = train_X.shape[1] if not self.n_feats else min(self.n_feats, train_X.shape[1]) # it can never have > the max number of features in training data
        # Starts from the root node
        self.root = self.build_DecisionTree(train_X, train_Y)


    def build_DecisionTree(self, train_X, train_Y, depth=0):
        num_samples, num_features = train_X.shape
        n_labels = len(np.unique(train_Y))
            
        # Stopping Criteria - return a leaf node
        if (depth >= self.max_depth or n_labels == 1 or num_samples < self.min_sample_split):
            leaf_value = self.get_most_common_label(train_Y)
            return Node(value=leaf_value)

        feat_idxs = np.random.choice(num_features, self.n_feats, replace=False) # replace = False is to prevent the same feature idx from being picked

        # recursive greedy search
        # 2 - choose the best objective feature with the highest information gain calculation
        best_gain, best_feat, best_thresh = self.get_best_criteria(train_X, train_Y, feat_idxs)

        # Handle the case where best_thresh is None
        if best_thresh is None:
            best_thresh = np.median(train_X[:, best_feat])

        # 3 - use the best objective feature to split the data into a left and right subtrees, continue until a leaf node is formed
        left_idxs, right_idxs = self.get_split(train_X[:,best_feat], best_thresh)
        left = self.build_DecisionTree(train_X[left_idxs,:], train_Y[left_idxs], depth+1)
        right = self.build_DecisionTree(train_X[right_idxs,:], train_Y[right_idxs], depth+1)
        # if the left & right recursion stops where they become leaf nodes, return the node that forms them
        return Node(best_feat, best_thresh, left, right, best_gain)


    
    def get_most_common_label(self, Y):
        if len(Y) == 0:
            # Handle the case when Y is empty (no samples)
            return None  # or any default value you prefer
        counter = Counter(Y)
        most_common_label = counter.most_common(1)[0][0]
        return most_common_label

    def get_best_criteria(self, train_X, train_Y, feat_idxs):
        best_gain = -1
        split_idx, split_thresh = None, None

        for feat_idx in feat_idxs:
            column_X = train_X[:,feat_idx] # pick the objective feature and its data from train_X
            tresholds = np.unique(column_X) # we do not want to repeat the same data
            # Compare the information gain of every single numeric or yes/no data for the selected objective feature and pick out the biggest one
            for split_treshold in tresholds:
                gain = self.information_gain(train_Y, column_X, split_treshold)
                if(gain > best_gain):
                    best_gain = gain
                    split_idx = feat_idx
                    split_thresh = split_treshold
        
        return best_gain, split_idx, split_thresh

    # Calculates the entropy of the given set of samples
    def entropy(self, train_Y):
        p = np.unique(train_Y, return_counts = True)[1] # return a list of counts for each unique val in y
        p = p / np.sum(p) # return a list of prob for each unique val in y
        entropy = np.sum([-(prob * np.log2(prob)) for prob in p if prob > 0])
        return entropy

    def information_gain(self, train_Y, column_X, split_treshold):
        # parent entropy
        parent_entropy = self.entropy(train_Y)
        # generate split
        left_idxs, right_idxs = self.get_split(column_X, split_treshold)

        # If either the left or right subset is empty, it means that all samples ended up in one side of the split, and there is no actual split happening. In such cases, the information gain is set to 0.
        if(len(left_idxs) == 0 or len(right_idxs) == 0):
            return 0
        
        # weighted avg child entropy
        n = len(train_Y)
        n_l, n_r = len(left_idxs), len(right_idxs) # weights of each halves
        entropy_l, entropy_r = self.entropy(train_Y[left_idxs]), self.entropy(train_Y[right_idxs])
        child_entropy = (n_l/n)*(entropy_l) + (n_r/n)*entropy_r

        # information gain
        ig = parent_entropy - child_entropy
        return ig
 

    def get_split(self, column_X, split_treshold):
        left_idxs = np.argwhere(column_X <= split_treshold).flatten() # flatten the 2d arr into 1d arr
        right_idxs = np.argwhere(column_X > split_treshold).flatten()
        return left_idxs, right_idxs

    # Make prediction on the labels for the testing dataset
    def test_data_predict_labels(self, test_X):
        # each testing data will start from the root node
        test_data_predicted_labels = np.array([self._traverse_tree(x, self.root) for x in test_X])
        return test_data_predicted_labels
    
    def _traverse_tree(self, x, node : Node):
        if(node.is_leaf_node()):
            return node.value
    
        if(x[node.obj_feature_idx] <= node.split_val):
            return self._traverse_tree(x, node.left_subtree)
    
        return self._traverse_tree(x, node.right_subtree)


def parse_dataset_csv(path_to_dataset):
    data_frame = pd.read_csv(path_to_dataset)

    # Define data types for each column
    dtypes = {
        'fixed acidity': float,
        'volatile acidity': float,
        'citric acid': float,
        'residual sugar': float,
        'chlorides': float,
        'free sulfur dioxide': float,
        'total sulfur dioxide': float,
        'density': float,
        'pH': float,
        'sulphates': float,
        'alcohol': float,
        'quality': int,
        'Id': int
    }
    data_frame = data_frame.astype(dtypes)
    
    # Convert the Data Frame into numpy array
    numpy_array = data_frame.to_numpy()
    return numpy_array

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy
    
if __name__ == "__main__":
    from sklearn.model_selection import train_test_split

    path_to_training_dataset = None

    if len(sys.argv) >= 1:
        path_to_training_dataset = sys.argv[1]

    training_dataset = parse_dataset_csv(path_to_training_dataset)
    X, y = training_dataset[:,:-2], training_dataset[:,-2]
    train_X, test_X, train_Y, test_Y = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    DTL = DecisionTreeLearning()
    DTL.model_fitting(train_X, train_Y)

    # Test the model
    predicted_test_Y = DTL.test_data_predict_labels(test_X)

    # Check Accuracy against the test_Y
    print("Accuracy of predicted wine quality data : ", accuracy(test_Y, predicted_test_Y))
