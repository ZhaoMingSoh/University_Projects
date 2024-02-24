from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import pandas as pd
import sys

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

path_to_training_dataset = None

if len(sys.argv) >= 1:
    path_to_training_dataset = sys.argv[1]

training_dataset = parse_dataset_csv(path_to_training_dataset)
X, y = training_dataset[:,:-2], training_dataset[:,-2]
train_X, test_X, train_Y, test_Y = train_test_split(X, y, test_size=0.2, random_state=42)

# Create Decision Tree Classifier object
dtl = DecisionTreeClassifier(criterion="entropy", splitter="random", max_depth=100, min_samples_split=2, random_state=0)

# Train Decision Tree Classifer
dtl = dtl.fit(train_X,train_Y)

#Predict the response for test dataset
y_pred = dtl.predict(test_X)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(test_Y, y_pred))
