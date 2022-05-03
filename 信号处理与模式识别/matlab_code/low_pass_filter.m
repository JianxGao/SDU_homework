function data = low_pass_filter(Wn,n,signal)
% Wn: 归一化截止频率
% n: 阶数
% signal: 需要滤波的信号
% 获取巴特沃斯滤波器参数
[b,a]=butter(n, Wn,'low');
data = filtfilt(b,a,signal);
end
