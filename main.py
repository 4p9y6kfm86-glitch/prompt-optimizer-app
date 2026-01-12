from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class PromptRequest(BaseModel):
    prompt: str

@app.post("/optimize")
def optimize_prompt(req: PromptRequest):
    instruction = (
        "あなたはプロンプトエンジニアリングスペシャリストです。"
        "次の文章をAI向けに最適化してください。\n"
        f"プロンプト: {req.prompt}\n"
        "最適化後:"
    )
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "あなたはプロンプト最適化の専門家です。"},
            {"role": "user", "content": instruction}
        ]
    )
    return {"optimized": response.choices[0].message.content}
