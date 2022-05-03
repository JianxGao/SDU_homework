% 将特征与标签整合为一个变量，方便后续操作
clc
clear
data = [];

label = load('predataset/label.mat').label;

% % 拼接特征，形成数据集
% for j=1:15
%     for i=1:3
%        filename = strcat(num2str(j),'_',num2str(i),'.mat');
%        dat = load(filename).features;
%        data = cat(1,data,dat);
%     end
% end
% 
% label = repmat(label,1,45)';
% dataset = cat(2,data,label);
for i =1:15
    filename = strcat('anewdata',num2str(i),'.mat');
    dat = load(filename).featuresall;
    data = cat(1,data,dat);
end
label = repmat(label,1,45)';
dataset = cat(2,data,label);


