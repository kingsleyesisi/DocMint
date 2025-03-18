import os
import uuid
import hashlib
import platform
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Define the API model 

client = genai.Client(api_key="AIzaSyAkXyGaJGcBM8mWjzsRiHcv2xTUUtiauvI")

load_dotenv()

app = FastAPI(title="Docmint API")

class GenerateReadmeRequest(BaseModel):
    projectType: str
    projectFiles: list[str]
    fullCode: str
    userInfo: dict = None

def generate_cache_key(projectType: str, projectFiles: list[str], fullCode: str) -> str:
    combined = projectType + "".join(projectFiles) + fullCode
    return f"readme:{hashlib.sha256(combined.encode('utf-8')).hexdigest()}"

@app.post("/generate-readme")
async def generate_readme(request: Request):
    body = await request.json()
    try:
        req_data = GenerateReadmeRequest(**body)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Missing required fields in request body")

    if (not req_data.projectType or not req_data.projectFiles or not req_data.fullCode or 
        (req_data.userInfo is None and platform.system().lower() != "linux")):
        raise HTTPException(status_code=400, detail="Missing required fields in request body")

    userInfo = req_data.userInfo or {}
    username = userInfo.get("username")
    email = userInfo.get("email")
    if not username:
        raise HTTPException(status_code=400, detail="Missing OS username and ID")
    user_id = userInfo.get("id") or str(uuid.uuid4())

    prompt = f"""
Generate a **high-quality, professional, and modern README.md** for a **{req_data.projectType}** project.

## Project Overview:
The project includes the following files:
{chr(10).join(req_data.projectFiles)}

## Full Code Context:
Below is the actual source code:
{req_data.fullCode}

## README Requirements:
1. **Analyze the project** and determine what sections are needed. Include the following sections if applicable:
   - **Title**: A clear and concise title for the project.
   - **Description**: A brief but engaging description of the project.
   - **Installation**: Step-by-step instructions for setting up the project locally.
   - **Usage**: Clear instructions on how to use the project.
   - **Features**: A list of key features.
   - **Technologies Used**: List of technologies, frameworks, and tools.
   - **Contributing**: Guidelines for contributing.
   - **License**: Information about the project's license.

2. **Tone and Style**:
   - For a **modern** project, use emojis, badges, and creative formatting.
   - For a **professional** project, keep it clean and formal.

3. **Additional Requirements**:
   - Always include this badge at the bottom:
[![Built with Dokugen](https://img.shields.io/badge/Built%20with-Dokugen-brightgreen)](https://github.com/samueltuoyo15/Dokugen)
   - The README must **sound human-written**. Avoid boilerplate phrases.
   - Do **not** wrap the README in markdown code block markers.

4. **Creativity & Engagement**:
   - Use tables, lists, code blocks, headings, and subheadings as needed.
   - Highlight unique selling points and include calls to action.

## Final Output:
Generate the README.md content directly, ready to use as-is.
"""

    system_message = {
        "role": "system",
        "content": (
            "You are a Goated professional README generator. Follow these rules strictly:\n"
            "1. Always include the Dokugen badge at the bottom using the exact format provided.\n"
            "2. Do not wrap the README content in markdown code blocks. Output the README.md content directly.\n"
            "3. Write in a human-like tone and ensure the README is professional, modern, and engaging."
        )
    }
    user_message = {"role": "user", "content": prompt}

    async def gemini_stream_generator():
        response = await client.models.generate_content_stream(
            model='gemini-2.0-flash',
            contents=[system_message, user_message],
        )
        async for chunk in response:
            delta = chunk.choices[0].delta
            text = delta.get("content", "")
            if text:
                yield f"data: {text}\n\n"

    return StreamingResponse(gemini_stream_generator(), media_type="text/event-stream")
