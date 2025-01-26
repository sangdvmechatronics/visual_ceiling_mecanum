#!/usr/bin/python3
import cv2
import numpy as np
import os
from pupil_apriltags import Detector
import time
import copy

families = 'tag36h11'
nthreads = 1
quad_decimate = 2.0
quad_sigma = 0.0
refine_edges = 1
decode_sharpening = 0.25
debug = 0 
at_detector = Detector(families=families,nthreads=nthreads,quad_decimate=quad_decimate,
                        quad_sigma=quad_sigma,refine_edges=refine_edges,decode_sharpening=decode_sharpening,debug=debug)

class detect_landmark():
    def __init__(self, img = None, show = True):
        self.img = img
        self.show = show


    def update_image(self, img):
        self.img = img


    def run_detect_tag(self):
        start_time = time.time()
        elapsed_time = 0
        if self.img is None:
            print("No image provided.")
            return None, None, None
        debug_image = copy.deepcopy(self.img)
        ## Xử lý trên ảnh gốc còn ảnh copy sẽ dùng để vẽ
        image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tags = at_detector.detect(image, estimate_tag_pose=False, camera_params=None, tag_size=None)
        center_list = []
        point_x = []
        tag_id = None

        center_list, point_x, tag_id, debug_image = self.draw_tags(debug_image, tags, center_list, point_x, tag_id)
        if self.show == True:
            cv2.imshow("debug_image", debug_image)
        return center_list, point_x, tag_id

        

    def draw_tags(self, debug_image, tags, center_list, point_x, tag_id):
        for tag in tags:
            tag_family = tag.tag_family
            tag_id = tag.tag_id
            center = tag.center
            corners = tag.corners


            center = (int(center[0]), int(center[1]))
            center_list.append(center)

            corner_01 = (int(corners[0][0]), int(corners[0][1]))
            corner_02 = (int(corners[1][0]), int(corners[1][1]))
            corner_03 = (int(corners[2][0]), int(corners[2][1]))
            corner_04 = (int(corners[3][0]), int(corners[3][1]))
          
            point_x = tuple( (x + y)/2 for x, y in zip(corner_04, corner_03))
            #print("point_x", point_x)
            cv2.circle(debug_image, (int(point_x[0]), int(point_x[1])), 1, (0, 0, 255), 2)
            cv2.circle(debug_image, (center[0], center[1]), 1, (0, 255, 0), 1)
        
            cv2.line(debug_image, (corner_01[0], corner_01[1]),
                    (corner_02[0], corner_02[1]), (255, 0, 0), 2)
            cv2.line(debug_image, (corner_02[0], corner_02[1]),
                    (corner_03[0], corner_03[1]), (255, 0, 0), 2)
            cv2.line(debug_image, (corner_03[0], corner_03[1]),
                    (corner_04[0], corner_04[1]), (0, 255, 0), 2)
            cv2.line(debug_image, (corner_04[0], corner_04[1]),
                    (corner_01[0], corner_01[1]), (0, 255, 0), 2)

        
        return center_list, point_x, tag_id, debug_image
        


































#     def show_image(self, debug_image):
#         cv2.imshow("image", debug_image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     def run_find_ROI(self):
#         center_list = []
#         center_list, point_x, tag_id, debug_image = self.run_detect_tag()
#         return center_list, point_x, tag_id, debug_image
# img = cv2.imread('april_tag_19.jpg')

# april_tag = detect_landmark(img)
# center_list = []
# april_tag.run_detect_tag()
# debug_image, center_list, point_x, tag_id = april_tag.draw_tags()
# april_tag.show_image()


## Thông tin lấy ra được là tâm hình QR và trung điểm số 1 và 2