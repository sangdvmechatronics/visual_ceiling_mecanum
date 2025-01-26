import cv2
import os

# Tạo thư mục lưu ảnh nếu chưa tồn tại
output_dir = os.path.join(os.path.dirname(os.getcwd()), "data/calib_image")
os.makedirs(output_dir, exist_ok=True)

# Khởi tạo camera
cap = cv2.VideoCapture(2)
if not cap.isOpened():
    print("Không thể mở camera.")
    exit()

image_index = 1

while True:
    # Đọc khung hình từ camera
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc dữ liệu từ camera.")
        break
    frame = cv2.resize(frame, (1280,720))
    # Hiển thị khung hình
    cv2.imshow("Camera", frame)

    # Lắng nghe phím bấm
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        # Lưu ảnh khi nhấn phím 's'
        image_path = os.path.join(output_dir, f"img_{image_index}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Ảnh được lưu: {image_path}")
        image_index += 1

    elif key == 27:  # Phím ESC
        print("Thoát chương trình.")
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
