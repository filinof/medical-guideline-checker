from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class CheckRequest(BaseModel):
    transcript: str
    guideline: str

@app.post("/check")
async def check_transcript(req: CheckRequest):
    prompt = f"""
Ты — медицинский эксперт. Сравни текст расшифровки речи врача с клиническими рекомендациями.

Вот рекомендации:
{req.guideline}

Вот текст визита:
{req.transcript}

Ответь, насколько визит соответствует клиническим рекомендациям? Укажи:
1. Степень соответствия в процентах
2. Какие пункты соблюдены
3. Какие пропущены
4. Общая оценка и рекомендации врачу по улучшению
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — строгий медицинский проверяющий."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"result": response["choices"][0]["message"]["content"]}

