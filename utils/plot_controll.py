import numpy as np
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu từ tệp văn bản
data = np.loadtxt(os.path.join(os.path.dirname(os.getcwd()), 'results','controll.txt'))


# Chia dữ liệu thành các cột
t_, v_, o = data[:, 0], data[:, 1], data[:, 2]


# Vẽ dữ liệu
plt.figure(figsize=(12, 8))

# Vẽ đường đi thực tế của x
plt.subplot(1, 2, 1)
plt.plot(t_, v_, label='V', color='blue')
plt.title("V")
plt.xlabel("Time Step")
plt.ylabel("V")
plt.grid(True)
plt.legend()

# Vẽ đường đi thực tế của y
plt.subplot(1, 2, 2)
plt.plot(t_, o, label='omega', color='green')
plt.title("omega")
plt.xlabel("Time Step")
plt.ylabel("Omega")
plt.grid(True)
plt.legend()



# Hiển thị tất cả biểu đồ
plt.tight_layout()
plt.show()
