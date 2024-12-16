from typing import Union

from fastapi import FastAPI, HTTPException, File, UploadFile

from my_chromadb.ExtractImage import extractImage
from my_openai.CreateSolution import createSolution
import time
import os
import shutil
app = FastAPI()

UPLOAD_FOLDER = "./usageImages"
UPLOAD_TEMP_FOLDER = "./tmpImage"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/aa")
def read_aa():
    print("aaaaaaaa")
    return {"Hello": "Worlds"}




@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/get-images")
async def get_file(file: UploadFile = File(...)):
    # 파일 이름 가져오기
    file_name = file.filename
    print("file_name :"+file_name)
    # 파일 경로 설정
    file_path = os.path.join(UPLOAD_TEMP_FOLDER, file_name)
    print("file_path :"+file_path)

    # 이미지 파일 저장
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    print(file_name)
    try:
        result = extractImage(file_name)
        shutil.rmtree(UPLOAD_TEMP_FOLDER, ignore_errors=True)
        os.makedirs(UPLOAD_TEMP_FOLDER, exist_ok=True)
        return result # 배열 형태로 반환
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-solution")
async def get_solution(keywords: str):

    try:
        generate_solution_start = time.time()
        result = createSolution(keywords)
        generate_solution_end = time.time()
        solution_time = generate_solution_end - generate_solution_start
        print("solution time :" + str(solution_time))
        return result # 배열 형태로 반환
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/registImg")
async def registImg(file: UploadFile = File(...)):
    # 파일 이름 가져오기
    file_name = file.filename

    # 파일 경로 설정
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    # 이미지 파일 저장
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file_name, "message": "File uploaded successfully"}