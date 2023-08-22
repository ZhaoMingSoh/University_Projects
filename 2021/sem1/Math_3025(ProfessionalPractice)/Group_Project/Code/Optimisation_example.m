%{

This script calls the function Optimisation to solve optimisation problems

(This particular example is from page 70 of the lecture notes on Maths IA
algebra that I used at Adelaide Uni.)

KB - May 2015

%}

%%% Constraints %%%

% Mx <= w

M = [1, 1, 1; -1, 0, 0; 0, -1, 0; 0, 0, 1]; 

w = [800; -200; -100; 200];

%%% Linear objective function %%%

% f(x1, x2, ..., xl) = c1 x1 + c2 x2 + ... + cl xl

 c = [2; 1; 3]; 
 
%%% Maximum value of f and a point where it is achieved %%% 
 
 [max_val, max_arg] = Optimisation(M, w, c)