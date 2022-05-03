%% 可视化部分
% 
clc
clear
close all;
figure,
hold on
fs = 200;

dat1_1 = load('predataset/1_1.mat');
data = dat1_1.djc_eeg1;

% 通道1
% channel = data(1,1:37000);
channel = data(18,:);
% channel1 = data(1,:);
% channel21 = data(21,:);
% channel41 = data(41,:);
% channel61 = data(61,:);
% plot(channel1(1:40000));
% plot(channel21(1:40000));
% plot(channel41(1:40000));
% plot(channel61(1:40000));
% legend('channel1','channel21','channel41','channel61')
% x_data = 1:600;
% plot(channel(1:40000))
% channel = low_pass_filter(50*2/fs,4,channel);
% channel = resample(channel,fs,200);
% plot(channel(1:40000))
% legend('initial signal','filtered signal')
N = length(channel); 
n = 0:N-1;
f = n*fs/N;

% 整体的快速傅里叶变换
channel_fft = fft(channel);
channel_fft = abs(channel_fft(1:floor(N/2)) * 2/N);
% 滤波，快速傅里叶变换
% 滤得delta波
[delta_data,delta_fft] = filter_and_fft([0.1*2 4*2]/fs,4,channel);
% 滤得theta波
[theta_data,theta_fft] = filter_and_fft([4*2 9*2]/fs,4,channel);
% 滤得alpha波
[alpha_data,alpha_fft] = filter_and_fft([8*2 12*2]/fs,4,channel);
[alpha_s_data,alpha_s_fft] = filter_and_fft([8*2 9*2]/fs,4,channel);
[alpha_m_data,alpha_m_fft] = filter_and_fft([9*2 12*2]/fs,4,channel);
[alpha_f_data,alpha_f_fft] = filter_and_fft([12*2 14*2]/fs,4,channel);
% 滤得beta波
[beta_data,beta_fft] = filter_and_fft([14*2 30*2]/fs,4,channel);
[beta_SMR_data,beta_SMR_fft] = filter_and_fft([12*2 16*2]/fs,4,channel);
[beta_sr_data,beta_sr_fft]   = filter_and_fft([16*2 20*2]/fs,4,channel);
[beta_hr_data,beta_hr_fft]   = filter_and_fft([20*2 30*2]/fs,4,channel);
% 滤得gamma波
[gamma_data,gamma_fft]   = filter_and_fft([30*2 50*2]/fs,4,channel);

% 时域
% plot(x_data,alpha_data(1501:2100))
% plot(x_data,alpha_s_data(1501:2100))
% plot(x_data,alpha_m_data(1501:2100))
% plot(x_data,alpha_f_data(1501:2100))
% plot(x_data,beta_data(1501:2100))
% plot(x_data,beta_SMR_data(1501:2100))
% plot(x_data,beta_sr_data(1501:2100))
% plot(x_data,beta_hr_data(1501:2100))
% 频域
% hold on
% legend('Initial FFT')
% xlim([5,40])
% plot(f(1:N/2),channel_fft)
% plot(f(1:N/2),delta_fft)
% plot(f(1:N/2),theta_fft)
plot(f(1:N/2),alpha_fft)
plot(f(1:N/2),alpha_s_fft)
plot(f(1:N/2),alpha_m_fft)
plot(f(1:N/2),alpha_f_fft)
% plot(f(1:N/2),beta_fft)
% plot(f(1:N/2),beta_SMR_fft)
% plot(f(1:N/2),beta_sr_fft)
% plot(f(1:N/2),beta_hr_fft)
% plot(f(1:N/2),gamma_fft)

% legend('initial signal','delta','theta','alpha','beta','gamma')
legend('alpha','alpha s','alpha m','alpha f')
% legend('beta','beta s','beta m','beta f')
