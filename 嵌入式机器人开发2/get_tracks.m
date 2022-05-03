% 根据球坐标参数方程，计算机械臂轨迹点
function points = get_tracks(theta,phi,R,xx,yy,zz)
    if length(phi)==1
        points = [
            R * sin(theta) * cos(phi) + xx; 
            R * sin(theta) * sin(phi) + yy; 
            R * cos(theta) + zz
        ];
    end
    if length(theta)==1
        points = [
            R * sin(theta) * cos(phi) + xx; 
            R * sin(theta) * sin(phi) + yy; 
            R * cos(zeros(1,length(phi))+theta) + zz
        ];
    end
    if length(theta)~=1 && length(phi)~=1
        points = [
            R * sin(theta) .* cos(phi) + xx; 
            R * sin(theta) .* sin(phi) + yy; 
            R * cos(theta) + zz 
        ];
    end
end