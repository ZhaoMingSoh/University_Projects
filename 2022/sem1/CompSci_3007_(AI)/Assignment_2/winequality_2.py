import numpy as np
from collections import Counter
import sys

# Create a node class for DTL
class Node:
    def __init__(self, obj_feature_idx=None, split_val=None, left_subtree=None, right_subtree=None, information_gain=None, label=None):
        self.obj_feature_idx = obj_feature_idx
        self.split_val = split_val
        self.left_subtree = left_subtree
        self.right_subtree = right_subtree
        self.information_gain = information_gain
        self.label = label # leaf_node label
    
class DecisionTreeLearning:
    def __init__(self, min_sample_split=2, max_depth=100):
        # Stopping critieria of the algo
        self.min_sample_split = min_sample_split
        self.max_depth = max_depth
        self.root = None # keeping track of the root node in order to transverse the decision tree in the future
    

    # Fit the given training dataset into a decision tree
    def model_fitting(self, depth, training_dataset=None):
        # Separate the Objective features and Labels from the dataset
        train_X = training_dataset[1:,:-1].astype("float")
        train_y = training_dataset[1:,-1].astype("int")

        self.root = self.build_DecisionTree(depth, train_X, train_y)


    def build_DecisionTree(self, depth, train_X, train_y):
        number_features = train_X.shape[1]
        number_samples = train_X.shape[0]

        # Recursive Criteria
        if number_samples >= self.min_sample_split and depth <= self.max_depth:
            # Find the best split value
            best_obj_feature_idx, best_split_val, best_info_gain, best_left_subtree_idx, best_right_subtree_idx = self.get_best_SplitVal(number_features=number_features, train_X=train_X, train_y=train_y)
            
            if best_info_gain > 0:
                left_subtree = self.build_DecisionTree(depth+1, train_X[best_left_subtree_idx,:], train_y[best_left_subtree_idx])
                right_subtree = self.build_DecisionTree(depth+1, train_X[best_right_subtree_idx,:], train_y[best_right_subtree_idx])

                # Once I got the best objective feature and its corresponding split value, we create a node with those information
                best_node = Node(obj_feature_idx=best_obj_feature_idx, split_val=best_split_val, left_subtree=left_subtree, right_subtree=right_subtree, information_gain=best_info_gain)
                return best_node

        leaf_label = Counter(train_y).most_common(1)[0][0]
        leaf_node = Node(label=leaf_label)
        return leaf_node
        

    def get_best_SplitVal(self, number_features, train_X, train_y):
        best_info_gain, best_obj_feature_idx, best_split_val = -1, None, None
        best_left_subtree_idx , best_right_subtree_idx = None, None
        # 1) Loop through each of the objective features (f_acid, v_acid, res_sugar, ..... )
        for feature_idx in range(number_features):
            feature_vals = np.unique(train_X[:,feature_idx])
            mean_feature_vals = self.get_mean_splitval(feature_vals)
            # 3) Test how well the currently selected objective feature val splits the samples into 2 subtrees
            for split_val in mean_feature_vals:
                # 3.a) split the samples into the left and right subtrees
                left_subtree_idx = np.where(train_X[:,feature_idx] <= split_val)[0]
                right_subtree_idx = np.where(train_X[:,feature_idx] > split_val)[0]

                # 3.b) calculates the information gain of the objective feature with the current subtrees
                info_gain = self.information_gain(train_y, left_subtree_idx, right_subtree_idx)

                # 3.c) stores the best feature with its best feature value given that it has the best info gain
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    best_split_val = split_val
                    best_obj_feature_idx = feature_idx
                    best_left_subtree_idx = left_subtree_idx
                    best_right_subtree_idx = right_subtree_idx
            
        return best_obj_feature_idx, best_split_val, best_info_gain, best_left_subtree_idx, best_right_subtree_idx

    # Calculates the average of every 2 elements for the list of all possible feature values of the current objective feature
    def get_mean_splitval(self, feature_vals):
        mean_splitval = []
        feature_vals_size = len(feature_vals)
        for val in range(1, feature_vals_size):
            first_val = feature_vals[val-1]
            second_val = feature_vals[val]
            mean_splitval.append((first_val + second_val)/2)
        return mean_splitval

    # Calculates the entropy of the given set of samples
    def entropy(self, train_y):
        p = np.unique(train_y, return_counts = True)[1] # return a list of counts for each unique val in y
        p = p / np.sum(p) # give us the probability of each unique val in y
        entropy = np.sum([-(prob * np.log2(prob)) for prob in p])
        return entropy

    # Calculates the sum of the entropy of all the branches of the Decision Tree node
    def remainder(self, train_y, left_subtree_idx, right_subtree_idx):
        num_samples_at_R = len(left_subtree_idx) + len(right_subtree_idx)
        prob_of_each_subtrees = [len(left_subtree_idx)/num_samples_at_R, len(right_subtree_idx)/num_samples_at_R]
        entropy_at_each_subtrees = [self.entropy(train_y[left_subtree_idx]), self.entropy(train_y[right_subtree_idx])]
        remainder_at_each_subtrees = zip(prob_of_each_subtrees, entropy_at_each_subtrees)
        sum_remainder = np.sum([s_p*s_e for s_p, s_e in remainder_at_each_subtrees])
        return sum_remainder

    def information_gain(self, train_y, left_subtree_idx, right_subtree_idx):
        # Make sure when the y training dataset is indexed from 1 not from 0 as the 0 is the feature's name
        parent_entropy = self.entropy(train_y)
        remainder = self.remainder(train_y, left_subtree_idx, right_subtree_idx)
        info_gain = parent_entropy - remainder
        return info_gain

    # Make prediction on the labels for the testing dataset
    def test_data_predict_labels(self, test_dataset_X):
        test_dataset_X = test_dataset_X[1:,:].astype('float')
        test_data_predicted_labels = []
        tree_node = None

        # Go through each row of the testing dataset - each row also refer to one sample
        for row in test_dataset_X:
            tree_node = self.root # Always start from the root node of the Decision Tree
            # Recursively go through the Decision Tree until a leaf node is reached -> this will return a label for the corresponding testing data
            while tree_node.label == None:
                objective_feature_idx = tree_node.obj_feature_idx
                split_val = tree_node.split_val
                if row[objective_feature_idx] <= split_val:
                    tree_node = tree_node.left_subtree
                elif row[objective_feature_idx] > split_val:
                    tree_node = tree_node.right_subtree
            test_data_predicted_labels.append(tree_node.label)
        return test_data_predicted_labels

# Parses the data from the .txt file into 2d numpy array format
def parse_dataset(path_to_dataset):
    decoy_dataset = []
    # Read the training data in
    with open(path_to_dataset) as train:
        temp = train.readline()
        while temp:
            line = (temp.strip()).split()
            decoy_dataset.append(line)
            temp = train.readline()

    training_dataset = np.array(decoy_dataset)
    return training_dataset

if __name__ == "__main__":
    path_to_training_dataset, path_to_testing_dataset, minleaf = None, None, None

    if len(sys.argv) >= 1:
        path_to_training_dataset = sys.argv[1]
        path_to_testing_dataset = sys.argv[2]
        minleaf = sys.argv[3]

    training_dataset = parse_dataset(path_to_training_dataset)
    testing_dataset = parse_dataset(path_to_testing_dataset)

    DCL = DecisionTreeLearning(min_sample_split=int(minleaf))
    DCL.model_fitting(0,training_dataset)
    predicted_labels = DCL.test_data_predict_labels(test_dataset_X=testing_dataset)
    for pred in predicted_labels:
        print(pred)