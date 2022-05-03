function signalentropy = entropy(channel)
p = hist(channel(:),length(channel));% 根据信号长度得到直方图
p = p/sum(p);
i = find(p);
signalentropy = -sum(p(i).*log2(p(i)));%计算信源熵
end