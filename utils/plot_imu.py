import os
import matplotlib.pyplot as plt  # type: ignore
import numpy as np

# Đường dẫn file đầu vào
input_file = os.path.join(os.path.dirname(os.getcwd()), "results/2101_3/imu_data.txt")

# Kiểm tra nếu file tồn tại
if not os.path.exists(input_file):
    raise FileNotFoundError(f"File {input_file} không tồn tại!")

# Đọc dữ liệu từ file
data = np.loadtxt(input_file, delimiter="\t")

# Tách các cột dữ liệu
time = data[:, 0]
roll = data[:, 1]
pitch = data[:, 2]
yaw = data[:, 3]

# Vẽ đồ thị
plt.figure(figsize=(10, 6))

# Roll
plt.plot(time, roll, label='Roll', color='r', linestyle='-', marker='o', markersize=4)

# Pitch
plt.plot(time, pitch, label='Pitch', color='g', linestyle='--', marker='s', markersize=4)

# Yaw
plt.plot(time, yaw, label='Yaw', color='b', linestyle='-.', marker='^', markersize=4)

# Thiết lập tiêu đề và nhãn
plt.title("Góc Roll, Pitch, Yaw theo thời gian", fontsize=14)
plt.xlabel("Thời gian (s)", fontsize=12)
plt.ylabel("Góc (radian)", fontsize=12)
plt.legend(loc="best")
plt.grid(True)



plt.show()