from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Backend running"}

chat_history = {}

class ChatRequest(BaseModel):
    user_id: str
    query: str

@app.post("/chat")
def chat(req: ChatRequest):
    try:

        if req.user_id not in chat_history:
            chat_history[req.user_id] = []

        chat_history[req.user_id].append({"role": "user", "content": req.query})

        if len(chat_history[req.user_id]) > 8:
            chat_history[req.user_id] = chat_history[req.user_id][-8:]

        if not api_key:
            return {"error": "API Key not found. Please check your .env file."}

        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system",
                 "content": "You are a helpful Data Structure tutor. Explain concepts with clarity, examples, and visual thinking. Use previous context if follow-up question is unclear."
                 },
                *chat_history[req.user_id]
            ]
        )

        answer = response.choices[0].message.content

        # store bot response
        chat_history[req.user_id].append({"role": "assistant", "content": answer})

        return {"reply": answer}

    except Exception as e:
        return {"error": str(e)}

@app.post("/image-chat")
async def image_chat(
    user_id: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Read image
        image_bytes = await image.read()

        # Convert to base64
        img_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Create chat history for image user if not exists
        if user_id not in chat_history:
            chat_history[user_id] = []

        response = client.chat.completions.create(
            model="qwen/qwen-2.5-vl",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Data Structure tutor. Understand diagrams, images, handwritten notes and explain clearly like a teacher."
                },
                *chat_history[user_id],
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Explain this image in context of data structures. Identify what it is and teach me."
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    ],
                }
            ]
        )

        answer = response.choices[0].message.content

        chat_history[user_id].append({"role": "assistant", "content": answer})

        return {"reply": answer}

    except Exception as e:
        return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
