# main.py
from .test2 import findImage  # test2.py에서 findImage 함수를 가져옴

# extractImage 함수 정의
def extractImage(imagePath):
    # 비교할 새로운 이미지 경로
    new_image_path = f"C:\\KDTFinalProject\\CleanAIDo_customer_back\\upload\\{imagePath}"
    results = findImage(new_image_path)  # findImage 함수를 호출하여 결과 받기

    print("=========================================================")
    for result in results:
        print(result)  # 유사 이미지 파일명 출력

    return results

