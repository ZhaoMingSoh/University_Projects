import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class Adaboost:

    # Adaboost Class Constructor 
    def __init__(self,Train_X,Train_Y,Test_X,Test_Y,KFold_Train_X,KFold_Test_X,KFold_Train_Y,KFold_Test_Y,Num_Of_Classifier):
        self.Train_X = Train_X
        self.Train_Y = Train_Y
        self.Test_X = Test_X
        self.Test_Y = Test_Y
        self.KFold_Train_X = KFold_Train_X
        self.KFold_Test_X = KFold_Test_X
        self.KFold_Train_Y = KFold_Train_Y
        self.KFold_Test_Y = KFold_Test_Y
        self.Num_Of_Classifier = Num_Of_Classifier # The Number base estimator (Decision Stump)
        self.alpha = [] # Stores the alpha value for each Decision Stump in each interation (Example: i=10, store alpha for decision stump number 10)
        self.Weak_Classifier = [] # Stores the number of base estimator (Decision Stump)
        self.feature_T = []
        self.accuracy = [] # Stores the accuracy for each Decision Stump 
        self.training_error = [] # Stores the traning data predictions 
        self.testing_error = [] # Stores the testing data predictions 
    
    
    # Fitting the Decision Stump based on the Training Dataset Given
    def Build_Model(self):

        # Extract The Dimension of Train_X data
        num_X, num_Y = np.shape(self.Train_X)

        # Converts self.Test_Y and self.Train_Y from matrix into array format --> (300,1) to (300) and (268,1) to (268)
        train_squeeze_Y = np.squeeze(np.asarray(self.Train_Y))
        
        # Set the initial Weight for each of the Train_X data
        weight = np.full(num_X, (1 / num_X))
    
        #Transpose_Train_Y = self.Train_Y.T
        train_pred = np.zeros(len(self.Train_X))
        test_pred = np.zeros(len(self.Train_Y))
        
        # This is where we construct/train the Decision Stump Model
        for index in range(self.Num_Of_Classifier):
            err_Tru = 1
            prediction_T = None
            model_T = None
            temp_misclassification = []
            feature_i = ''

            i = 0

            while i < num_Y:
                temp_sum = np.full(num_X, 0)
                # Build the Generic Decision Stump
                # Entropy is used here to select the best performing Decision tree in each iteration based on how good a feature can split the Train_X data into 
                clf = DecisionTreeClassifier(criterion='entropy', max_depth=1)

                # Fit the Decision Stump with the corresponding Train_X data and Train_Y label and the data weights 
                Model = clf.fit(np.float32(self.Train_X.iloc[:,[i]]),np.float32(self.Train_Y), sample_weight=np.array(weight))
                short_prediction = clf.predict(self.Train_X.iloc[:,[i]])
                
                for iterator in range(len(short_prediction)):
                    if short_prediction[iterator] != train_squeeze_Y[iterator]:
                        temp_sum[iterator] = 1 

                #misclassification_Array = np.where(short_prediction != self.Train_Y['M'],1,0)
                
                short_err = np.sum(temp_sum*weight)

                if short_err <= err_Tru:
                    err_Tru = short_err
                    prediction_T = short_prediction
                    model_T = Model
                    feature_i = i
                
                i = i + 1

            # Store the Fitted Decision Stump intp the models array
            self.Weak_Classifier.append(model_T)
            self.feature_T.append(feature_i)
            
            # Calculate the alpha values
            al = 1/2 * np.log((1-err_Tru)/err_Tru)
            self.alpha.append(al)
            # Calculate the new weight for each of the data in Train_X
            weight *= np.exp(-al*self.Train_Y['M'].astype(int) * prediction_T.astype(int))
            weight /= np.sum(weight) # Normalise the weight of each data 
            
            self.predict()
            self.test_train_error()
    
    def predict(self):
        predictions = []
        
        temp_arr_1 = []
        temp_arr_2 = []
        temp_accuracy = 0
        
        count = 0
        # Calculate the accuracy of each Decision Stump on the Testing dataset 
        for al, clf in zip(self.alpha, self.Weak_Classifier):
            prediction = al*clf.predict(self.Test_X.iloc[:,[self.feature_T[count]]])
            predictions.append(prediction)
            count = count + 1 

        temp_arr_1 = np.sign(np.sum(predictions, axis=0))
        temp_arr_2 = np.where(temp_arr_1 == self.Test_Y['M'],1,0)
        temp_accuracy = np.sum(temp_arr_2)/len(predictions[0])
        self.accuracy.append(temp_accuracy)
    
    def test_train_error(self):
        # Training variables
        pred_Train = []
        Temp_Train = []
        Temp_Train_Total = []

        # Testing variables
        pred_Test = []
        Temp_Test = []
        Temp_Test_Total = []

        count = 0

        for al, clf in zip(self.alpha, self.Weak_Classifier):
            predictions_train_err = al*clf.predict(self.KFold_Train_X.iloc[:,[self.feature_T[count]]])
            predictions_test_err = al*clf.predict(self.KFold_Test_X.iloc[:,[self.feature_T[count]]])
            pred_Train.append(predictions_train_err)
            pred_Test.append(predictions_test_err)
            count =  count + 1

        # Calculate Training Error 
        Temp_Train = np.sign(np.sum(pred_Train, axis=0))
        Temp_Train_Total = np.where(Temp_Train == self.KFold_Train_Y['M'],1,0)
        self.training_error.append(1-(np.sum(Temp_Train_Total)/len(pred_Train[0])))

        # Calculate Testing Error
        Temp_Test = np.sign(np.sum(pred_Test, axis=0))
        Temp_Test_Total = np.where(Temp_Test == self.KFold_Test_Y['M'],1,0)
        self.testing_error.append(1-(np.sum(Temp_Test_Total)/len(pred_Test[0])))

#Import the Dataset
dataset = pd.read_csv("wdbc_data.csv")

training_Y = dataset.iloc[0:300,[1]]
training_X = dataset.iloc[0:300,2:]

testing_Y = dataset.iloc[300:,[1]]
testing_X = dataset.iloc[300:,2:]

training_Y[training_Y=='M']=1
training_Y[training_Y=='B']=-1

testing_Y[testing_Y=='M']=1
testing_Y[testing_Y=='B']=-1

KF_X_train, KF_X_test, KF_Y_train, KF_Y_test = train_test_split(training_X, training_Y, test_size = 0.3)

number_of_base_learners = 200

Temp_accuracy = []

figure = plt.figure(figsize=(10,10))
figure2 = plt.figure(figsize=(10,10))
figure3 = plt.figure(figsize=(10,10))
acc0 = figure.add_subplot(111)
err0 = figure2.add_subplot(111)
err1 = figure3.add_subplot(111)

m = Adaboost(training_X, training_Y, testing_X, testing_Y, KF_X_train, KF_X_test, KF_Y_train, KF_Y_test, number_of_base_learners)
m.Build_Model()

train_Y = np.squeeze(np.asarray(training_Y))
test_Y = np.squeeze(np.asarray(testing_Y))

sklearn_test_Err = []
sklearn_train_Err = []

# Sklearn AdaboostClassifier Implementation 
for i in range(1, number_of_base_learners+1):
    AdaBoost = AdaBoostClassifier(n_estimators=i,algorithm='SAMME')
    AdaBoost.fit(np.float32(training_X), np.float32(train_Y)) 
    prediction = AdaBoost.score(np.float32(testing_X), np.float32(test_Y)) # Calculate the score for the Testing Data
    prediction_Train = AdaBoost.score(np.float32(KF_X_train), np.float32(KF_Y_train)) # Calculate the score for Traning Data obtained from Validation set
    prediction_Test = AdaBoost.score(np.float32(KF_X_test), np.float32(KF_Y_test)) # Calculate the score for Testing Data obtained from Validation set
    Temp_accuracy.append(prediction)
    sklearn_train_Err.append(1-prediction_Train) # Calculate the Training error from the Training Data obtained from Validation Set
    sklearn_test_Err.append(1-prediction_Test)  # Calculate the Testing error from the Testing Data obtained from Validation Set
    
# My Adaboost accuracy vs Sklearn Adaboost accuracy
acc0.plot(range(len(m.accuracy)),m.accuracy,'-b')
acc0.plot(range(len(Temp_accuracy)), Temp_accuracy, 'r--')
acc0.set_xlabel('Number of base Model used for boosting')
acc0.set_ylabel('Accuracy')

# My Adaboost training error vs Sklearn Adaboost training error
err0.plot(range(len(m.training_error)),m.training_error,'-b')
err0.plot(range(len(sklearn_train_Err)), sklearn_train_Err, 'r--')
err0.set_xlabel('Number of iterations')
err0.set_ylabel('Training Error Rate')

# My Adaboost testing error vs Sklearn Adaboost testing error
err1.plot(range(len(m.testing_error)),m.testing_error,'-b')
err1.plot(range(len(sklearn_test_Err)), sklearn_test_Err, 'r--')
err1.set_xlabel('Number of iterations')
err1.set_ylabel('Testing Error Rate') 
                 
plt.show()        

