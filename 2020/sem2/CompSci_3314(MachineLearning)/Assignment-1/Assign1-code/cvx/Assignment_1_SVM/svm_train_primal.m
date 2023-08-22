function svm_model = svm_train_primal (data_train , label_train , regularisation_para_C)
% This function uses the cvx soft-margin primal model to train on the given
% training datasets(X_training) and labels(y_training) in order to produce the slack, primal_w and
% primal_b variables 

% Extract the dimensions of the training datasets 
[row,col] = size(data_train);

cvx_begin
    cvx_precision low
    variables slack(row) w(col) b
    minimize((w'*w)/2+((regularisation_para_C/row)*sum(slack)))
    subject to
        label_train'.*(data_train*w+b) >= 1-slack;
        slack >= 0;
cvx_end 

%% Storing each of the variables into a svm_model structure
field1 = 'w';
value1 = w;

field2 = 'b';
value2 = b;

svm_model = struct(field1,value1,field2,value2);

end


