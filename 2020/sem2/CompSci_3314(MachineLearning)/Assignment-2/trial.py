import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import genfromtxt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


input_data = genfromtxt('dataset.csv', delimiter=',')
input_data = pd.DataFrame(input_data, columns=['ID', 'Target', 'Feature1',
'Feature2','Feature3','Feature4','Feature5','Feature6','Feature7','Feature8','Feature9',
'Feature10','Feature11','Feature12','Feature13','Feature14','Feature15','Feature16','Feature17',
'Feature18','Feature19','Feature20','Feature21','Feature22','Feature23','Feature24','Feature25',
'Feature26','Feature27','Feature28','Feature29','Feature30'])
data_without_id_target = input_data[['Feature1',
'Feature2','Feature3','Feature4','Feature5','Feature6','Feature7','Feature8','Feature9',
'Feature10','Feature11','Feature12','Feature13','Feature14','Feature15','Feature16','Feature17',
'Feature18','Feature19','Feature20','Feature21','Feature22','Feature23','Feature24','Feature25',
'Feature26','Feature27','Feature28','Feature29','Feature30']]
x_train = data_without_id_target.loc[0:299]
y_train = input_data['Target'].loc[0:299]
x_test_train = data_without_id_target.loc[300:568]
y_test = input_data['Target'].loc[300:568]

myPrediction = None
myPredictionAccuracy = None
myPredictionList = []


class Adaboost:
    def __init__(self, iteration_num):
        self.iteration_num = iteration_num
        self.weight = []
        self.best_classifiers = []
        self.alpha = []
        self.feature_id =[]
    def fit(self, X, y):
        # # print('hello')
        self.weight = np.full(X.shape[0], 1/X.shape[0])
        for k in range(self.iteration_num):
            print('k is ', k)
            # reset error and bestprediction
            error = 1
            best_prediction = None
            best_stump = None
            id = ''
            for m in range(1,X.shape[1]+1): # find the best classifier from 'Feature1' to 'Feature30'
                # aStump = DecisionStump()
                aStump = DecisionTreeClassifier(max_depth=1)
                # # print('m:', m)
                # aStump.predict(X, y, 'Feature'+str(m), self.weight)
                aStump.fit(X[['Feature'+str(m)]], y, self.weight)
                temp_predict = aStump.predict(X[['Feature'+str(m)]])
                # print (m)
                # print(self.weight)
                diff_array = np.full(self.weight.shape[0], 0)
                diff_array[temp_predict.astype(int) != np.array(y).astype(int)] = 1
                temp_error = np.sum(diff_array * self.weight)
                # # print('in round ',k, 'Feature'+str(m), ' aStump error is ', aStump.error, ' error is ', error)
                # # print('---end---')
                if(temp_error <= error):
                    error = temp_error
                    # best_prediction = aStump.predict(X, y, 'Feature'+str(m), self.weight)
                    best_prediction = temp_predict
                    best_stump = aStump
                    id = 'Feature'+str(m)
            # # print('best stump is ', best_stump.feature_id)
            #print(error)
            # print('best stump is ', id)
            self.best_classifiers.append(best_stump)
            self.feature_id.append(id)
            # pay more attention to the incorrectly classified, update weight
            # # print("correctly labeled weight: ", np.sum(self.weight[best_prediction == np.array(y)]))
            # # print("incorrectly labeled weight: ", np.sum(self.weight[best_prediction != np.array(y)]))
            # # print("error: ", aStump.error)
            # for e in range(y.shape[0]):
            #     if int(best_prediction[e]) != int(np.array(y)[e]):
            #         self.weight[e] = self.weight[e] * np.exp(aStump.alpha)
            #     else:
            #         self.weight[e] = self.weight[e] * np.exp( (-1) * aStump.alpha)
            alpha = 0.5 * np.log((1.0 - error) / (error))
            self.alpha.append(alpha)
            #print('alpha is ',alpha)
            self.weight *= np.exp((-1) * alpha * best_prediction * y)
            # # print('self.weight is changed to ', self.weight)
            # then divide the normaliser z
            z = np.sum(self.weight)
            # # print('z is ',z)
            
            self.weight = self.weight/z
            print(self.alpha)
            myPrediction = self.predict(x_test_train)
            myPredictionAccuracy = np.sum(myPrediction.astype(int) == np.array(y_test).astype(int)) / y_test.shape[0]
            myPredictionList.append(myPredictionAccuracy)

    def predict(self, X):
        final_prediction = np.full(X.shape[0], 0.0)
        sample_num = X.shape[0]
        count = 0
        for e in self.best_classifiers:
            # # print('The best classifier is ', e.feature_id, ', with alpha ', e.alpha)
            # temp_predict = np.ones(sample_num)
            # if e.flip == 1:
            #     temp_predict[np.array(X[e.feature_id]) <= e.threshold] = -1
            # else:
            #     temp_predict[np.array(X[e.feature_id]) > e.threshold] = -1
            final_prediction += self.alpha[count]*e.predict(X[[self.feature_id[count]]])
            count += 1
            # # print('final prediction is ', final_prediction)
        final_prediction = np.sign(final_prediction)
        #print(final_prediction)
        return final_prediction

# myPrediction = clf.predict(x_test_train)
# myPredictionList = []
sklearnPredictionList = []
x_label = []
n_estimators = 10
clf = Adaboost(n_estimators)
clf.fit(x_train, y_train)
# myPrediction = clf.predict(x_train)
# myPredictionAccuracy = np.sum(myPrediction.astype(int) == np.array(y_train).astype(int)) / y_train.shape[0]
# myPredictionList.append(myPredictionAccuracy)

for i in range(1, n_estimators+1):
    x_label.append(i)
    sklearn_clf = AdaBoostClassifier(n_estimators=i, algorithm='SAMME')
    sklearn_clf.fit(x_train, y_train)
    sklearn_clf.predict(x_test_train)
    sklearnPredictionList.append(sklearn_clf.score(x_test_train, y_test))

plt.plot(x_label, myPredictionList, label="My Prediction")

# plotting the line 2 points
plt.plot(x_label, sklearnPredictionList, label="SKLearn Prediction")
plt.xlabel('Number of Estimators')
plt.ylabel('Accuracy')
# show a legend on the plot
plt.legend()
plt.show()
# # print('Accuracy is ', np.sum(myPrediction.astype(int) == np.array(y_test).astype(int))/y_test.shape[0])