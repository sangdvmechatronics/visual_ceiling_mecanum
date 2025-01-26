% Đọc dữ liệu từ tệp kết quả
data = load('output_results_1.txt');

% Tách dữ liệu thành các cột riêng
x_actual = data(:, 4);
y_actual = data(:, 5);
theta_actual = data(:, 6);

figure(1)
subplot(3,1,1)
plot(x_actual,"-r")
subplot(3,1,2)
plot(y_actual,"-r")
subplot(3,1,3)
plot(theta_actual,"-r")
grid on;



% Vẽ biểu đồ giá trị x_actual và y_actual (đường đi của robot)
figure(2);
plot(x_actual, y_actual, '-o');
xlabel('X position (meters)');
ylabel('Y position (meters)');
title('Trajectory of Robot');
axis equal
grid on;

% Vẽ biểu đồ giá trị theta_actual (góc hướng của robot)
% figure;
% plot(theta_actual);
% xlabel('Time step');
% ylabel('Theta (radians)');
% title('Orientation of Robot');
% grid on;
