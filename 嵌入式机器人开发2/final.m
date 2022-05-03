%% 初始化
clc                     % 清空命令行
clear                   % 清空变量
close all;              % 关闭所有图例
% 根据D-H参数表生成机械臂模型
%          theta      d       a          alpha 
L(1) = Link([0,     151.9,   0,      deg2rad(-90)]);
L(2) = Link([0,     -86.85,  243.65, deg2rad(0)]);
L(3) = Link([0,     92.85,   213,    deg2rad(0)]);
L(4) = Link([0,     -83.4,   0,      deg2rad(90)]);
L(5) = Link([0,     83.4,    0,      deg2rad(90)]);
L(6) = Link([0,     300,     0,      deg2rad(0)]);
% 根据作业要求PDF文件中的要求添加机械臂限制
L(1).qlim = [-2*pi,2*pi];
L(2).qlim = [-2*pi,2*pi];
L(3).qlim = [-2*pi,2*pi];
L(4).qlim = [-2*pi,2*pi];
L(5).qlim = [-2*pi,2*pi];
% 生成机械臂
UR3 = SerialLink(L,'name','UR3');
% 可视化机械臂，并初始化位置信息，使得机械臂竖直
view(3);                            % 展开三维视图
UR3.teach([pi -pi/2 0 pi/2 0 0])
hold on;
%%
% 球面半径
R = 650;
% 球心坐标
xx=400;
yy=1000;
zz=300;
% 生成球面
[x y z] = sphere(100);
surfl(R * x + xx, R * y + yy, R * z + zz);
shading interp;
% 山大字样位置偏置变量
bias = 0;
bias2 = -83;

% 计算轨迹
% 计算“山” 第一画，即 竖
% 调用自定义函数get_tracks
p1 = get_tracks(deg2rad(60:1:90-bias),deg2rad(155-bias2),R,xx,yy,zz);

% 过渡，计算初始位置到“山”的第一画
start_point = [0,377.4,691.95];
p_s = mtraj(@tpoly , start_point,p1(:,1)',20)';

% 计算“山” 第二画，即 竖
p2 = get_tracks(deg2rad(78:1:90 - bias),deg2rad(142-bias2),R,xx,yy,zz);

% 过渡，连接“山”第一画的末尾与第二画的开头
p12 = mtraj(@tpoly , p1(:,30)', p2(:,1)', 10)';  

% 计算“山” 第三画，即 横
p3 = get_tracks(deg2rad(90 - bias),deg2rad((142:1:168) - bias2),R,xx,yy,zz);

% 计算“山” 第四画，即 竖
p4 = get_tracks(deg2rad(78:1:90 - bias),deg2rad(168 - bias2),R,xx,yy,zz);

% 过渡，连接“山”第三画的末尾与第四画的开头
p34 = mtraj(@tpoly , p3(:,27)', p4(:,1)', 10)';  

% 计算“大” 第一画 横
p5 = get_tracks(deg2rad(76 - bias),deg2rad((175:1:201) - bias2),R,xx,yy,zz);

% 过渡，连接“山”第四画的末尾与第四画的开头
p45 = mtraj(@tpoly , p4(:,13)', p5(:,1)', 15)';  

% 计算“大 第二画，即 竖
p6 = get_tracks(deg2rad(60:1:76 - bias),deg2rad(188 - bias2),R,xx,yy,zz);

% 过渡，连接“大”第一画的末尾与第二画的开头
p56 = mtraj(@tpoly , p5(:,27)',p6(:,1)', 20)';

% 计算“大 第三画，即撇
a1 =         188;
b1 =     0.02837;
c1 =       18.24;
theta_deg = 76:1:90 - bias;
phi_deg = a1.*sin(b1.*theta_deg+c1);
p7 = get_tracks(deg2rad(theta_deg),deg2rad(phi_deg-bias2),R,xx,yy,zz);

% 过渡，连接“大”第三画的末尾与第四画的开头
theta_deg = 76:0.5:90 - bias;
phi_deg = a1.*sin(b1.*theta_deg+c1);
p78 = get_tracks(deg2rad(theta_deg),deg2rad(phi_deg-bias2),R,xx,yy,zz);
p7 = [p7 fliplr(p78)];

% 计算“大 第四画，即捺
na_a = 0.0744;
na_b = -11.42;
na_c = 626.4;
theta_deg = 76:1:90 - bias;
phi_deg = na_a.*theta_deg.*theta_deg+na_b*theta_deg+na_c;
theta = deg2rad(theta_deg);
phi = deg2rad(phi_deg-bias2);
p8 = get_tracks(theta,phi,R,xx,yy,zz);

% 计算“大”的第四画到离开球面的轨迹
final_point = [-750,50,80];
p_f = mtraj(@tpoly , p8(:,15)',final_point, 80)';

% 画出轨迹
plot3(p1(1,:),p1(2,:),p1(3,:),'r');
% plot3(p12(1,:),p12(2,:),p12(3,:),'g');    %过渡曲线
plot3(p2(1,:),p2(2,:),p2(3,:),'r');
plot3(p3(1,:),p3(2,:),p3(3,:),'r');
plot3(p4(1,:),p4(2,:),p4(3,:),'r');
% plot3(p45(1,:),p45(2,:),p45(3,:),'g');    %过渡曲线
plot3(p5(1,:),p5(2,:),p5(3,:),'r');
plot3(p6(1,:),p6(2,:),p6(3,:),'r');
% plot3(p56(1,:),p56(2,:),p56(3,:),'g');    %过渡曲线
plot3(p7(1,:),p7(2,:),p7(3,:),'r');
plot3(p8(1,:),p8(2,:),p8(3,:),'r');
 
% 轨迹合并
track = [p_s,p1,p12,p2,p3,p34,p4,p45,p5,p56,p6,p7,p8,p_f];
% 计算位子矩阵并移动
T = transl(track');
q = UR3.ikine(T,'mask',[1 1 1 0 0 0]);
UR3.teach(q);


