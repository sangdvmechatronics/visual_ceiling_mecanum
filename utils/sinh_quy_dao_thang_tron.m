clear all;
close all;
clc; 
x(1) = 0; y(1) = 0; phi (1) = 0;
dt = 0.1; t(1) = 0;
for i = 2 : 1044
    t(i) = t(i-1)+dt;   
    vr(i) = 0.2; or(i) = 0;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i))*dt;
    y(i) = y(i-1) + vr(i)*sin(phi(i))*dt;
end
for i = 1045:1180
    t(i) = t(i-1)+dt;
    or(i) = -20/173 ; vr(i) = 1.73 * 20/173;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i))*dt;
    y(i) = y(i-1) + vr(i)*sin(phi(i))*dt;
end
for i = 1181:1719
    t(i) = t(i-1)+dt;
    vr(i) = 0.2; or(i) = 0;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i))*dt;
    y(i) = y(i-1) + vr(i)*sin(phi(i))*dt;
end
for i = 1720:1813
    t(i) = t(i-1)+dt;
    or(i) = 1/6; vr(i) = 1.2 *1/6;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i))*dt;
    y(i) = y(i-1) + vr(i)*sin(phi(i))*dt;
end
for i = 1814:2469
    t(i) = t(i-1)+dt;
    vr(i) = 0.2; or(i) = 0;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i))*dt;
    y(i) = y(i-1) + vr(i)*sin(phi(i))*dt;
end
% Khởi tạo V_dot
for i = 1:length(t)
    V_dot(i) = 0;
end

% Chuyển đổi mảng sang dạng cột
t = t'; x = x'; y = y'; phi = phi'; vr = vr'; or = or'; V_dot = V_dot';

% Xuất dữ liệu ra file .txt
data = [t, x, y, phi, vr, or, V_dot];
fileID = fopen('quy_dao_v7.txt', 'w');
fprintf(fileID, 't\tx_d\ty_d\ttheta_d\tVr\toz\tVdot\n'); % Tiêu đề
fprintf(fileID, '%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n', data');
fclose(fileID);

% Vẽ đồ thị
figure;
plot(x, y);
axis equal;
title('Quỹ đạo chuyển động');
xlabel('X (m)');
ylabel('Y (m)');

figure;
subplot(2, 1, 1);
plot(t, vr);
title('Vận tốc (vr) theo thời gian');
xlabel('Thời gian (s)');
ylabel('Vận tốc (m/s)');

subplot(2, 1, 2);
plot(t, or);
title('Tốc độ góc (or) theo thời gian');
xlabel('Thời gian (s)');
ylabel('Tốc độ góc (rad/s)');
