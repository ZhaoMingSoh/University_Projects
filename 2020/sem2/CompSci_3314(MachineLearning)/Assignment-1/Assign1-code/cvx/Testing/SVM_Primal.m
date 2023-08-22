[row,col] = size(X_training);

C = 0.00001;

cvx_begin
    cvx_precision low
    variables slack(row) w(col) b
    minimize((w'*w)/2+(C/row)*sum(slack))
    subject to
        y_training'.*(X_training*w+b) >= 1-slack;
        slack >= 0;
cvx_end 