
load('test.mat');
X_test = X;
y_test = y;
clear X;
clear y;

load('train.mat');
X_training = X;
y_training = y;
clear X;
clear y;

%% Converting all 0 labels in y_training_labels and y_test_labels to -1 
for i=1:8500
    if y_training(1,i) == 0
        y_training(1,i) = -1;
    end
end

for i=1:1500
    if y_test(1,i) == 0
        y_test(1,i) = -1;
    end
end


