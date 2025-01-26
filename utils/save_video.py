# import pyrealsense2 as rs
# import numpy as np
# import cv2

# # Cấu hình luồng video
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

# # Bắt đầu luồng video
# pipeline.start(config)

# # Định nghĩa codec và tạo đối tượng VideoWriter để lưu video
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('lan5.avi', fourcc, 30, (848, 480))

# try:
#     while True:
#         # Lấy khung hình từ camera
#         frames = pipeline.wait_for_frames()
#         color_frame = frames.get_color_frame()

#         if not color_frame:
#             continue

#         # Chuyển đổi hình ảnh thành mảng numpy
#         color_image = np.asanyarray(color_frame.get_data())

#         # Hiển thị hình ảnh
#         cv2.imshow('RealSense', color_image)
#         print("runing...")
#         # Ghi hình ảnh vào tệp video
#         out.write(color_image)

#         # Nhấn 'q' để thoát
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# finally:
#     # Dừng luồng video
#     pipeline.stop()

#     # Giải phóng đối tượng VideoWriter và đóng cửa sổ hiển thị
#     out.release()
#     cv2.destroyAllWindows()


import pyrealsense2 as rs
import numpy as np
import cv2

# Cấu hình luồng camera
pipeline = rs.pipeline()
config = rs.config()

# Thiết lập độ phân giải và tốc độ khung hình
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

# Bắt đầu truyền dữ liệu từ camera
pipeline.start(config)

# Đặt tên file đầu ra và codec
output_file = 'realsense_output_1.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter(output_file, fourcc, 30.0, (848, 480))

try:
    while True:
        # Lấy frame từ camera
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Chuyển đổi hình ảnh thành numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Hiển thị video trực tiếp
        cv2.imshow('RealSense', color_image)

        # Ghi video vào file
        output.write(color_image)

        # Nhấn 'q' để dừng lại
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Dừng truyền dữ liệu từ camera
    pipeline.stop()
    # Đóng file video và cửa sổ
    output.release()
    cv2.destroyAllWindows()
