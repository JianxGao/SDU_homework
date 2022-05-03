function [signal_data,signal_fft] = pre_data(data)
    fs = 150;
    signal_data = [];
    signal_fft = [];
    for i=1:62
        channel = data(i,:);
        channel = resample(channel,fs,200);
        N = length(channel)-1;
        % 整体的快速傅里叶变换
        channel_fft = fft(channel);
        channel_fft = abs(channel_fft(1:N/2)*2/N);
        % 滤波，快速傅里叶变换
        % 滤得delta波
        [delta_data,delta_fft] = filter_and_fft([0.1*2 4*2]/fs,4,channel);
        % 滤得theta波
        [theta_data,theta_fft] = filter_and_fft([4*2 9*2]/fs,4,channel);
        % 滤得alpha波
        [alpha_data,alpha_fft] = filter_and_fft([8*2 12*2]/fs,4,channel);
%         [alpha_s_data,alpha_s_fft] = filter_and_fft([8*2 9*2]/fs,4,channel);
%         [alpha_m_data,alpha_m_fft] = filter_and_fft([9*2 12*2]/fs,4,channel);
%         [alpha_f_data,alpha_f_fft] = filter_and_fft([12*2 14*2]/fs,4,channel);
        % 滤得beta波
        [beta_data,beta_fft] = filter_and_fft([14*2 30*2]/fs,4,channel);
%         [beta_SMR_data,beta_SMR_fft] = filter_and_fft([12*2 16*2]/fs,4,channel);
%         [beta_sr_data,beta_sr_fft]   = filter_and_fft([16*2 20*2]/fs,4,channel);
%         [beta_hr_data,beta_hr_fft]   = filter_and_fft([20*2 30*2]/fs,4,channel);
        % 滤得gamma波
        [gamma_data,gamma_fft]   = filter_and_fft([30*2 50*2]/fs,4,channel);
        % 时域
        subdataset = [  channel    
                        delta_data
                        theta_data
                        alpha_data
%                         alpha_s_data
%                         alpha_m_data
%                         alpha_f_data
                        beta_data
%                         beta_SMR_data
%                         beta_sr_data
%                         beta_hr_data
                        gamma_data   ];
        % 频率
        sub_squence_fft = [ channel_fft    
                            delta_fft
                            theta_fft
                            alpha_fft
%                             alpha_s_fft
%                             alpha_m_fft
%                             alpha_f_fft
                            beta_fft
%                             beta_SMR_fft
%                             beta_sr_fft
%                             beta_hr_fft
                            gamma_fft   ];
        % dataset = subdataset;
        signal_data = [signal_data
                       subdataset];
        signal_fft = [signal_fft
                      sub_squence_fft];
    end
end