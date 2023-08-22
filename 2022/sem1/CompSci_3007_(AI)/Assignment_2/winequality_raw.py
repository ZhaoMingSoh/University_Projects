import numpy as np
from collections import Counter
import sys

# count_ = 0

# Create a node class for DTL
class Node:
    def __init__(self, obj_feature_idx=None, split_val=None, left_subtree=None, right_subtree=None, information_gain=None, depth_level=None, bool_left = False, bool_right = False, label=None):
        self.obj_feature_idx = obj_feature_idx
        self.split_val = split_val
        self.left_subtree = left_subtree
        self.right_subtree = right_subtree
        self.information_gain = information_gain
        self.depth_level = depth_level
        self.bool_left = bool_left
        self.bool_right = bool_right
        self.label = label # leaf_node label
    
class DecisionTreeLearning:
    def __init__(self, min_sample_split=2, max_depth=30):
        # Stopping critieria of the algo
        self.min_sample_split = min_sample_split
        self.max_depth = max_depth
        self.root = None # keeping track of the root node in order to transverse the decision tree in the future
    

    # Fit the given training dataset into a decision tree
    def model_fitting(self, depth, training_dataset=None):
        # Separate the Objective features and Labels from the dataset
        train_X = (training_dataset[1:,:number_features]).astype('float')
        train_y = (training_dataset[1:,number_features]).astype('int')

        self.root = self.build_DecisionTree(depth, train_X, train_y)


    def build_DecisionTree(self, depth, train_X, train_y, bool_left=False, bool_right=False):
        number_features = train_X.shape[1]
        number_samples = train_X.shape[0]
        # global count_
        # count_ += 1
        # print(f"count : {count_}")

        # Recursive Criteria
        if number_samples >= self.min_sample_split and depth <= self.max_depth:
            # Find the best split value
            best_obj_feature_idx, best_split_val, best_info_gain, best_left_subtree_idx, best_right_subtree_idx = self.get_best_SplitVal(number_features=number_features, train_X=train_X, train_y=train_y)
            # print("\n")
            # print(f"Best_Obj_Feature_idx = {best_obj_feature_idx}, Best_Split_Val = {best_split_val}, Best_Info_Gain = {best_info_gain}")
            
            if best_info_gain > 0:
                # best_left_subtree_idx = np.where(train_X[:, best_obj_feature_idx] <= best_split_val)[0]
                # best_right_subtree_idx = np.where(train_X[:, best_obj_feature_idx] > best_split_val)[0]
                # print(f"best_left_subtree_idx : {best_left_subtree_idx}")
                # print("new_left_train_X :")
                # print(train_X[best_left_subtree_idx])
                # print(f"new_left_train_y : {train_y[best_left_subtree_idx]}")
                
                left_subtree = self.build_DecisionTree(depth+1, train_X[best_left_subtree_idx,:], train_y[best_left_subtree_idx], bool_left=True)
                # print(f"best_right_subtree_idx : {best_right_subtree_idx}")
                # print("new_right_train_X :")
                # print(train_X[best_right_subtree_idx])
                # print(f"new_right_train_y : {train_y[best_right_subtree_idx]}")
                right_subtree = self.build_DecisionTree(depth+1, train_X[best_right_subtree_idx,:], train_y[best_right_subtree_idx], bool_right=True)

                # Once I got the best objective feature and its corresponding split value, we create a node with those information
                best_node = Node(obj_feature_idx=best_obj_feature_idx, split_val=best_split_val, left_subtree=left_subtree, right_subtree=right_subtree, information_gain=best_info_gain, depth_level=depth, bool_left=bool_left, bool_right=bool_right)
                return best_node

        leaf_label = Counter(train_y).most_common(1)[0][0]
        # print(f"leaf_label : {leaf_label}")
        leaf_node = Node(depth_level = depth,label=leaf_label, bool_left=bool_left, bool_right=bool_right)

        return leaf_node
        

    def get_best_SplitVal(self, number_features, train_X, train_y):
        # count = 0
        best_info_gain, best_obj_feature_idx, best_split_val = -1, None, None
        best_left_subtree_idx , best_right_subtree_idx = None, None
        # 1) Loop through each of the objective features (f_acid, v_acid, res_sugar, ..... )
        for feature_idx in range(number_features):
            # count = 0
            # print('-'*100)
            # print(f"feature_idx : {feature_idx}")
            # 2) Store all the unique values of the "selected" objective feature
            feature_vals = np.unique(train_X[:,feature_idx])
            mean_feature_vals = self.get_mean_splitval(feature_vals)
            # print(f"feature_vals : {feature_vals}")
            # print(mean_feature_vals)
            # 3) Test how well the currently selected objective feature val splits the samples into 2 subtrees
            for split_val in mean_feature_vals:
                # count += 1
                # print("\n")
                # print(f"Count = {count}")
                # print(f"split_val = {split_val}")
                # 3.a) split the samples into the left and right subtrees
                left_subtree_idx = np.where(train_X[:,feature_idx] <= split_val)[0]
                right_subtree_idx = np.where(train_X[:,feature_idx] > split_val)[0]

                # if len(left_subtree_idx)>0 and len(right_subtree_idx)>0:
                # print(f"left_subtree_idx = {left_subtree_idx}")
                # print(f"right_subtree_idx = {right_subtree_idx}")
                    # 3.b) calculate the information gain of the objective feature with the current subtrees
                info_gain = self.information_gain(train_y, left_subtree_idx, right_subtree_idx)

                # print(f"info_gain = {info_gain}")
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    best_split_val = split_val
                    best_obj_feature_idx = feature_idx
                    best_left_subtree_idx = left_subtree_idx
                    best_right_subtree_idx = right_subtree_idx
            
        return best_obj_feature_idx, best_split_val, best_info_gain, best_left_subtree_idx, best_right_subtree_idx

    def get_mean_splitval(self, feature_vals):
        mean_splitval = []
        feature_vals_size = len(feature_vals)
        for val in range(1, feature_vals_size):
            first_val = feature_vals[val-1]
            second_val = feature_vals[val]
            mean_splitval.append((first_val + second_val)/2)
        return mean_splitval

    def entropy(self, train_y):
        p = np.unique(train_y, return_counts = True)[1] # return a list of counts for each unique val in y
        # print(f"number of unique val : {p}")
        p = p / np.sum(p) # give us the probability of each unique val in y
        # print(f"probability of each unique val : {p}")
        entropy = np.sum([-(prob * np.log2(prob)) for prob in p])
        return entropy


    def remainder(self, train_y, left_subtree_idx, right_subtree_idx):
        num_samples_at_R = len(left_subtree_idx) + len(right_subtree_idx)
        # print(f"total_number_of_samples_at_R : {num_samples_at_R}")
        prob_of_each_subtrees = [len(left_subtree_idx)/num_samples_at_R, len(right_subtree_idx)/num_samples_at_R]
        # print(f"probability_of_left_subtree : {prob_of_each_subtrees[0]}, probability_of_the_right_subtree : {prob_of_each_subtrees[1]}")
        entropy_at_each_subtrees = [self.entropy(train_y[left_subtree_idx]), self.entropy(train_y[right_subtree_idx])]
        # print(f"entropy_of_the_left_subtree : {entropy_at_each_subtrees[0]}, entropy_of_the_right_subtree : {entropy_at_each_subtrees[1]}")
        remainder_at_each_subtrees = zip(prob_of_each_subtrees, entropy_at_each_subtrees)
        sum_remainder = np.sum([s_p*s_e for s_p, s_e in remainder_at_each_subtrees])
        return sum_remainder


    def information_gain(self, train_y, left_subtree_idx, right_subtree_idx):
        # Make sure when the y training dataset is indexed from 1 not from 0 as the 0 is the feature's name
        parent_entropy = self.entropy(train_y)
        # print(f"parent_entropy : {parent_entropy}")
        remainder = self.remainder(train_y, left_subtree_idx, right_subtree_idx)
        # print(f"remainder : {remainder}")c
        info_gain = parent_entropy - remainder
        return info_gain

    def prediction_accuracy(self, test_dataset_result, test_predicted_result):
        count = 0
        l = []
        # test_predicted_result = [int(item) for item in test_predicted_result]
        print(f"length of the test-dataset-result : {len(test_dataset_result)}, length of the predicted-test-result : {len(test_predicted_result)}")
        print(f"test-dataset-result : {test_dataset_result}")
        print(f"test-dataset-result (dtype) : {test_dataset_result.dtype.name}")
        print(f"predicted-test-result : {test_predicted_result}")
        print(f"predicted-test-result (dtype) : {isinstance(test_predicted_result[0], int)}")
        if len(test_dataset_result) == len(test_predicted_result):
            for i in range(len(test_dataset_result)):
                if int(test_dataset_result[i]) == test_predicted_result[i]:
                    count += 1
                    l.append("True")
                else:
                    l.append("False")
        else:
            print("Error: test_dataset_result are not the same length as test_predicted_result !!")
        
        accuracy = count / len(test_dataset_result)
        print(l)
        return accuracy

    def execute_print(self):
        self.print_tree(self.root)

    def print_tree(self, tree_node):
        print(f"depth = {tree_node.depth_level}")

        if tree_node.bool_left and tree_node.bool_right == False:
            print("Left_subtree :")
        elif tree_node.bool_left == False and tree_node.bool_right:
            print("Right_subtree :")

        print(f"objective_feature_idx : {tree_node.obj_feature_idx}, split_val : {tree_node.split_val}")
        if tree_node.label != None:
            return tree_node.label
        self.print_tree(tree_node.left_subtree)
        self.print_tree(tree_node.right_subtree)


    def test_data_predict_labels(self, test_dataset_X):
        test_dataset_X = test_dataset_X[1:,:].astype('float')
        test_data_predicted_labels = []
        tree_node = None
        for row in test_dataset_X:
            tree_node = self.root
            while tree_node.label == None:
                objective_feature_idx = tree_node.obj_feature_idx
                split_val = tree_node.split_val
                if row[objective_feature_idx] <= split_val:
                    tree_node = tree_node.left_subtree
                elif row[objective_feature_idx] > split_val:
                    tree_node = tree_node.right_subtree
            test_data_predicted_labels.append(tree_node.label)
        return test_data_predicted_labels

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

def write_to_file(predicted_labels):
    predicted_labels = [str(item) for item in predicted_labels]
    with open("./sample_data/predicted_labels.txt", 'w') as f:
        for line in predicted_labels:
            f.write(line)
            f.write("\n")

def compare_2_files():
    f1 = open("./sample_data/test-sample-2-result", "r")  
    f2 = open("./sample_data/predicted_labels.txt", "r") 
    i = 0
    for line1 in f1:
        i+=1
        for line2 in f2:
            if line1 == line2:
                print(f"Line {i} : Same")
            else:
                print(f"Line {i} : ")
                print("\tFile 1 :", line1, end='')
                print("\tFile 2 :", line2, end='')
            break
    f1.close()
    f2.close()

path_to_training_dataset, path_to_testing_dataset, minleaf, path_to_testing_dataset_result = None, None, None, None
if len(sys.argv) >= 1:
    path_to_training_dataset = sys.argv[1]
    path_to_testing_dataset = sys.argv[2]
    minleaf = sys.argv[3]
    path_to_testing_dataset_result = sys.argv[4]

training_dataset = parse_dataset(path_to_training_dataset)
testing_dataset = parse_dataset(path_to_testing_dataset)
testing_dataset_result = parse_dataset(path_to_testing_dataset_result).flatten()
print(testing_dataset_result)

# print(testing_dataset)
number_samples = training_dataset.shape[0]-1
number_features = training_dataset.shape[1]-1
training_dataset_X = training_dataset[1:,:number_features]
training_dataset_Y = training_dataset[1:,number_features]
# print(training_dataset_Y)

# Return the total number of samples for each Quality rating (Q1 = 5, Q2 = 6, Q3 = 7)
unique_quality_val, num_samples_for_quality = np.unique(training_dataset_Y[1:], return_counts = True)

# print(f'Quality 5 samples: {num_samples_for_quality[0]}, Quality 6 samples: {num_samples_for_quality[1]}, Quality 7 samples: {num_samples_for_quality[2]}')

DCL = DecisionTreeLearning(min_sample_split=int(minleaf))
DCL.model_fitting(0,training_dataset)
predicted_labels = DCL.test_data_predict_labels(test_dataset_X=testing_dataset)
write_to_file(predicted_labels)
accuracy = DCL.prediction_accuracy(test_dataset_result=testing_dataset_result ,test_predicted_result=predicted_labels)
print("Accuracy : "+str(accuracy))
compare_2_files()
DCL.execute_print()
    
