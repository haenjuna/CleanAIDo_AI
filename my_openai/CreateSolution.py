import openai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.environ.get('GPT_API_KEY')


def createSolution(input_keyword):
    message_content = ("이제부터 너에게 키워드들과 현재 사용자의 질문을 줄거야, 질문은 없을 수도 있어, 키워드들에는 청소를 해야할 부분과, "
                       "거기서 쓰이는 청소물품들이 있어 여기서 네가 할일은 키워드에있는 청소물품으로 청소를 해야할 부분의 청소방법을"
                       "알려주는거야") + input_keyword

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "you are a cleaning expert."},
            {"role": "user", "content": message_content},
        ],
        temperature=0.5
    )

    solution = response['choices'][0]['message']['content']  # 요약된 내용 반환
    return solution
