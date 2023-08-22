

%% Check the accuracy of the model on the test data by comparing the predicted_testlabel with the y_test labels
Correct_instance = 0;

for index=1:1500
    if predicted_testlabel(index,:) == y_test(index,:)
        Correct_instance = Correct_instance + 1;
    end
end

Accuracy_test = Correct_instance/1500;

%% Check the accuract of the model on the training data by comparing the predicted_trainlabel with y_train labels

Correct_instance_train = 0;

for index=1:8500
    if predicted_trainlabel(index,:) == y_train(index,:)
        Correct_instance_train = Correct_instance_train + 1;
    end
end

Accuracy_train = Correct_instance_train/8500;

