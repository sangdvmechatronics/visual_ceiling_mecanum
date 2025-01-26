#!/usr/bin/python3

import cv2
import os
import numpy as np
import time
from info_MĐV import *
import rospy


def get_euler_angles():

    # Lấy giá trị từ Parameter Server
    try:
        euler_angles = rospy.get_param('euler_angles')
        roll = euler_angles['roll']
        pitch = euler_angles['pitch']
        yaw = euler_angles['yaw']

        # rospy.loginfo(f"Roll: {roll:.6f}, Pitch: {pitch:.6f}, Yaw: {yaw:.6f}")
        return roll, pitch, yaw
    except KeyError:
        rospy.logwarn("Euler angles are not yet available on the parameter server.")
        return None
    

class calculate_position():
    
    def __init__(self,center_list, point_x, tag_id, dpi_x, dpi_y, size_img, theta_val_rad, r_BA):

        self.center_list = center_list
        self.point_x = point_x
        self.count = tag_id
        self.dpi_x = dpi_x
        self.dpi_y = dpi_y
        self.size_img = size_img
        self.theta_val_rad = theta_val_rad
        self.r_BA = r_BA


    # Tính toán khoảng cách 
    def calculate_distances(self):
        distances = []
        # đọc các tâm tìm trong toàn bộ ảnh rồi tính toán khoảng cách tới tâm ảnh
        for i , (centers) in enumerate(self.center_list):
            cx, cy = centers
            #### Cộng thêm quá trình hiệu chỉnh tâm robot về tam ảnh
            vx = cx - (self.size_img[0] / 2)              
            vy = cy - (self.size_img[1] / 2)
            distance = np.sqrt(vx**2 + vy**2)
            distances.append(distance) 
        # Tìm khoảng cách ngắn nhất và lấy thông tin
        distance_robot = min(distances)
        min_index = distances.index(distance_robot)
        min_cx, min_cy = self.center_list[min_index]    

        distance_robot *= self.dpi_x ### thực hiện hiểu chỉnh với thực tế
        return distance_robot, min_cx, min_cy

    # Tạo vectors ngắn nhất từ tâm đường tròn tới đường tròn  gần tâm ảnh crop nhất
    ## Dùng để tính theta
    def create_vector_X_crop(self):
        # Tâm ảnh crop thực hiển điều chỉnh cắt
        cx = self.size_img[0]/2
        cy = self.size_img[1]/2
        # print(f"cx: {cx}, cy: {cy}")
        # vector_X_cropped = None
        # global flag_rotate
        
        if len(self.point_x) > 0:
            center1 = self.point_x[0] # lấy tọa độ của điểm đầu tiên trong mảng
            center2 = self.point_x[1]# lấy tọa độ của điểm thứ hai trong mảng
            # print(center1, center2)
            #print(f"center1 {center1}, center2: {center2}")

            vector_X_cropped = np.array([center1-cx, center2-cy])
            # if (center1>cx) >= 0:
            #     flag_rotate = True
            # else:
            #     flag_rotate = False
            return vector_X_cropped
        # else:
        #     vector_X_cropped = None
        return None
    
    
    # Tạo vectors AB ( từ tâm hình tròn tới tâm ảnh) ( rB -rA)
    def create_vector_rAB(self, min_cx, min_cy):
        #### Cộng thêm quá trình hiệu chỉnh tâm robot về tam ảnh
        self.r_BA = np.array([(self.size_img[0]/2 - min_cx), (self.size_img[1]/2  - min_cy)])
        #print(self.r_BA)



    # Tính góc trục x (ảnh cropped) với phương ngang của ảnh
    def theta(self, vector_X_cropped):
        if vector_X_cropped is not None:
        # Tính góc bằng arctan2
            # print("vector_X_cropped[1]", vector_X_cropped[1])
            # print("vector_X_cropped[0]", vector_X_cropped[0])
            y1 = float(vector_X_cropped[1]* 0.088 / 26)
            x1 = float(vector_X_cropped[0]* 0.088 / 26)
            self.theta_val_rad = np.arctan2(y1, x1) 
            # # Kiểm tra vector_X_cropped[0] và điều chỉnh góc
            # if vector_X_cropped[0] < 0:
            #     self.theta_val_rad = self.theta_val_rad   # Giữ nguyên góc nếu x > 0
            # else:
            #     self.theta_val_rad = np.pi - self.theta_val_rad   # Điều chỉnh nếu x < 0
            
            # # Chuyển góc về khoảng [0, 2π] để đảm bảo luôn dương
            # self.theta_val_rad = np.mod(self.theta_val_rad, 2 * np.pi)

            # self.theta_val_rad = self.theta_val_rad  + np.pi

            return self.theta_val_rad
        else:
        # Trường hợp vector_X_cropped không hợp lệ
            print("vector_X_cropped is None or invalid")

    

    def pos_tranform_robot_to_landmank(self):
        
        c = np.cos(-self.theta_val_rad)
        s = np.sin(-self.theta_val_rad)
        # print("góc xoay", np.rad2deg(self.theta_val_rad))
        ## thực hiện tính theta theo chiều dương cùng chiều kim đồng hồ trục z hướng lên. đâm vào màn hình
        R1 = np.array([[c, -s , 0, 0],
                    [s, c, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        # cy = np.cos(np.pi)
        # sy = np.sin(np.pi)

        # R_y = np.array([[cy, 0, sy, 0],
        #                 [0, 1, 0, 0],
        #                 [-sy, 0, cy, 0],
        #                 [0, 0, 0, 1]])
        r_BA_array = np.array([[self.r_BA[0]],
            [self.r_BA[1]],
            [0],
            [1]])  
        r_B_i = np.dot(R1,r_BA_array)
        # r_B_i = np.dot(np.dot(R_y, R1) ,r_BA_array)


        r_B_i[0,0] *= self.dpi_x
        r_B_i[1,0] *= self.dpi_y
        r_B_i = np.array([[r_B_i[0,0]], [r_B_i[1,0]],[0], [1]])
        #print("r_B_i \n", r_B_i)
            # Ghi dữ liệu vào file
        with open("results/vitri_rb.txt", "a") as file:  # "a" để ghi tiếp dữ liệu
            file.write(f"{r_B_i[0, 0]}\t{r_B_i[1, 0]}\t{self.theta_val_rad}\n")
        return r_B_i 

    ## Thực hiện tính toán vị trí robot trong hệ tọa độ thực toàn cầu
    def pos_robot_to_global(self, r_B_i ):
        # print("asfdsf", theta_val_rad)
        tag_id = self.count
        # print("r_B_i", r_B_i)
        pos_robot_real = None
        if tag_id >= 0:
            T, r_O_i, phi = get_r_o_i_by_id(tag_id)

            # print("r0", r_O_i)

            if r_B_i is not None:
                r_B_g = r_O_i + np.dot(T, r_B_i)

                # Lấy giá trị yaw từ get_euler_angles
                euler_angles = get_euler_angles()
                if euler_angles is not None:
                    _, _, yaw = euler_angles
                else:
                    rospy.logwarn("Yaw is not available. Using default phi.")
                    yaw = phi  # Giá trị dự phòng nếu không lấy được yaw
                # Thay thế phi_r bằng yaw
                phi_r = yaw


                # theta_deg = np.rad2deg(self.theta_val_rad)
                # Kiểm tra vector_X_cropped[0] và điều chỉnh góc
                # if theta_deg > 0:
                #     theta_deg = theta_deg # Giữ nguyên góc nếu x > 0
                # else:
                #     theta_deg = theta_deg + 360   # Điều chỉnh nếu x < 0
                
                # phi_r = phi - self.theta_val_rad + np.pi


                pos_robot_real = [[r_B_g[0, 0]], [r_B_g[1,0]], [phi_r]]
        # print("pos_robot_real", pos_robot_real)
        #print(f"Pose_theta: {round(np.rad2deg(phi_r),2)} degree")
        return pos_robot_real
    
    def run_position(self):
        try:

            # distance_robot, min_cx, min_cy = self.calculate_distances()
            #print(f"minx { min_cx}, min y {min_cy}")
            # print("khoang cach", round(distance_robot,2))
            # cv2.circle(cropped_img, (int(self.point_x[0]), int(self.point_x[1])), 2, (255,0,0), 4)
            # vector_X_cropped = self.create_vector_X_crop()
            # print("vector_X_cropped", vector_X_cropped)

            # self.theta_val_rad = self.theta(vector_X_cropped)
            #self.create_vector_rAB(min_cx, min_cy)
            # print("r_BA", self.r_BA)

            r_B_i = self.pos_tranform_robot_to_landmank()
            #     fl.write(f"{float(r_B_i[0] )}\t{float(r_B_i[1]) }\n")

            # print("cec", self.theta_val_rad )
            #print("check point obj", self.point_x)

            result = self.pos_robot_to_global(r_B_i)
            # print(result)
            return result
        except Exception as e:
            print(f"Error: {e}")
            result = None
            return result

