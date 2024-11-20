import cv2
import numpy as np

# 그리기 관련 파라미터
drawing = False  # 마우스 클릭 중이면 True
ix, iy = -1, -1  # 초기 x, y 좌표

# 세그먼테이션(주석)을 저장할 리스트
annotations = []

# 마우스 콜백 함수: 윤곽선을 그리기 위한 함수
def draw_contour(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        annotations.append([(x, y)])  # 새 윤곽선 시작

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # 현재 윤곽선에 점을 추가
            annotations[-1].append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # 마지막 점과 첫 번째 점을 연결하여 윤곽선을 닫음
        annotations[-1].append((x, y))

# 윤곽선의 바운딩 박스(x, y, w, h)를 계산하는 함수
def get_bounding_box(contour):
    points = np.array(contour, dtype=np.int32)
    x, y, w, h = cv2.boundingRect(points)  # 바운딩 박스 계산
    return x, y, w, h

# 이미지를 세그멘테이션하고 주석을 받는 함수
def segment_image(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        print("이미지를 찾을 수 없습니다!")
        return

    # 이미지 복사본을 만들어서 주석 표시
    annotated_image = image.copy()
    cv2.namedWindow("Image Segmentation")
    cv2.setMouseCallback("Image Segmentation", draw_contour)

    while True:
        # 복사본에 주석을 표시
        temp_image = annotated_image.copy()
        for contour in annotations:
            # 윤곽선의 바운딩 박스를 계산
            x, y, w, h = get_bounding_box(contour)
            # 바운딩 박스를 이미지에 그리기
            cv2.rectangle(temp_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 이미지에 주석을 표시
        cv2.imshow("Image Segmentation", temp_image)
        
        # 's'를 눌러 주석 저장, 'c'를 눌러 주석 지우기, 'q'를 눌러 종료
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            # 바운딩 박스를 저장
            with open("annotations.txt", "w") as f:
                for contour in annotations:
                    x, y, w, h = get_bounding_box(contour)
                    f.write(f"{x},{y},{w},{h}\n")  # 바운딩 박스 좌표 저장
            print("주석이 annotations.txt에 저장되었습니다.")
        elif key == ord("c"):
            # 주석 지우기
            annotations.clear()
            annotated_image = image.copy()
            print("주석이 지워졌습니다.")
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()

# 예시 사용법
if __name__ == "__main__":
    PathNames = r"C:\Users\cic\Desktop\awwdd\Picture"
    segment_image(PathNames + "//000000016598.jpg")
