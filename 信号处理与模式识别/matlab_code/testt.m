clc
clear

initial_dataset1 = load('predataset/2_1.mat');
initial_dataset2 = load('predataset/2_2.mat');
initial_dataset3 = load('predataset/2_3.mat');
initial_dataset4 = load('predataset/3_1.mat');
initial_dataset5 = load('predataset/3_2.mat');
initial_dataset6 = load('predataset/3_3.mat');
initial_dataset7 = load('predataset/4_1.mat');
initial_dataset8 = load('predataset/4_2.mat');
initial_dataset9 = load('predataset/4_3.mat');
initial1 =[initial_dataset1,initial_dataset2,initial_dataset3]; 
initial2 =[initial_dataset4,initial_dataset5,initial_dataset6]; 
initial3 =[initial_dataset7,initial_dataset8,initial_dataset9]; 
iniital = [initial1,initial2,initial3]
% for i=1:2
%     filename = strcat('test',num2str(i),'.mat')
%     a  = data(i).djc_eeg1;
%     save(filename, 'a');
% end