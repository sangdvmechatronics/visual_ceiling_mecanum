#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import numpy as np
import time
from geometry_msgs.msg import Pose2D
# from sub_data_sensor import *
import cv2
import os

file_path = "results/controll.txt"
if os.path.exists(file_path):
    os.remove(file_path)
file_path = "results/quydaodieukhien.txt"
if os.path.exists(file_path):
    os.remove(file_path)
    file_path = "results/e.txt"
if os.path.exists(file_path):
    os.remove(file_path)


def read_pos_rb():
    try:
        # Lấy giá trị pos_rb từ parameter server
        pos_rb_values = rospy.get_param('pos_rb')
        print("pos_rb_values: ",pos_rb_values)
        if pos_rb_values:
            pos_rb = Pose2D()
            pos_rb.x, pos_rb.y, pos_rb.theta = pos_rb_values
            pos_rb_float = np.array([[pos_rb.x], [pos_rb.y], [pos_rb.theta]])
            return pos_rb_float
        else:
            print("No pos_rb data found.")
            return None
    except KeyError:
        print("pos_rb not found on parameter server.")
        return None


    

class PIDController:
    def __init__(self, v_max=0.2, w_max=0.2, a1=0.05, a2=0.05, b1=0.0, b2=0.0, c1=0.05, c2=0.05):
        self.v_max = v_max
        self.w_max = w_max
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2
        self.c1 = c1
        self.c2 = c2

    def transform_error(self, e):
        R_T = np.array([
            [np.cos(e[2][0]), np.sin(e[2][0]), 0],
            [-np.sin(e[2][0]), np.cos(e[2][0]), 0],
            [0, 0, 1]
        ])
        e_r = np.dot(R_T, e)
        return e_r

    def compute_pid_params(self, e_r):
        es = np.linalg.norm(e_r[:2])  
        self.Kp = self.a1 + self.a2 * es
        self.Ki = self.b1 - self.b2 * es
        self.Kd = self.c1 + self.c2 * es

    def compute_V_pid(self, e_r, ex_r_last, pre_integral_error_x , dt):
        integral_error_x = pre_integral_error_x +  e_r[0][0] * dt
        derivative_error = (e_r[0][0] - ex_r_last) / max(dt, 1e-16)
        ex_r_last = e_r[0][0] 
        eV = self.Kp * e_r[0][0] + self.Ki * integral_error_x + self.Kd * derivative_error
        pre_integral_error_x = integral_error_x
        return eV, ex_r_last, pre_integral_error_x


    def compute_o_pid(self, e_r, ey_r_last,  pre_integral_error_y , etheta_r_last, pre_integral_error_theta ,dt):

        integral_error_y = pre_integral_error_y +  e_r[1][0] * dt
        derivative_error_y = (e_r[1][0] - ey_r_last) / max(dt, 1e-16)
        ey_r_last = e_r[1][0]
        A = self.Kp * e_r[1][0] + self.Ki * integral_error_y + self.Kd * derivative_error_y

        integral_error_theta = pre_integral_error_theta + e_r[2][0] * dt
        derivative_error_theta = (e_r[2][0] - etheta_r_last) / max(dt, 1e-16)
        etheta_r_last = e_r[2][0]         
        B = self.Kp * e_r[2][0] + self.Ki * integral_error_theta + self.Kd * derivative_error_theta

        eO = A +B

        pre_integral_error_y = integral_error_y
        pre_integral_error_theta = integral_error_theta

        return eO, ey_r_last, etheta_r_last,  pre_integral_error_y, pre_integral_error_theta


    def compute_output(self, e, ex_r_last, ey_r_last, etheta_r_last, pre_integral_error_x, pre_integral_error_y, pre_integral_error_theta,pos_rb_d, dt):
        e_r = self.transform_error(e)
        self.compute_pid_params(e_r)
        eV, ex_r_last, pre_integral_error_x = self.compute_V_pid(e_r, ex_r_last, pre_integral_error_x , dt)
        eO, ey_r_last, etheta_r_last,  pre_integral_error_y, pre_integral_error_theta = self.compute_o_pid( e_r, ey_r_last,  pre_integral_error_y , etheta_r_last, pre_integral_error_theta ,dt)

        # V_G = pos_rb_d[4] + eV  ## van toc dieu khien
        # omega_controll =  pos_rb_d[5] + eO    ## omega dieu khien

        # V_G = pos_rb_d[4] * 0.88 * np.cos(e[2][0]) + 0.38 * e_r[0][0]   ## van toc dieu khien
        # omega_controll =  pos_rb_d[5] +  pos_rb_d[4]  * (0.88 * e_r[1][0]) + 0.95 * np.sin(e[2][0]) ## omega dieu khien
        V_G = pos_rb_d[4] *  np.cos(e[2][0]) + 0.2 * e_r[0][0]   ## van toc dieu khien
        omega_controll =  pos_rb_d[5] +  pos_rb_d[4]  * (0.2 * e_r[1][0]) + 0.2 * np.sin(e[2][0]) ## omega dieu khien

        print(" pos_rb_d[4]",  pos_rb_d[4])
        print(" pos_rb_d[5]",  pos_rb_d[5])

        if V_G >= self.v_max:
            V_G = self.v_max
        # if V_G < 0:
        #     V_G = 0
        if omega_controll >= self.w_max:
            omega_controll = self.w_max

        # if omega_controll <= - self.w_max:
        #     omega_controll = -self.w_max

        return V_G, omega_controll, ex_r_last, ey_r_last, etheta_r_last, pre_integral_error_x, pre_integral_error_y, pre_integral_error_theta


def read_target_data(file_path):
    with open(file_path, "r") as file:
        data = file.readlines()[1:]  # Bỏ qua dòng đầu tiên chứa tiêu đề
    
    # Đọc dữ liệu và tách thành các giá trị
    pos_rb_d = []
    for line in data:
        line = line.strip()
        if line:  # Kiểm tra dòng không rỗng
            values = line.split('\t')
            if len(values) == 7:  # Đảm bảo dòng có đúng 7 giá trị
                try:
                    # Chuyển đổi tất cả các giá trị thành float
                    pos_rb_d.append([float(x) for x in values])
                except ValueError:
                    print(f"Warning: Dòng có lỗi dữ liệu: {line}")
    
    # Gán vào các mảng numpy với 7 giá trị mỗi dòng
    return [np.array([[t], [x_d], [y_d], [theta_d], [V_d], [oz], [V_dot]]) 
            for t, x_d, y_d, theta_d, V_d, oz, V_dot in pos_rb_d]

if __name__ == "__main__":
    rospy.init_node('pid_controller_node')
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    target_data = read_target_data("quy_dao_v7.txt")

    pid = PIDController(v_max= 0.5, w_max = 0.5, a1 = 0.1, a2 = 0.1, b1 = 0.05, b2 = 0.05, c1 = 0.06, c2 = 0.06)

    later = time.time()

    # Thêm một biến flag để dừng vòng lặp khi nhận lệnh dừng
    flag = True
    pre_integral_error_x = 0
    pre_integral_error_y = 0
    pre_integral_error_theta = 0
    ex_r_last = 0
    ey_r_last = 0
    etheta_r_last = 0
    while flag:
        while not rospy.is_shutdown():
            try:
                for pos_rb_d in target_data:
                    if not flag:
                        break  # Dừng vòng lặp khi flag là False

                    # Đảm bảo vòng lặp chỉ diễn ra 0.1s
                    now = time.time()
                    dt = now - later
                    later = now
                    t_sys =+ dt
                    # print("dt:  ", t_sys)
                    pos_rb_float = read_pos_rb()



                    if pos_rb_float is not None:
                        print("pos_rb x:", pos_rb_float)
                    else:
                        print("pos_rb is None")

                    # Tính lỗi
                    print("pos_rb_d", pos_rb_d)


                
                    e1 = pos_rb_d[1] - pos_rb_float[0][0]
                    e2 = pos_rb_d[2] - pos_rb_float[1][0]
                    e3 = pos_rb_d[3] - pos_rb_float[2][0]

                    # print("etheta", e3)
                    e = np.array([[float(e1)], [float(e2)], [float(e3)]]).reshape(3,1)
                    print("e_check", e) 


                    # Tính toán điều khiển


                    V_G, omega_controll, ex_r_last, ey_r_last, etheta_r_last, pre_integral_error_x, pre_integral_error_y, pre_integral_error_theta = pid.compute_output(e, ex_r_last, ey_r_last, etheta_r_last, pre_integral_error_x, pre_integral_error_y, pre_integral_error_theta,pos_rb_d, dt)

                    # In kết quả
                    if pos_rb_float is not None:
                        print(f"t: {pos_rb_d[0][0]} ,V: {V_G}, Omega: {omega_controll}")

                        with open("results/controll.txt", "a") as fl:
                            fl.write(f"{float(pos_rb_d[0][0])}\t{float(V_G)}\t{float(omega_controll)}\n")

                        with open("results/quydaodieukhien.txt", "a") as fl:
                            fl.write(f"{float(pos_rb_d[0][0])}\t{float(pos_rb_float[0][0])}\t{float(pos_rb_float[1][0])}\t{float(pos_rb_float[2][0])}\n")

                        with open("results/e.txt", "a") as fl:
                            fl.write(f"{float(pos_rb_d[0][0])}\t{float(e[0][0])}\t{float(e[1][0])}\t{float(e[2][0])}\n")


                    # Tạo đối tượng Twist và gửi thông tin lên ROS
                    twist = Twist()
                    twist.linear.x = V_G
                    twist.angular.z = omega_controll
                    cmd_vel_pub.publish(twist)
                    print("da gui")

                    # Đảm bảo mỗi vòng lặp diễn ra đúng 0.1s
                    loop_duration = time.time() - now
                    sleep_time = max(0.1 - loop_duration, 0)
                    rospy.sleep(sleep_time)
                    print("------------------------------------------")
                flag = False

            except KeyboardInterrupt:
                print("Đã nhận lệnh dừng chương trình. Kết thúc.")
                running = False  # Đặt flag để dừng vòng lặp
                rospy.signal_shutdown("Program stopped by user.")
                # cmd_vel_pub.unregister()  # Ngừng phát lệnh cmd_vel
            flag = False


