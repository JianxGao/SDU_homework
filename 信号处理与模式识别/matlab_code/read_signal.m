%% 加载数据集
clc
clear
close all;
dat1_1 = load('predataset/1_1.mat');
dat1_2 = load('predataset/1_2.mat');
dat1_3 = load('predataset/1_3.mat');
dat2_1 = load('predataset/2_1.mat');
dat2_2 = load('predataset/2_2.mat');
dat2_3 = load('predataset/2_3.mat');
dat3_1 = load('predataset/3_1.mat');
dat3_2 = load('predataset/3_2.mat');
dat3_3 = load('predataset/3_3.mat');
dat4_1 = load('predataset/4_1.mat');
dat4_2 = load('predataset/4_2.mat');
dat4_3 = load('predataset/4_3.mat');
dat5_1 = load('predataset/5_1.mat');
dat5_2 = load('predataset/5_2.mat');
dat5_3 = load('predataset/5_3.mat');
% dat6_1 = load('predataset/6_1.mat');
% dat6_2 = load('predataset/6_2.mat');
% dat6_3 = load('predataset/6_3.mat');
% dat7_1 = load('predataset/7_1.mat');
% dat7_2 = load('predataset/7_2.mat');
% dat7_3 = load('predataset/7_3.mat');
% dat8_1 = load('predataset/8_1.mat');
% dat8_2 = load('predataset/8_2.mat');
% dat8_3 = load('predataset/8_3.mat');
% dat9_1 = load('predataset/9_1.mat');
% dat9_2 = load('predataset/9_2.mat');
% dat9_3 = load('predataset/9_3.mat');
% dat10_1 = load('predataset/10_1.mat');
% dat10_2 = load('predataset/10_2.mat');
% dat10_3 = load('predataset/10_3.mat');
% dat11_1 = load('predataset/11_1.mat');
% dat11_2 = load('predataset/11_2.mat');
% dat11_3 = load('predataset/11_3.mat');
% dat12_1 = load('predataset/12_1.mat');
% dat12_2 = load('predataset/12_2.mat');
% dat12_3 = load('predataset/12_3.mat');
% dat13_1 = load('predataset/13_1.mat');
% dat13_2 = load('predataset/13_2.mat');
% dat13_3 = load('predataset/13_3.mat');
% dat14_1 = load('predataset/14_1.mat');
% dat14_2 = load('predataset/14_2.mat');
% dat14_3 = load('predataset/14_3.mat');
% dat15_1 = load('predataset/15_1.mat');
% dat15_2 = load('predataset/15_2.mat');
% dat15_3 = load('predataset/15_3.mat');

%% 合并数据集，方便操作
initial1 =[dat1_1,dat1_2,dat1_3]; 
initial2 =[dat2_1,dat2_2,dat2_3];    
initial3 =[dat3_1,dat3_2,dat3_3]; 
initial4 =[dat4_1,dat4_2,dat4_3]; 
initial5 =[dat5_1,dat5_2,dat5_3]; 
% initial6 =[dat6_1,dat6_2,dat6_3]; 
% initial7 =[dat7_1,dat7_2,dat7_3]; 
% initial8 =[dat8_1,dat8_2,dat8_3]; 
% initial9 =[dat9_1,dat9_2,dat9_3]; 
% initial10 =[dat10_1,dat10_2,dat10_3];
% initial11 =[dat11_1,dat11_2,dat11_3];
% initial12 =[dat12_1,dat12_2,dat12_3];
% initial13 =[dat13_1,dat13_2,dat13_3];
% initial14 =[dat14_1,dat14_2,dat14_3];
% initial15 =[dat15_1,dat15_2,dat15_3];

%% 滤波并特征提取
get_data(initial1,1);
get_data(initial2,2);
get_data(initial3,3);
get_data(initial4,4);
get_data(initial5,5);
% get_data(initial6,6);
% get_data(initial7,7);
% get_data(initial8,8);
% get_data(initial9,9);
% get_data(initial10,10);
% get_data(initial11,11);
% get_data(initial12,12);
% get_data(initial13,13);
% get_data(initial14,14);
% get_data(initial15,15);

