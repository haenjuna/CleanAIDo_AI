from typing import Union

from fastapi import FastAPI, HTTPException

from my_chromadb.ExtractImage import extractImage
from my_openai.CreateSolution import createSolution
import time
app = FastAPI()


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


@app.get("/get-images")
async def get_file(file_name: str):
    """
    파일 이름을 받아 해당 파일의 각 줄을 배열로 반환하는 API 엔드포인트
    """
    print(file_name)
    try:
        result = extractImage(file_name)
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