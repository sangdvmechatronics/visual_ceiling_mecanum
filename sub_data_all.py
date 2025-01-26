#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Imu
import tf.transformations as tf
import os

# Biến toàn cục
pos_rb = Pose2D()
initial_euler = None

# Hàm callback cho dữ liệu Pose2D
def position_callback(data):
    global pos_rb
    pos_rb.x = data.x
    pos_rb.y = data.y
    pos_rb.theta = data.theta

    # Lưu giá trị pos_rb vào Parameter Server
    rospy.set_param('pos_rb', [pos_rb.x, pos_rb.y, pos_rb.theta])
    rospy.loginfo("---Updated pos_rb---")
    # rospy.loginfo(f"Updated pos_rb: x={pos_rb.x}, y={pos_rb.y}, theta={pos_rb.theta}")

# Hàm callback cho dữ liệu IMU
def imu_callback(msg):
    global initial_euler

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
        # rospy.loginfo(f"Initial Euler angles: roll={euler[0]:.6f}, pitch={euler[1]:.6f}, yaw={euler[2]:.6f}")

    # Tính toán góc Euler đã chuẩn hóa (trừ giá trị ban đầu)
    normalized_euler = [euler[i] - initial_euler[i] for i in range(3)]

    # Hiển thị kết quả
    # rospy.loginfo(f"Normalized Euler angles: roll={normalized_euler[0]:.2f}, pitch={normalized_euler[1]:.2f}, yaw={normalized_euler[2]:.2f}")

    # Lưu giá trị góc Euler đã chuẩn hóa vào Parameter Server
    rospy.set_param('euler_angles', {
        'roll': normalized_euler[0],
        'pitch': normalized_euler[1],
        'yaw': normalized_euler[2]
    })
    rospy.loginfo("---Updated imu data---")

# Hàm khởi tạo node và subscriber
def main():
    rospy.init_node('visual_odometry_imu_node', anonymous=True)

    # Subscriber cho topic Pose2D
    rospy.Subscriber('data_xla', Pose2D, position_callback)

    # Subscriber cho topic IMU
    rospy.Subscriber('/imu/data', Imu, imu_callback)
    # Tần số xử lý dữ liệu 20 Hz
    rate = rospy.Rate(20)  
    while not rospy.is_shutdown():
        rospy.loginfo("Listening to topics: /imu/data and data_xla...")
        rate.sleep()  # Duy trì tần số 20 Hz

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
