
## Khai báo thư viện cần thiết
import cv2
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)  # Lấy tốc độ khung hình mặc định từ camera
out = cv2.VideoWriter('video29_04_2_5m.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps,(width, height))
### chương trình chính

def main():
    i = 0
    while True:

        ret, img = cap.read()
        i +=1
        #cv2.imshow("anh_ban_dau", img)
        out.write(img)
        print("giay thu", i)
        
        if cv2.waitKey(1) == ord('q'):
            break
            
    cap.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
