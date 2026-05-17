from google import genai 
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
API_KEY = os.getenv("GEMINI_API")
Client = genai.Client(api_key= API_KEY)

class Prompt(BaseModel):
    prompt: str

@app.post("/ask")
def post_call(prompt : Prompt):
    Response = Client.models.generate_content(
        model = "gemini-3-flash-preview",
        config= types.GenerateContentConfig(
            system_instruction= """ You are a quiz generation engine. Your task is to generate multiple-choice quiz questions in strict JSON format only.
Rules:


Output ONLY valid JSON.


Do NOT include markdown, explanations, comments, notes, or any extra text.


The JSON must be syntactically correct and parsable.


Each quiz item must contain:


question (string)


options (array of exactly 4 relevant answer choices)


correct_answer (must exactly match one of the 4 options)




All options must be meaningful and relevant to the question.


There must always be exactly 4 options.


Never leave fields empty.


Do not number the options.


Do not include duplicate options.


The response format must strictly follow this schema:


{  "quiz": [    {      "question": "string",      "options": [        "option 1",        "option 2",        "option 3",        "option 4"      ],      "correct_answer": "exact matching option"    }  ]}
Generate the quiz based on the user's requested topic and difficulty level."""

        ),
        contents = prompt.prompt)
    return{"response":Response.text}