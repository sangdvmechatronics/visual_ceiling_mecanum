
## Khai báo thư viện cần thiết
import cv2


### chương trình chính

def main():
    cap = cv2.VideoCapture(2)
    # Xác định các thông số video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Lấy tốc độ khung hình mặc định từ camera
    
    # Tạo đối tượng VideoWriter để lưu video
    out = cv2.VideoWriter('2101_3.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 4, (954, 540))
    while True:
        ### cài đặt FPS 
        frame_rate = 10 
        ### Đọc hình ảnh từ camera và resize 960x540 
        ret, img = cap.read()
        #cv2.imshow("anh goc", img)
       
        img = cv2.resize(img, (954, 540))
        cv2.imshow("anh sau resize", img)
        #print("kích thước ảnh", img.shape[0], img.shape[1])
        ## thực hiện hiệu chỉnh và cắt anh 
        
        #cv2.circle(img, (int(pos_center_img[0]), int(pos_center_img[1])), 3,(0,0,255),1)
        print("kích thước ảnh", img.shape[1], img.shape[0])
        
        ## Lưu hình ảnh gốc chứ không phải hình ảnh sau hieijeu chỉnh
        out.write(img)

        print("fps :", fps)
        #cv2.imshow("anh_ban_dau", img)
        if cv2.waitKey(1) == ord('q'):
            break
            
    cap.release()
    out.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()