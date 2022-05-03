function [newX,T,meanValue] = pca_method(X,CRate)
%每行是一个样本
%newX  降维后的新矩阵
%T 变换矩阵
%meanValue  X每列均值构成的矩阵，用于将降维后的矩阵newX恢复成X
%CRate 贡献率
%计算中心化样本矩阵
meanValue=ones(size(X,1),1)*mean(X);
X=X-meanValue;%每个维度减去该维度的均值
C=cov(x);%计算协方差矩阵
 
%计算特征向量V，特征值D
[V,D]=eig(C);
%将特征向量按降序排序
[dummy,order]=sort(diag(D),'descend');
V=V(:,order);%将特征向量按照特征值大小进行降序排列
d=diag(D);%将特征值取出，构成一个列向量
newd=d(order);%将特征值构成的列向量按降序排列
 
%取前n个特征向量，构成变换矩阵
sumd=sum(newd);%特征值之和
for j=1:length(newd)
    i=sum(newd(1:j,1))/sumd;%计算贡献率，贡献率=前n个特征值之和/总特征值之和
    if i>CRate%当贡献率大于95%时循环结束,并记下取多少个特征值
        cols=j;
        break;
   end
end
T=V(:,1:cols);%取前cols个特征向量，构成变换矩阵T
newX=X*T;%用变换矩阵T对X进行降维
end
