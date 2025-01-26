#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
import cv2
import numpy as np
import os
import argparse



def crop_ROI_tags(img, min_cx, min_cy):
    if os.path.exists('img/landmark.jpg'):
        os.remove('img/landmark.jpg')
    x1, y1 = int(min_cx - 35), int(min_cy - 35)
    x2, y2 = int(min_cx + 35), int(min_cy + 35)
    if x1 >= 0 and y1 >= 0 and x2 <= img.shape[1] and y2 <= img.shape[0]:

        cropped_img = img[y1:y2, x1:x2]
        # cv2.imshow("crop", cropped_img)
        # Lưu ảnh vào thư mục img
        cv2.imwrite('img/landmark.jpg', cropped_img)
        return cropped_img


def get_images(image, K_camera_matrix, loaded_mtx, loaded_dist, size_img_resize):
    # Thực hiện hiệu chỉnh ảnh (undistort)
    undistorted_img = cv2.undistort(image, loaded_mtx, loaded_dist, None, K_camera_matrix)
    
    # Tính toán ROI từ ma trận camera mới
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(loaded_mtx, loaded_dist, size_img_resize, alpha=1)
    
    # Áp dụng ROI để cắt ảnh chính xác
    # chinh dung bang kich thuoc anh de tranh bi cut image nhe ! dmm
    x, y, w, h = 0, 0, 954, 540
    undistorted_img = undistorted_img[y:y+h, x:x+w]
    
    return undistorted_img

def get_args(video_path = None):
    parser = argparse.ArgumentParser()

    # parser.add_argument("--video", type=str, default= 2, help="Path to input video file")
    parser.add_argument("--video", type=str, default=video_path, help="Path to input video file")

    parser.add_argument("--width", help="Video width", type=int, default=954)
    parser.add_argument("--height", help="Video height", type=int, default=540)

    parser.add_argument("--families", type=str, default="tag36h11")
    parser.add_argument("--nthreads", type=int, default=1)
    parser.add_argument("--quad_decimate", type=float, default=2.0)
    parser.add_argument("--quad_sigma", type=float, default=0.0)
    parser.add_argument("--refine_edges", type=int, default=1)
    parser.add_argument("--decode_sharpening", type=float, default=0.25)
    parser.add_argument("--debug", type=int, default=0)
    args = parser.parse_args()

    return args
