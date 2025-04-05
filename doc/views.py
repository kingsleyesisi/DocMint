from django.shortcuts import render
from rest_framework import viewsets
from google import genai
import asyncio
from dotenv import load_dotenv
from rest_framework.response import Response
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

API_KEY = getattr(settings, 'GEMINI_API', None)
client = genai.Client(api_key=API_KEY)


system_message = {
    "role": "system",
    "content": (
        "You are a professional README generator. Follow these rules strictly:\n"
        "1. Always include the DocMint badge at the bottom using the exact format provided.\n"
        "2. Do not wrap the README content in markdown code blocks. Output the README.md content directly.\n"
        "3. Write in a human-like tone and ensure the README is professional, modern, and engaging."
    )
}

def generate_readme(content):
    user_message = {"role": "user", "content": content}

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=[json.dumps(system_message), json.dumps(user_message)]
        )
        answer = response.text
        print(answer)
        return {"answer": answer}
    except Exception as e:
        print(f"Error generating README: {e}")
        return {"error": str(e)}

@csrf_exempt
def index(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("message", "").strip()
            print(prompt)
            if not prompt:
                return JsonResponse({"error": "Prompt is required"}, status=400)
            
            result = generate_readme(prompt)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)


@csrf_exempt
def generate_from_files(request):
    if request.method == "POST":
        try:
            if 'files' not in request.FILES:
                return JsonResponse({"error": "Files are required"}, status=400)
            
            files = request.FILES.getlist('files')
            if not files:
                return JsonResponse({"error": "No files provided"}, status=400)
            
            project_type = request.POST.get('projectType', '').strip()
            if not project_type:
                return JsonResponse({"error": "Project type is required"}, status=400)
            
            project_summary = f"Project Summary:\nThis is a {project_type}.\n"
            combined_content = ""
            file_details = []

            for file in files:
                file_name = file.name
                file_extension = os.path.splitext(file_name)[1]
                content = file.read().decode('utf-8')
                
                if not content.strip():
                    return JsonResponse({"error": f"File {file_name} content is empty"}, status=400)
                
                combined_content += content + "\n"  # Combine all file contents
                file_details.append(f"File: {file_name}, Type: {file_extension}")
            
            project_summary += "Files included:\n" + "\n".join(file_details) + "\n\n"
            
            # Generate documentation for the combined content



            prompt = f"""
            Generate a **high-quality, professional, and modern README.md** for a **{project_type}** project.

            ## Project Overview:
            The project includes the following files:
            {chr(10).join(file_details)}

            ## Full Code Context:
            Below is the actual source code:
            {combined_content}

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
            [![Built with DocMint](https://img.shields.io/badge/Generated%20by-DocMint-red)](https://github.com/kingsleyesisi/DocMint)
            - The README must **sound human-written**. Avoid boilerplate phrases.
            - Do **not** wrap the README in markdown code block markers.

            4. **Creativity & Engagement**:
            - Use tables, lists, code blocks, headings, and subheadings as needed.
            - Highlight unique selling points and include calls to action.

            ## Final Output:
            Generate the README.md content directly, ready to use as-is.
            """
                # documentation_prompt = (
                #     f"{project_summary}Generate a detailed documentation for the project "
                #     f"including how it works and, if applicable, how to use its API."
            # )
            result = generate_readme(prompt)
            
            return JsonResponse({"result": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)
