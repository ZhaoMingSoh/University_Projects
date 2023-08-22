clear
clc
%{

This script calls the function Optimisation to solve optimisation problems

(This particular example is from page 70 of the lecture notes on Maths IA
algebra that I used at Adelaide Uni.)

KB - May 2015

%}

%%% Constraints %%%

% Mx <= w

M=[400,500,520;50,70,40;70,80,150;30,40,50;1,1,1];

Waus=[700*10^3;70*10^3;100*10^3;50*10^3;1200];
Wind=[890*10^3;120*10^3;160*10^3;80*10^3;2100];
%The output capacity in Canada increases from 900 to 1200 from 2025 onwards 
Wcan1=[660*10^3;60*10^3;140*10^3;70*10^3;900]; %for 2021-2025
Wcan2=[660*10^3;60*10^3;140*10^3;70*10^3;1200];%for 2025 onwards

%%% Linear objective function %%%

% f(x1, x2, ..., xl) = c1 x1 + c2 x2 + ... + cl xl

%RPcountry=[Cubic RP,Traveller RP,Adventurer RP]
%RP=Retail Price in AUD
RPaus=[1.3*10^4,1.6*10^4,2*10^4];
RPind=[6.3*10^3,7.2*10^3,8.55*10^3];
RPcan=[1.18*10^4,1.39*10^4,1.66*10^4];

%SPcountry=[Steel SP,Glass SP,Rubber SP,Paint SP];
%SP=Supply Price
SPaus=[0.3,1.4,2.4,22];
SPind=[0.25,0.5,1.5,10];
SPcan=[0.4,1.5,2.5,26];

%Labour Costs
Laus=0.5;
Lind=0.2;
Lcan=0.45;

% Objective functions of each Country (including labour and material costs)
Caus=[RPaus(1)*(1-Laus)-SPaus*M(1:4,1);RPaus(2)*(1-Laus)-SPaus*M(1:4,3);RPaus(3)*(1-Laus)-SPaus*M(1:4,3)];
Cind=[RPind(1)*(1-Lind)-SPind*M(1:4,1);RPind(2)*(1-Lind)-SPind*M(1:4,3);RPind(3)*(1-Lind)-SPind*M(1:4,3)];
Ccan=[RPaus(1)*(1-Lcan)-SPcan*M(1:4,1);RPcan(2)*(1-Lcan)-SPcan*M(1:4,3);RPcan(3)*(1-Lcan)-SPcan*M(1:4,3)];

% Objective functions of each Country (excluding labour and material costs\)
Caus_1=[RPaus(1)*(1-Laus)-SPaus*M(1:4,1);RPaus(2)*(1-Laus)-SPaus*M(1:4,3);RPaus(3)*(1-Laus)-SPaus*M(1:4,3)];
Cind_1=[RPind(1)*(1-Lind)-SPind*M(1:4,1);RPind(2)*(1-Lind)-SPind*M(1:4,3);RPind(3)*(1-Lind)-SPind*M(1:4,3)];
Ccan_1=[RPaus(1)*(1-Lcan)-SPcan*M(1:4,1);RPcan(2)*(1-Lcan)-SPcan*M(1:4,3);RPcan(3)*(1-Lcan)-SPcan*M(1:4,3)];

%%% Maximum value of f and a point where it is achieved %%% 
%OPEX Per year
OPaus=1.2*10^6;
OPind=5*10^5;
OPcan=1.1*10^6;
 
 [max_val_aus, max_arg_aus] = Optimisation(M, Waus, Caus);
 [max_val_ind, max_arg_ind] = Optimisation(M, Wind, Cind);
 [max_val_can1, max_arg_can1] = Optimisation(M, Wcan1, Ccan);
 [max_val_can2, max_arg_can2] = Optimisation(M, Wcan2, Ccan);
 
 
 
 max_val_aus=max_val_aus-OPaus;
 max_val_ind=max_val_ind-OPind;
 max_val_can1=max_val_can1-OPcan;
 max_val_can2=max_val_can2-OPcan;
 
 %output
fprintf('Australia: max profit $%d\n', max_val_aus)
fprintf('Optimal Cubics %d\n', max_arg_aus(1))
fprintf('Optimal Travellers %d\n', max_arg_aus(2))
fprintf('Optimal Adventurers %d\n', max_arg_aus(3))

fprintf('\nIndonesia: max profit $%d\n', max_val_ind)
fprintf('Optimal Cubics %d\n', max_arg_ind(1))
fprintf('Optimal Travellers %d\n', max_arg_ind(2))
fprintf('Optimal Adventurers %d\n', max_arg_ind(3))

fprintf('\nCanada 2021-2025: max profit $%d\n', max_val_can1)
fprintf('Optimal Cubics %d\n', max_arg_can1(1))
fprintf('Optimal Travellers %d\n', max_arg_can1(2))
fprintf('Optimal Adventurers %d\n', max_arg_can1(3))

fprintf('\nCanada 2025 onwards: max profit $%d\n', max_val_can2)
fprintf('Optimal Cubics %d\n', max_arg_can2(1))
fprintf('Optimal Travellers %d\n', max_arg_can2(2))
fprintf('Optimal Adventurers %d\n', max_arg_can2(3))

fprintf('\nCanada Average: max profit $%d\n', (max_val_can1+max_val_can2)/2)



%Net Present Value
%Discount Rate = d
d=0.08;

%Number of years = n
n=9;

%Initial Investment amount in AUD
Invest=2*10^7;

aus=6.224447058823530e+06;
ind=9.276735294117646e+06;
can1=5.368299999999999e+06;
can2=6910900;

NPVaus=0;
NPVind=0;
NPVcan=0;

for i=0:n
        NPVaus=NPVaus+(aus/((1+0.08)^i));    
        NPVind=NPVind+(ind/(1+0.08)^i);     
    if i<5
        NPVcan=NPVcan+(can1/(1+0.08)^i);             
    else
        NPVcan=NPVcan+(can2/(1+0.08)^i);
    end       
end

fprintf('\n NPV\n AUS: %d, IND %d, CAN %d',NPVaus,NPVind,NPVcan)


