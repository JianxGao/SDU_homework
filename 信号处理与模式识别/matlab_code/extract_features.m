function features = extract_features(squence_data,squence_fft)
for x = 1:3
    % 保存的文件名    
    filename = strcat(num2str(num),'_',num2str(x),'2222.mat')
    initial_dataset = initial(x);

    fs = 200;

    fileds = fieldnames(initial_dataset);
    features = [];
    for index=1:length(fileds)
        k = fileds(index);
        key = k{1};
        data = initial_dataset.(key);
        % 开始滤波并合并数据
        channel = data(1,:);
        N = length(channel);
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
        [gamma_data,gamma_fft]   = filter_and_fft([30*2 75*2]/fs,4,channel);
        % 合并数组
        % 时域
        squence_data = [channel    
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
        % 频域
        squence_fft = [ channel_fft    
                        delta_fft
                        theta_fft
                        alpha_fft
%                         alpha_s_fft
%                         alpha_m_fft
%                         alpha_f_fft
                        beta_fft
%                         beta_SMR_fft
%                         beta_sr_fft
%                         beta_hr_fft
                        gamma_fft   ];
        for i=2:62
            channel = data(i,:);
            N = length(channel);
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
%             [alpha_s_data,alpha_s_fft] = filter_and_fft([8*2 9*2]/fs,4,channel);
%             [alpha_m_data,alpha_m_fft] = filter_and_fft([9*2 12*2]/fs,4,channel);
%             [alpha_f_data,alpha_f_fft] = filter_and_fft([12*2 14*2]/fs,4,channel);
            % 滤得beta波
            [beta_data,beta_fft] = filter_and_fft([14*2 30*2]/fs,4,channel);
%             [beta_SMR_data,beta_SMR_fft] = filter_and_fft([12*2 16*2]/fs,4,channel);
%             [beta_sr_data,beta_sr_fft]   = filter_and_fft([16*2 20*2]/fs,4,channel);
%             [beta_hr_data,beta_hr_fft]   = filter_and_fft([20*2 30*2]/fs,4,channel);
            % 滤得gamma波
            [gamma_data,gamma_fft]   = filter_and_fft([30*2 75*2]/fs,4,channel);
            % 时域
            subdataset = [  channel    
                            delta_data
                            theta_data
                            alpha_data
%                             alpha_s_data
%                             alpha_m_data
%                             alpha_f_data
                            beta_data
%                             beta_SMR_data
%                             beta_sr_data
%                             beta_hr_data
                            gamma_data   ];
            % 频率
            sub_squence_fft = [ channel_fft    
                                delta_fft
                                theta_fft
                                alpha_fft
%                                 alpha_s_fft
%                                 alpha_m_fft
%                                 alpha_f_fft
                                beta_fft
%                                 beta_SMR_fft
%                                 beta_sr_fft
%                                 beta_hr_fft
                                gamma_fft   ];
            % dataset = subdataset;
            squence_data = cat(1,squence_data,subdataset);
            squence_fft = cat(1,squence_fft,sub_squence_fft);
        end
        % 特征提取
        feather = [];
        for i=1:744
            A = squence_data(i,:);% 时域特征提取部分
            B = squence_fft(i,:);% 频域
            % 时域         
            feather = [feather,mean(A)];
            feather = [feather,std(A)];
            feather = [feather,std(A)/mean(A)];
            feather = [feather,min(A)];
            feather = [feather,max(A)];
            feather = [feather,max(A)-min(A)];
            feather = [feather,iqr(A)]; % 4分位数
            % 后加的
            feather = [feather,mean(abs(A).^2)];% 功率
            feather = [feather,entropy(A)];% 信息熵
            feather = [feather,mean(abs(A))];% 绝对值的平均值(整流平均值)
            feather = [feather,kurtosis(A)];% 峰度
            feather = [feather,skewness(A)];% 偏度
            feather = [feather,rms(A)/mean(abs(A))];% 波形因子
            feather = [feather,(max(A)-min(A))/rms(A)];% 峰值因子
            feather = [feather,(max(A)-min(A))/mean(abs(A))];% 脉冲因子
            feather = [feather,(max(A)-min(A))/mean(sqrt(abs(A)))^2];% 裕度因子
            % 频域
            feather = [feather,mean(B)];
            feather = [feather,std(B)];
            feather = [feather,std(B)/mean(B)];
            feather = [feather,min(B)];
            feather = [feather,max(B)];
            feather = [feather,meanfreq(B)];
            feather = [feather,skewness(B)];
            feather = [feather,kurtosis(B)]; 
            feather = [feather,mean(abs(B).^2);];% 功率
            feather = [feather,entropy(B)];% 信息熵
        end
        features = [features
                    feather];
    end
    save(filename, 'features');
end