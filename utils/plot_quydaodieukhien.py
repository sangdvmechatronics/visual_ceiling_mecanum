import numpy as np
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu từ tệp văn bản
data = np.loadtxt(os.path.join(os.path.dirname(os.getcwd()), 'results', 'quydaodieukhien.txt'))
data_1_path = os.path.join(os.path.dirname(os.getcwd()), 'quy_dao_v7.txt')
with open(data_1_path, "r") as file:
    data_one = file.readlines()[1:]  # Bỏ qua dòng đầu tiên chứa tiêu đềls
# Đọc dữ liệu và tách thành các giá trị
data_1 = []
for line in data_one:
    line = line.strip()
    if line:  # Kiểm tra dòng không rỗng
        values = line.split('\t')
        if len(values) == 7:  # Đảm bảo dòng có đúng 7 giá trị
            # Chuyển đổi tất cả các giá trị thành float
            data_1.append([float(x) for x in values])

# Chuyển data_1 thành numpy array
data_1 = np.array(data_1)

# Đọc dữ liệu từ file e.txt
data_2 = np.loadtxt(os.path.join(os.path.dirname(os.getcwd()), 'results', 'e.txt'))

# Chia dữ liệu thành các cột
t_, x_, y_, theta_ = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
t_1, x_r, y_r, theta_r, V_r, o_r = data_1[:, 0], data_1[:, 1], data_1[:, 2], data_1[:, 3], data_1[:, 4],data_1[:, 5],
t_2, ex, ey, etheta = data_2[:, 0], data_2[:, 1], data_2[:, 2], data_2[:, 3]



# Vẽ dữ liệu
plt.figure(figsize=(12, 6))

# Đồ thị 1: x, y, x_r, y_r
plt.subplot(1, 1, 1)
plt.plot(x_, y_, label='r', color='blue', linestyle='-')
plt.plot(x_r, y_r, label='f', color='blue', linestyle='--')
plt.title("quy dao ")
plt.xlabel("X(m)")
plt.ylabel("Y(m)")
plt.axis("equal")
plt.legend()
plt.grid()


plt.figure(figsize=(12, 6))
# Đồ thị 2: theta, theta_r
plt.subplot(1, 1, 1)
plt.plot(t_, theta_, label='r', color='red', linestyle='-')
plt.plot(t_1, theta_r, label='f', color='orange', linestyle='--')
plt.title("Góc quay (theta) và góc tham chiếu (theta_r)")
plt.xlabel("Thời gian (t)")
plt.ylabel("Góc (rad)")
plt.legend()
plt.grid()

# Vẽ đồ thị e_x, e_y, e_theta
# plt.figure(figsize=(10, 6))
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t_2, ex, label='e_x', color='blue', linestyle='-')
plt.plot(t_2, ey, label='e_y', color='green', linestyle='-')
plt.grid()
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_2, etheta, label='e_theta', color='red', linestyle='-')
plt.title("sai so")
plt.xlabel("Thời gian (t)")
plt.ylabel("gia tri")
plt.legend()
plt.grid()


# Đọc dữ liệu từ tệp văn bản
data_three = np.loadtxt(os.path.join(os.path.dirname(os.getcwd()), 'results','controll.txt'))


# Chia dữ liệu thành các cột
t_3, v_, o = data_three[:, 0], data_three[:, 1], data_three[:, 2]


# Vẽ dữ liệu
plt.figure(figsize=(12, 8))

# Vẽ đường đi thực tế của x
plt.subplot(2, 1, 1)
plt.plot(t_3, v_, label='V', color='blue')
plt.plot(t_1, V_r, label='V_f', color='red')
plt.title("V")
plt.xlabel("Time Step")
plt.ylabel("V")
plt.grid(True)
plt.legend()

# Vẽ đường đi thực tế của y
plt.subplot(2, 1, 2)
plt.plot(t_3, o, label='omega', color='green')
plt.plot(t_1, o_r, label='o_f', color='red')
plt.title("omega")
plt.xlabel("Time Step")
plt.ylabel("Omega")
plt.grid(True)
plt.legend()


# Hiển thị tất cả biểu đồ
plt.tight_layout()
plt.show()
