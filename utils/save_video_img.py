import cv2
import os

# Đường dẫn tới video
output_folder = os.path.join(os.path.dirname(os.getcwd()),"data/save_video_img")


# Thư mục để lưu các khung hình
video_path = os.path.join(os.path.dirname(os.getcwd()),"data/data_1201/1101_lan3.mp4")
# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Mở video
cap = cv2.VideoCapture(video_path)

# Kiểm tra xem video có được mở thành công không
if not cap.isOpened():
    print("Không thể mở video!")
    exit()

frame_number = 0

# Đọc các khung hình từ video
while True:
    ret, frame = cap.read()  # Đọc từng khung hình
    if not ret:  # Nếu không đọc được khung hình, thoát vòng lặp
        break
    
    # Tạo tên file cho khung hình
    frame_filename = os.path.join(output_folder, f"{frame_number}_img.jpg")
    cv2.imshow("img", frame)
    # Lưu khung hình
    cv2.imwrite(frame_filename, frame)
    
    # Tăng số thứ tự khung hình
    frame_number += 1

# Giải phóng bộ nhớ
cap.release()
print(f"Đã lưu {frame_number} khung hình vào thư mục {output_folder}")
