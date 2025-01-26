import numpy as np
import matplotlib.pyplot as plt

# Khởi tạo biến
x, y, phi, vr, or_, t = [0], [0], [0], [], [], [0]
dt = 0.1

# Tính toán dữ liệu
for i in range(1, 1045):
    t.append(t[-1] + dt)
    vr.append(0.2)
    or_.append(0)
    phi.append(phi[-1] + or_[-1] * dt)
    x.append(x[-1] + vr[-1] * np.cos(phi[-1]) * dt)
    y.append(y[-1] + vr[-1] * np.sin(phi[-1]) * dt)

for i in range(1045, 1181):
    t.append(t[-1] + dt)
    or_.append(-20 / 173)
    vr.append(1.73 * 20 / 173)
    phi.append(phi[-1] + or_[-1] * dt)
    x.append(x[-1] + vr[-1] * np.cos(phi[-1]) * dt)
    y.append(y[-1] + vr[-1] * np.sin(phi[-1]) * dt)

for i in range(1181, 1720):
    t.append(t[-1] + dt)
    vr.append(0.2)
    or_.append(0)
    phi.append(phi[-1] + or_[-1] * dt)
    x.append(x[-1] + vr[-1] * np.cos(phi[-1]) * dt)
    y.append(y[-1] + vr[-1] * np.sin(phi[-1]) * dt)

for i in range(1720, 1814):
    t.append(t[-1] + dt)
    or_.append(1 / 6)
    vr.append(1.2 * 1 / 6)
    phi.append(phi[-1] + or_[-1] * dt)
    x.append(x[-1] + vr[-1] * np.cos(phi[-1]) * dt)
    y.append(y[-1] + vr[-1] * np.sin(phi[-1]) * dt)

for i in range(1814, 2470):
    t.append(t[-1] + dt)
    vr.append(0.2)
    or_.append(0)
    phi.append(phi[-1] + or_[-1] * dt)
    x.append(x[-1] + vr[-1] * np.cos(phi[-1]) * dt)
    y.append(y[-1] + vr[-1] * np.sin(phi[-1]) * dt)

# Khởi tạo V_dot
V_dot = [0] * len(t)

# Chuyển đổi sang mảng NumPy
t = np.array(t)
x = np.array(x)
y = np.array(y)
phi = np.array(phi)
vr = np.array(vr)
or_ = np.array(or_)
V_dot = np.array(V_dot)

# Kiểm tra và xử lý kích thước không đồng nhất
min_length = min(len(t), len(x), len(y), len(phi), len(vr), len(or_), len(V_dot))
t = t[:min_length]
x = x[:min_length]
y = y[:min_length]
phi = phi[:min_length]
vr = vr[:min_length]
or_ = or_[:min_length]
V_dot = V_dot[:min_length]

# Xuất dữ liệu ra file .txt
data = np.column_stack((t, x, y, phi, vr, or_, V_dot))
header = 't\tx_d\ty_d\ttheta_d\tVr\toz\tVdot'
np.savetxt('quy_dao_v7.txt', data, header=header, fmt='%.6f', delimiter='\t', comments='')

# Vẽ đồ thị
plt.figure()
plt.plot(x, y)
plt.axis('equal')
plt.title('Quỹ đạo chuyển động')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(t, vr)
plt.title('Vận tốc (vr) theo thời gian')
plt.xlabel('Thời gian (s)')
plt.ylabel('Vận tốc (m/s)')

plt.subplot(2, 1, 2)
plt.plot(t, or_)
plt.title('Tốc độ góc (or) theo thời gian')
plt.xlabel('Thời gian (s)')
plt.ylabel('Tốc độ góc (rad/s)')

plt.show()
