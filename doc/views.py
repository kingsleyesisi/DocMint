from django.shortcuts import render
from rest_framework import viewsets
from google import genai
import asyncio
from dotenv import load_dotenv
from rest_framework.response import Response

env = load_dotenv()

client = genai.Client(api_key="AIzaSyAkXyGaJGcBM8mWjzsRiHcv2xTUUtiauvI")

def generate_readme(content):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
    answer = response.text
    print(answer)
    return {"answer": answer}

def get(requst):

    ans = generate_readme("what is the current time")
    print(ans)

    return Response({"answer": ans})
