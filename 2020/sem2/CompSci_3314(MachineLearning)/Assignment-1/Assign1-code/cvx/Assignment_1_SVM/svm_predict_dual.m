function test_accuracy_d = svm_predict_dual (data_test , label_test , svm_model_d)
% This function uses the variables generated from the svm_train_dual model to predict the classification on the X_test data

%% Variables declaration
% An array with 1500 elements initialised as zero
Predicted_dual_labels = zeros(1500,1);

Total_Predicted_dual_Labels = zeros(1500,11);

dual_Sum = 0;

% the w_dual and b_dual from svm_model
w_dual = svm_model_d.w_dual;
b_dual = svm_model_d.b_dual;

%% Classifying the test dataset using the training model variables 
for num_D=1:11
    for x=1:1500
        if (data_test(x,:)*w_dual(:,num_D)+b_dual(num_D)) > 0
            Predicted_dual_labels(x,1) = 1;
        else
            Predicted_dual_labels(x,1) = -1;
        end
    end
    Total_Predicted_dual_Labels(:,num_D) = Predicted_dual_labels;
end

%% Comparing the y labels generated by my model to the predefined y labels in y_test table
for num_D=1:11
    for x=1:1500
        if Total_Predicted_dual_Labels(x,num_D) == label_test(x)
            dual_Sum = dual_Sum + 1;
        end
    end
    test_accuracy_d(num_D) = dual_Sum/1500*100; % Checking for Correctness 

    dual_Sum = 0;
end
[B_D,Pos_D] = max(test_accuracy_d); 
Best_Test_Accuracy_Dual = B_D;

test_accuracy_d = struct('All_C_accuracy_D', test_accuracy_d, 'Best_Accuracy_D', Best_Test_Accuracy_Dual);

end


