# Decision Tree Classifier or Learning

# Steps in the algorithm :

substantiating data :

- objective feature : a specific characteristic representing an entire column
- treshold : the value of the data point under a specific column

1. starts from the root, select the best objective feature & the best treshold for a node by calculating and comparing every single data points' information gain on either an objective feature from a subset of objectives features or a random selected one.
2. there are 2 nuances in calculating the information gain for the data points,
   - each numeric data points need to be converted into an average of 2 data points
   - binary or boolean data points that signify yes/no can proceed as normal
3. Information gain procedure :
   - calculate the entropy(parent)
   - split the data points into 2 halves based on the selected treshold for comparison
   - calculate the weight of each halves and then calculate the entropy of each halves, sum of the product of the weight & entropy of each halves
   - entropy(parent) - entropy(children)
4. when the best objective feature and treshold is obtained, use it to split the data points into a left and right child.
5. repeat steps (1 to 4) until a leaf node is obtained.
   - when the left and right child are leaf nodes, a decision tree node is then formed.

These steps outline the comprehensive procedure for constructing a decision tree by iteratively evaluating and splitting the data points based on the selected features and thresholds until a well-defined decision tree structure is achieved.

# Random Forest

because of the way best_tresh is initialised as a None in the decision tree algo in winequality_DTL_1.py, the random forest algo in winequality_RFL_1.py will sometimes run into an error : **TypeError: '<=' not supported between instances of 'float' and 'NoneType'**

```python
   if(x[node.obj_feature_idx] <= node.split_val): # some of the nodes will have None as the splitVal
```

the node splitVal shouldn't even be None in the first place, that means something is wrong with the algo, but I'm not sure where ......

# Venv for Python

'''bash
$ python3 -m venv new-venv
$ source new-venv/bin/activate
(new-venv) $ python -m pip install -r requirements.txt
'''
The requirements.txt contains all the dependencies and libaries required for the python projects in this folder to run.
