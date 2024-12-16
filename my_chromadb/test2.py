# test2.py
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import chromadb
import os
import time

# CLIP 모델과 프로세서 초기화
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


# 이미지 파일을 로드하고 임베딩 생성
def get_image_embedding(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embeddings = model.get_image_features(**inputs)
    return embeddings.squeeze().numpy()


# ChromaDB 클라이언트와 컬렉션 초기화
client = chromadb.Client()
collection = client.create_collection("image_embeddings")


# 이미지 임베딩을 ChromaDB에 저장하는 함수
def findImage(new_image_path):

    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_folder = os.path.join(script_dir, 'usageImages')
    print("usageImages" + image_folder)

    # 이미지 폴더에서 이미지를 DB에 추가
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        embedding = get_image_embedding(image_path)

        collection.add(
            ids=[image_file],  # 이미지 파일명을 고유 ID로 사용
            documents=[image_file],  # 문서로 이미지 파일명 추가
            embeddings=[embedding]  # 임베딩 추가
        )
    print("213213213213213")

    # 새로운 이미지 임베딩 생성
    generate_embed_start = time.time()
    new_embedding = get_image_embedding(new_image_path)
    generate_embed_end = time.time()
    embed_elpased_time = generate_embed_end - generate_embed_start
    print("embedding time :"+ str(embed_elpased_time))

    # ChromaDB에서 유사 이미지 검색
    search_start = time.time()
    results = collection.query(query_embeddings=[new_embedding], n_results=5)  # top_k는 검색 결과 개수
    search_end = time.time()
    search_elapsed_time = search_end - search_start
    print("searching time :"+str(search_elapsed_time))

    return results["documents"]  # 반환된 documents 리스트 반환
