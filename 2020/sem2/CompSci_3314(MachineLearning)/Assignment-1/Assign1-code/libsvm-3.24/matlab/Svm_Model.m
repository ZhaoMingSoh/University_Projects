%% Extract the label y and the features x from the given training and testing document
[y_train, x_train] = libsvmread('train.libsvm');
[y_test, x_test] = libsvmread('test.libsvm');

for index=1:8500
    if y_train(index,:) == 0
        y_train(index,:) = -1;
    end
end

for in=1:1500
    if y_test(in,:) == 0
        y_test(in,:) = -1;
    end
end


%% Run the svmtrain 
model = svmtrain(y_train, x_train, '-s -t -c 50');

%% Run the svmpredict using the generated model on y_test and x_test
[predicted_testlabel] = svmpredict(y_test, x_test, model, '-q');

%% Check the accuracy of the model on the test data by comparing the predicted_testlabel with the y_test labels
Correct_instance = 0;

for index=1:1500
    if predicted_testlabel(index,:) == y_test(index,:)
        Correct_instance = Correct_instance + 1;
    end
end

Accuracy_test = Correct_instance/1500;