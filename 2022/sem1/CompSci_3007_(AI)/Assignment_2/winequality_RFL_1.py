import numpy as np
import pandas as pd
from collections import Counter
from winequality_DTL_1 import DecisionTreeLearning

'''
    create a bootstrap dataset of the same size as the original training dataset.
'''
def bootstrap_dataset(train_X, train_Y):
    n_data = train_X.shape[0]
    bootstrap_idxs = np.random.choice(n_data, n_data, replace=True) # the same data can be picked more than once
    return train_X[bootstrap_idxs], train_Y[bootstrap_idxs]

def get_most_common_label(train_Y):
    counter = Counter(train_Y)
    print(counter)
    most_common_label = counter.most_common(1)[0][0]
    return most_common_label

class RandomForest:
    '''
        n_trees : number of decision trees
        n_feats : number of features to randomly choose from at each step
    '''
    def __init__(self, n_D_trees=10, min_samples_split=2, max_depth=100, n_feats=None):
        self.n_D_trees = n_D_trees
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_feats = n_feats
        self.D_trees = [] # store the all the decision trees

    def model_fitting(self, train_X, train_Y):
        self.D_trees = []
        for _ in range(self.n_D_trees):
            decision_tree = DecisionTreeLearning(self.min_samples_split, self.max_depth, self.n_feats, random_forest=True)
            bootstrap_X, bootstrap_Y = bootstrap_dataset(train_X, train_Y) # Step 1 : bootstrap the training dataset
            decision_tree.model_fitting(bootstrap_X, bootstrap_Y) # Step 2 : create decision tree from the bootstrapped training dataset
            self.D_trees.append(decision_tree) # store all of the decision trees

    def predict(self, test_X):
        D_trees_preds = np.array([decision_tree.test_data_predict_labels(test_X) for decision_tree in self.D_trees])
        # convert from the row of the 2d array to the column of the 2d array, R*C -> C*R
        D_trees_preds = np.swapaxes(D_trees_preds, 0, 1)
        pred_label = [get_most_common_label(D_tree_pred) for D_tree_pred in D_trees_preds]
        return np.array(pred_label)


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
    import sys
    from sklearn.model_selection import train_test_split

    path_to_training_dataset = None

    if len(sys.argv) >= 1:
        path_to_training_dataset = sys.argv[1]

    training_dataset = parse_dataset_csv(path_to_training_dataset)
    X, y = training_dataset[:,:-2], training_dataset[:,-2]
    train_X, test_X, train_Y, test_Y = train_test_split(X, y, test_size=0.2, random_state=42)

    rfl = RandomForest(n_D_trees=100,n_feats=2)
    rfl.model_fitting(train_X, train_Y)
    pred_Y = rfl.predict(test_X)
    acc = accuracy(pred_Y, test_Y)
    print("Accuracy : ", acc)