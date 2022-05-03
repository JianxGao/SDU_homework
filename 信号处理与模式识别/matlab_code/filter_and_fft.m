function [newdata,fftdata] = filter_and_fft(Wn,n,signal)
% Wn: 归一化截止频率
% n: 阶数
% signal: 需要滤波的信号

% 获取巴特沃斯滤波器参数
[b,a] = butter(n,Wn,'bandpass');
N = length(signal);
% 滤波
data = filtfilt(b,a,signal);
% 快速傅里叶变换
fftdata = fft(data);
newdata = ifft(fftdata);
fftdata = abs(fftdata(1:floor(N/2))*2/N);
end