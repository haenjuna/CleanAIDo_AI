# main.py
from .test2 import findImage  # test2.py에서 findImage 함수를 가져옴
import os

def extractImage(imageName):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    new_image_path = os.path.join(script_dir, 'tmpImage',imageName)
    print("usageImages" + new_image_path)

    results = findImage(new_image_path)

    print("=========================================================")
    for result in results:
        print(result)

    return results
