#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import time
import argparse
import numpy as np
import cv2 as cv
from pupil_apriltags import Detector
from pre_process import *
from find_ROI import *
from calcu import *
from bdk_test import *

import rospy
from geometry_msgs.msg import Pose2D


def publish_robot_position(pub, x, y, theta):
    """
    Publish the robot's position (x, y, theta) to the ROS topic.
    """
    pos = Pose2D()
    pos.x = x
    pos.y = y
    pos.theta = theta
    # rospy.loginfo(f"Publishing: x={x}, y={y}, theta={theta}")
    pub.publish(pos)

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
    
def main():

    # args = get_args(video_path= "data/2101_2.mp4")
    args = get_args()

    cap_width = args.width
    cap_height = args.height

    families = args.families
    nthreads = args.nthreads
    quad_decimate = args.quad_decimate
    quad_sigma = args.quad_sigma
    refine_edges = args.refine_edges
    decode_sharpening = args.decode_sharpening
    debug = args.debug


    # size_img = (811, 449)
    # size_img_resize = (1272, 720)

    ## chuan kich thuoc voi realsense camera
    # size_img = (848, 480)
    # size_img_crop = (50,50)

    ### kich thuoc anh sau khi resize va hieu chinh voi chuan 954 540
    size_img = (954, 540)
    size_img_resize = (954, 540)
    size_img_crop = (66,66)

    dpi_x = (0.088 / 45)
    dpi_y = (0.088 / 65)
    





    # Open video file or camera
    if args.video:
        cap = cv.VideoCapture(args.video)
    else:
        cap = cv.VideoCapture(2)  # Default to camera



    if not cap.isOpened():
        print("Error: Unable to open video or camera.")
        return

    # Detector
    at_detector = Detector(
        families=families,
        nthreads=nthreads,
        quad_decimate=quad_decimate,
        quad_sigma=quad_sigma,
        refine_edges=refine_edges,
        decode_sharpening=decode_sharpening,
        debug=debug,
    )


        # Parse arguments
    rospy.init_node('robot_position_publisher', anonymous=True)
    pub = rospy.Publisher('data_xla', Pose2D, queue_size=10)
    rate = rospy.Rate(20)  # 20 Hz publishing rate




    file_path = "results/vitri.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    file_path = "results/vitri_rb.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    camera_matrix_file = "assets/camera_matrix_lib"
    april_tag_detector = detect_landmark(show=False)
    april_tag_detector_crop = detect_landmark(show=False)
    previous_position = np.array([[0], [0], [0]])
    actual_position = np.array([[0], [0], [0]])
    pos_robot_real = np.array([[0], [0], [0]])

    robot = calculate_position(center_list = None, point_x = None, tag_id = None, dpi_x = dpi_x, dpi_y = dpi_y, size_img = size_img, theta_val_rad = None, r_BA = None ) ## img_big
    robot_crop = calculate_position(center_list = None, point_x = None, tag_id = None, dpi_x = dpi_x, dpi_y = dpi_y, size_img = size_img_crop, theta_val_rad = None, r_BA = None ) ## img_crop
    pid = PIDController(v_max= 0.2, w_max= 0.2, a1=0.6, a2=0.6, b1=0.004, b2=0.004, c1=0.06, c2=0.06)
    
    while True:
        ret, image = cap.read()
        if not ret:
            print("End of video or cannot read frame.")
            break

        image = cv.resize(image, size_img_resize)
        K_camera_matrix = np.load(camera_matrix_file + "/camera_matrix.npy")
        loaded_dist = np.load(camera_matrix_file + "/dist_coeffs.npy")
        

        image = get_images(image, K_camera_matrix, K_camera_matrix, loaded_dist, size_img_resize)
        # print("image_size", image.shape)

        image = cv.resize(image, size_img_resize)
        # print("image_size", image.shape)

        debug_image = copy.deepcopy(image)
        image_1 = image.copy()
        image_2 = image.copy()

        april_tag_detector.update_image(image_1)
        center_list, point_x, tag_id = april_tag_detector.run_detect_tag()
        # print("chekck point tag obj", point_x)

        robot.center_list = center_list
        robot.point_x = point_x
        #print("chekck point robot obj", robot.center_list)
        robot.count = tag_id
        print("count_robot", tag_id)
        if tag_id is not None:
            #print("tag_id : ", tag_id)
            if len(center_list) > 0:
                distance_robot, min_cx, min_cy = robot.calculate_distances()
                # print(f"min_cx_checkchekc {min_cx}, min_cx:{min_cy}")

                # print("distance_object", distance_robot)
                robot.create_vector_rAB(min_cx, min_cy)
                # print("rBA", robot.r_BA)
                cropped_img = crop_ROI_tags(image, min_cx, min_cy)
                if cropped_img is not None:
                    cropped_img_copy = cropped_img.copy()
                    april_tag_detector_crop.update_image(cropped_img)
                    # cv.imshow("crop!!", april_tag_detector_crop.img)
                    center_list_2, point_x_2, tag_id_2 = april_tag_detector_crop.run_detect_tag()
                    # print("tag_id_2_check", center_list_2)
                    # Cập nhật các giá trị mới vào đối tượng robot_crop
                    robot_crop.center_list = center_list_2
                    robot_crop.point_x = point_x_2
                    robot_crop.count = tag_id_2
                    vector_X_cropped = robot_crop.create_vector_X_crop()
                    #print("vector_X_cropped_check", vector_X_cropped)
                    # print("tag_id_2_check_robot_crop", tag_id_2)
                    # robot_crop.run_position(cropped_img_copy)
                    # print("robot_crop.run_position", robot_crop.run_position(cropped_img_copy))
                    # kiem tra ket qua
                    # print("point_x_2", point_x_2)
                   # # Tính điểm kết thúc vector trong ảnh
                    if len(point_x_2)>=2:
                        end_point = (int(point_x_2[0]), int(point_x_2[1]))
                        # print("end_point", end_point)
                        # Vẽ vector lên ảnh
                        start_point = (int(robot_crop.size_img[0]/2), int(robot_crop.size_img[1]/2))  # Tâm ảnh
                        color = (255, 255, 0)  # Màu xanh lá
                        thickness = 2  # Độ dày đường vẽ
                        cv.arrowedLine(cropped_img_copy, start_point, end_point, color, thickness)
                        cv.circle(cropped_img_copy, (int(point_x_2[0]), int(point_x_2[1])), 1, (0, 0, 255), 2)


                        start_point_1 = ((int(size_img[0]/2)), int(size_img[1]/2))  # Tâm ảnh

                        end_point_1 = (int(min_cx), int(min_cy))
                        cv.arrowedLine(image_2, end_point_1, start_point_1, color, thickness)

                        robot_theta_val_rad = robot_crop.theta(vector_X_cropped)
                        robot.theta_val_rad =  robot_theta_val_rad
                        
                        #print("cec robot crop", robot_theta_val_rad)
                        if robot_theta_val_rad is not None:
                            theta_deg = np.rad2deg(robot_theta_val_rad)
                             # # Kiểm tra vector_X_cropped[0] và điều chỉnh góc
                            if theta_deg > 0:
                                theta_deg = theta_deg # Giữ nguyên góc nếu x > 0
                            else:
                                theta_deg= theta_deg + 360   # Điều chỉnh nếu x < 0
                            
                            # print("theta_val_rad_arctan (do)", theta_deg)

                        r_B_i = robot.pos_tranform_robot_to_landmank()
                        pos_robot_real = None

                        if r_B_i is not None:
                            pos_robot_real = robot.pos_robot_to_global(r_B_i)
                            #print("count_robot_sau-cung", robot.count)

                            # Hiển thị hình ảnh
                    # cv.imshow("Image", image_2)
                    # cv.imshow("Processed Image", cropped_img_copy)
        #print("pos_robot_real", pos_robot_real)
        # Cập nhật giá trị trước đó
        if pos_robot_real is not None:
            previous_position = pos_robot_real
        else:
            pos_robot_real = previous_position
        roll, pitch, yaw = get_euler_angles()
        pos_robot_real[2][0] = float(yaw)

        # Gán giá trị cuối cùng
        if pos_robot_real is not None:
            x_actual = pos_robot_real[0][0]
            y_actual = pos_robot_real[1][0]
            theta_actual = float(yaw)

            # if theta_actual >= 2 * np.pi:
            #     theta_actual = theta_actual - 2 * np.pi
            # theta_actual = np.deg2rad(theta_actual)

            theta_r =  np.rad2deg(theta_actual)

            print(f"x:  {round(x_actual, 3)}, y:  {round(y_actual, 3)}, theta: {round(theta_r, 3)} do")

            if x_actual is not None:
                with open("results/vitri.txt", "a") as fl:
                    fl.write(f"{float(x_actual)}\t{float(y_actual)}\t{float(theta_actual)}\n")
        ######## Publish position to ROS topic
        publish_robot_position(pub, x_actual, y_actual, theta_actual)
        rate.sleep()
        
        print("\n")

        # Exit on ESC key
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
