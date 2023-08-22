function svm_model_d = svm_train_dual (data_train , label_train , regularisation_para_C)
% This function uses the cvx soft-margin dual model to train on the given
% training datasets(X_training) and labels(y_training) in order to produce
% the al, w_dual and and b_dual

% Extract the dimensions of the traning data 
[row,col] = size(data_train);

%% Dual Model
P = (label_train'*label_train).*(data_train*data_train');

cvx_begin
    cvx_precision low
    variables al(row)
    maximize(sum(al) - (al'*P*al)/2)
    subject to
        label_train*al == 0;
        al >= 0;
        al <= regularisation_para_C/row;
cvx_end

%% Calculate the w_dual and b_dual variables using the generated alpha
w_dual = zeros(col,1);
b_dual = 0;

for o=1:row
    if ((al(o,1) < (regularisation_para_C/row -1*power(10,-7))) && (al(o,1) > 1*power(10,-7))) 
        w_dual = w_dual + al(o,1)*label_train(o)*data_train(o,:)';
    end
end
for o=1:row
    b_dual = b_dual + (1/row)*(label_train(o)-w_dual'*data_train(o,:)');
end

%% Storing the variables into a svm_model_d structure
f1 = 'w_dual';
val1 = w_dual;

f2 = 'b_dual';
val2 = b_dual;

svm_model_d = struct(f1,val1,f2,val2);

end



    
