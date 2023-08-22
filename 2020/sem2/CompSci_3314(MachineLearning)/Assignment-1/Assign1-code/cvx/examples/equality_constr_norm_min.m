% Equality constrained norm minimization.
%
% This script constructs a random equality-constrained norm minimization
% problem and solves it using CVX. You can also change p to +2 or +Inf
% to produce different results. Alternatively, you an replace
%     norm( A * x - b, p )
% with
%     norm_largest( A * x - b, 'largest', p )
% for 1 <= p <= 2 * n.

% Generate data
p = 1;
n = 10; m = 2*n; q=0.5*n;
A = randn(m,n);
b = randn(m,1);
C = randn(q,n);
d = randn(q,1);

% Create and solve problem
cvx_begin
   variable x(n)
   dual variable y
   minimize( norm( A * x - b, p ) )
   subject to
        y : C * x == d;
cvx_end


