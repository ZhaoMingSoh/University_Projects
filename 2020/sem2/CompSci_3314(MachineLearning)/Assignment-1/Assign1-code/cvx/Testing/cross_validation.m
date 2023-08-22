Num_Fold = 5;
cvIndices = crossvalind('Kfold',y_training,Num_Fold);
[row,col] = size(X_training);

increment_i = 0;
C_Fold = 1:1:1;

for k=1:length(C_Fold)
    for i=1:Num_Fold
        % Selecting a validation set from each Fold
        Validation_sample=X_training(cvIndices==i,:);
        % Set the remaining fold as the training sample
        TrainingFold_sample=X_training(cvIndices~=i,:);
        % Selecting the traning label not equal to the current Fold
        TrainingFold_label=y_training(cvIndices~=i);
        
        [r_sam,c_sam] = size(TrainingFold_sample);
        [r_val,c_val] = size(Validation_sample);
        
        cvx_begin
        cvx_precision low
        variables slack(r_sam) w(c_sam) b
        minimize((w'*w)/2+(C_Fold(k)/r_sam)*sum(slack))
        subject to
        TrainingFold_label'.*(TrainingFold_sample*w+b) >= 1-slack;
        slack >= 0;
        cvx_end
        
        
        Predicted_Labels = zeros(1,r_val);
        increment_i = increment_i + i;
        Temp_b_fold(i) = b;
        
        %% Classifying the test dataset using the generated training model variables
        for o=1:r_val
            if (Validation_sample(o,:)*w+b) > 0
                Predicted_Labels(o) = 1;
            else
                Predicted_Labels(o) = -1;
            end
        end
        
        OutLabel(cvIndices==i,1) = Predicted_Labels;
        
        
    end
    
    Sum_Fold = 0;
    
    for i=1:row
        if OutLabel(i,1) == y_training(i)
            Sum_Fold = Sum_Fold + 1;
        end
    end
    
    %% Checking for Correctness
    test_accuracy_Fold(k) = Sum_Fold/row;
    
  
   
    
    
end

[C,I] = max(test_accuracy_Fold); 
Best_Accuracy = C;
Best_Hyperparameter = C_Fold(I);


 