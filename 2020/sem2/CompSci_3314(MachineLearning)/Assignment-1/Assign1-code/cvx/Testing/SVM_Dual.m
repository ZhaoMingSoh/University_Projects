[row,col] = size(X_training);

C_dual = 0.01;
P = (y_training'*y_training).*(X_training*X_training');

cvx_begin
    cvx_precision low
    variables al(row)
    maximize(sum(al) - (al'*P*al)/2)
    subject to
        y_training*al == 0;
        al >= 0; 
        al <= C_dual/row;
cvx_end