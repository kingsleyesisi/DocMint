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

def generate_readme(content):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
    answer = response.text
    print(answer)
    return {"answer": answer}

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
def generate_from_file(request):
    if request.method == "POST":
        try:
            if 'file' not in request.FILES:
                return JsonResponse({"error": "File is required"}, status=400)
            
            file = request.FILES['file']
            content = file.read().decode('utf-8')
            
            if not content.strip():
                return JsonResponse({"error": "File content is empty"}, status=400)
            
            result = generate_readme(content)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)