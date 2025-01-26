import rospy
from sensor_msgs.msg import Imu
import tf.transformations as tf
import os

# Biến lưu trữ thời gian và góc Euler lần đầu tiên
prev_time = None
initial_time = None
initial_euler = None

# Thời gian tích lũy bắt đầu từ 0
accumulated_time = 0.0

# Tên file để lưu kết quả
output_file = os.path.join(os.getcwd(), "results/imu_data.txt")
if os.path.exists(output_file):
    os.remove(output_file)
def imu_callback(msg):
    global prev_time, initial_time, accumulated_time, initial_euler

    # Lấy thời gian hiện tại từ header
    curr_time = msg.header.stamp.to_sec()

    # Thiết lập thời gian ban đầu
    if initial_time is None:
        initial_time = curr_time

    # Tính delta t và cập nhật thời gian tích lũy
    if prev_time is not None:
        delta_t = curr_time - prev_time
        accumulated_time += delta_t
        rospy.loginfo(f"Delta t: {delta_t:.6f} seconds")
    else:
        delta_t = 0.0  # Không có delta t lần đầu
    prev_time = curr_time

    # Lấy giá trị quaternion
    qx = msg.orientation.x
    qy = msg.orientation.y
    qz = msg.orientation.z
    qw = msg.orientation.w

    # Chuyển đổi quaternion sang góc Euler
    euler = tf.euler_from_quaternion([qx, qy, qz, qw])  # [roll, pitch, yaw]

    # Lưu giá trị Euler ban đầu nếu chưa có
    if initial_euler is None:
        initial_euler = euler
        rospy.loginfo(f"Initial Euler angles: roll={euler[0]:.6f}, pitch={euler[1]:.6f}, yaw={euler[2]:.6f}")

    # Tính toán góc Euler đã chuẩn hóa (trừ giá trị ban đầu)
    normalized_euler = [euler[i] - initial_euler[i] for i in range(3)]

    # Hiển thị kết quả
    rospy.loginfo(f"Accumulated time: {accumulated_time:.6f}, Normalized Euler angles: roll={normalized_euler[0]:.6f}, pitch={normalized_euler[1]:.6f}, yaw={normalized_euler[2]:.6f}")

    # Lưu kết quả vào file
    with open(output_file, "a") as f:
        f.write(f"{accumulated_time:.6f}\t{normalized_euler[0]:.6f}\t{normalized_euler[1]:.6f}\t{normalized_euler[2]:.6f}\n")

def main():
    # Tạo file và xóa nội dung cũ nếu tồn tại
    with open(output_file, "w") as f:
        pass

    rospy.init_node('imu_data_reader', anonymous=True)
    rospy.Subscriber('/imu/data', Imu, imu_callback)

    rospy.loginfo("Listening to /imu/data topic...")
    rospy.spin()

if __name__ == "__main__":
    main()
