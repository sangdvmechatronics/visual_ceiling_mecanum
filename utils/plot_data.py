import numpy as np
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu từ tệp văn bản
data = np.loadtxt(os.path.join(os.path.dirname(os.getcwd()), 'results','vitri.txt'))
data_1 = np.loadtxt(os.path.join(os.path.dirname(os.getcwd()), 'results','vitri_rb.txt'))

# Chia dữ liệu thành các cột
x_, y_, theta_ = data[:, 0], data[:, 1], data[:, 2]
x_1, y_1, theta_1 = data_1[:, 0], data_1[:, 1], data_1[:, 2]

# Vẽ dữ liệu
plt.figure(figsize=(12, 8))

# Vẽ đường đi thực tế của x
plt.subplot(2, 3, 1)
plt.plot(x_, label='Actual Path X', color='blue', marker = "o", markersize = "1")
plt.title("X Position (Actual Path)")
plt.xlabel("Time Step")
plt.ylabel("X Position")
plt.grid(True)
plt.legend()

# Vẽ đường đi thực tế của y
plt.subplot(2, 3, 2)
plt.plot(y_, label='Actual Path Y', color='green', marker = "o", markersize = "1")
plt.title("Y Position (Actual Path)")
plt.xlabel("Time Step")
plt.ylabel("Y Position")
plt.grid(True)
plt.legend()

# Vẽ góc theta thực tế
plt.subplot(2, 3, 3)
plt.plot(theta_, label='Actual Path Y', color='red')
plt.title("Theta")
plt.xlabel("Time Step")
plt.ylabel("Theta (radians)")
plt.grid(True)
plt.legend()

# Vẽ quỹ đạo X-Y
plt.subplot(2, 3, 4)
plt.plot(x_, y_, label='Actual Path XY', color='purple',  markersize=1,  marker='o')
plt.title("Trajectory (X-Y)")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.axis("equal")
plt.grid(True)
plt.legend()

# Vẽ X từ file vitri_1.txt
plt.subplot(2, 3, 5)
plt.plot(x_1, label='Path X from vitri_1.txt', color='orange', linestyle='None',  markersize=5,  marker='o')
plt.title("X Position (File vitri_1.txt)")
plt.xlabel("Time Step")
plt.ylabel("X Position")
plt.grid(True)
plt.legend()

# Vẽ Y từ file vitri_1.txt
plt.subplot(2, 3, 6)
plt.plot(y_1, label='Path Y from vitri_1.txt', color='cyan', marker="o")
plt.title("Y Position (File vitri_1.txt)")
plt.xlabel("Time Step")
plt.ylabel("Y Position")
plt.grid(True)
plt.legend()

# Hiển thị tất cả biểu đồ
plt.tight_layout()
plt.show()
