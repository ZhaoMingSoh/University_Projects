%% Loading train.mat and test.mat datasets 
load('test.mat');
X_test_data = X;
y_test_labels = y;
clear X;
clear y;

load('train.mat');
X_training_data = X;
y_training_labels = y;
clear X;
clear y;

%% Converting all 0 labels in y_training_labels and y_test_labels to -1 
for i=1:8500
    if y_training_labels(1,i) == 0
        y_training_labels(1,i) = -1;
    end
end

for i=1:1500
    if y_test_labels(1,i) == 0
        y_test_labels(1,i) = -1;
    end
end

%%  5 Fold Cross Validation for both Primal and Dual To find the best performing Hyperparameter C
% Note : 
Num_Fold = 5;

% Separate the training labels into 5 randomly generated subsets, each
% cvindice refers to the subset that each corresponding training label is placed
% into.
cvIndices = crossvalind('Kfold',y_training_labels,Num_Fold);

% Hyperparameter ranges from 0.01 to 80 by an increment of 10
C_Fold = [0.01 0.1 1 10 20 30 40 50 60 70 80];

%% Primal 
Temp_w_arr_Primal = zeros(200,Num_Fold);
w_fold_primal = zeros(200,length(C_Fold));

%% Dual
Temp_w_arr_Dual = zeros(200,Num_Fold);
w_fold_Dual = zeros(200,length(C_Fold));

% Run the Cross Validation for each different C_Fold
for k=1:length(C_Fold)
    %Run the Cross Validation for each Fold
    for i_p=1:Num_Fold
        % Selecting a validation set from each Fold
        Validation_sample=X_training_data(cvIndices==i_p,:);
        % Set the remaining fold as the training sample
        TrainingFold_sample=X_training_data(cvIndices~=i_p,:);
        % Selecting the traning label not equal to the current Fold
        TrainingFold_label=y_training_labels(cvIndices~=i_p);
        
        [r_val,c_val] = size(Validation_sample);
        
        %% Train the primal model with the TrainingFold_sample and
        % TrainingFold_label
        svm_model = svm_train_primal(TrainingFold_sample, TrainingFold_label, C_Fold(k));
        
        %% Train the Dual model with the TrainingFold_sample and
        % TrainingFold_label
        svm_model_d = svm_train_dual (TrainingFold_sample ,TrainingFold_label, C_Fold(k));
        
        Fold_Predicted_Labels_Primal = zeros(1,r_val);
        Fold_Predicted_Labels_Dual = zeros(1,r_val);
        
        w_fold_p=svm_model.w;
        b_fold_p=svm_model.b;
        
        w_fold_D=svm_model_d.w_dual;
        b_fold_D=svm_model_d.b_dual;
        
        %% Store each w generated from each Num_Fold to an Array (Primal)
        for oo=1:200
            Temp_w_arr_Primal(oo,i_p) = w_fold_p(oo,1);
        end
        
        % Store each b generated from each Num_Fold to an Array
        Temp_b_arr_Primal(i_p) = b_fold_p;
        
        %% Store each w generated from each Num_Fold to an Array (Dual)
        for oo_D=1:200
            Temp_w_arr_Dual(oo_D,i_p) = w_fold_D(oo_D,1);
        end
        
         % Store each b generated from each Num_Fold to an Array
        Temp_b_arr_Dual(i_p) = b_fold_D;
        
        
        %% Classifying the test dataset using the generated training model variables (Primal)
        for f=1:r_val
            if (Validation_sample(f,:)*w_fold_p+b_fold_p) > 0
                Fold_Predicted_Labels_Primal(f) = 1;
            else
                Fold_Predicted_Labels_Primal(f) = -1;
            end
        end
        
        % Concatenate each Fold_Predicted_labels for each cross Validation
        % into a single array
        OutLabel_Primal(cvIndices==i_p,1) = Fold_Predicted_Labels_Primal;
        
        
        %% Classifying the test dataset using the generated training model variables (Dual)
        for f=1:r_val
            if (Validation_sample(f,:)*w_fold_D+b_fold_D) > 0
                Fold_Predicted_Labels_Dual(f) = 1;
            else
                Fold_Predicted_Labels_Dual(f) = -1;
            end
        end
        
        % Concatenate each Fold_Predicted_labels for each cross Validation
        % into a single array
        OutLabel_Dual(cvIndices==i_p,1) = Fold_Predicted_Labels_Dual;
    end
    
    %% (Primal) 
    %Storing the average b value obtained from 5 folds for each Different C 
    b_fold_primal(k) = sum(Temp_b_arr_Primal)/Num_Fold;
    
    % Computing the average w value across the 5 folds for each row
    Sum_w_P = 0;
    for w_row_P=1:200
        for w_col_P=1:Num_Fold
            Sum_w_P = Sum_w_P + Temp_w_arr_Primal(w_row_P,w_col_P);
        end
        w_fold_primal(w_row_P,k) = Sum_w_P/Num_Fold;
        Sum_w_P = 0; % Resets the Sum_w
    end
    
    % Comparing the OutLabel with the training label
    Sum_Fold_P = 0;
    for i_Compare_P=1:8500
        if OutLabel_Primal(i_Compare_P,1) == y_training_labels(i_Compare_P)
            Sum_Fold_P = Sum_Fold_P + 1;
        end
    end
    
    % Checking for Accuracy of the OutLabel
    Validation_Accuracy_Fold_Primal(k) = Sum_Fold_P/8500;
    
    
    %% Dual 
    %Storing the average b value obtained from 5 folds for each Different C 
    b_fold_Dual(k) = sum(Temp_b_arr_Dual)/Num_Fold;
    
    % Computing the average w value across the 5 folds for each row
    Sum_w_D = 0;
    for w_row_D=1:200
        for w_col_D=1:Num_Fold
            Sum_w_D = Sum_w_D + Temp_w_arr_Dual(w_row_D,w_col_D);
        end
        w_fold_Dual(w_row_D,k) = Sum_w_D/Num_Fold;
        Sum_w_D = 0; % Resets the Sum_w
    end
    
    % Comparing the OutLabel with the training label
    Sum_Fold_D = 0;
    for i_Compare_D=1:8500
        if OutLabel_Dual(i_Compare_D,1) == y_training_labels(i_Compare_D)
            Sum_Fold_D = Sum_Fold_D + 1;
        end
    end
    
    % Checking for Accuracy of the OutLabel
    Validation_Accuracy_Fold_Dual(k) = Sum_Fold_D/8500;
end

%% Primal
% Find the Hyperparameter C that gives the highest Accuracy
[C_P,I_pos_P] = max(Validation_Accuracy_Fold_Primal); 
Best_Accuracy_Primal = C_P;
Best_Hyperparameter_Primal = C_Fold(I_pos_P);

% Replace the w vector and the value of b with the w vector and the value of b obtained from the optimal C
svm_model.w = w_fold_primal;
svm_model.b = b_fold_primal;

test_accuracy = svm_predict_primal (X_test_data, y_test_labels, svm_model);


%% Dual
% Find the Hyperparameter C that gives the highest Accuracy
[C_D,I_pos_D] = max(Validation_Accuracy_Fold_Dual); 
Best_Accuracy_Dual = C_D;
Best_Hyperparameter_Dual = C_Fold(I_pos_D);

% Replace the w vector and the value of b with the w vector and the value of b obtained from the optimal C
svm_model_d.w_dual = w_fold_Dual;
svm_model_d.b_dual = b_fold_Dual;

test_accuracy_d = svm_predict_dual (X_test_data, y_test_labels, svm_model_d);

%% Calculate the difference between Primal w,b and Dual w,b for each of the Hyperparameter C
Difference_temp_w = zeros(200,length(C_Fold));
for diff_col=1:length(C_Fold)
    for diff_row=1:200
        Difference_temp_w(diff_row,diff_col) = abs(w_fold_primal(diff_row,diff_col)) - abs(w_fold_Dual(diff_row,diff_col));
    end
end


for diff_each_w=1:length(C_Fold)
    Difference_w(diff_each_w) = abs(sum(Difference_temp_w(:,diff_each_w))/200);
end

for diff_each_b=1:length(C_Fold)
    Difference_b(diff_each_b) =  abs(b_fold_Dual(diff_each_b)) - abs(b_fold_primal(diff_each_b));
end

