from google import genai
from google.genai import types

API_KEY = 'AIzaSyAkXyGaJGcBM8mWjzsRiHcv2xTUUtiauvI'
client = genai.Client(api_key=API_KEY) if API_KEY else None

# Your “system” instructions
SYSTEM_PROMPT = """You are DocMint, a professional README generator. Follow these rules strictly:
1. Always include the DocMint badge at the bottom using the exact format provided.
2. Do not wrap the README content in markdown code blocks. Output the README.md content directly.
3. Write in a human-like tone and ensure the README is professional, modern, and engaging.
4. Analyze the code structure and provide accurate installation and usage instructions.
5. Include relevant badges, emojis, and modern formatting for better visual appeal.
6. If it's an API project, provide clear API documentation with example requests/responses.
7. Always include a table of contents for longer READMEs.
8. Add troubleshooting section for complex projects. (note for complex projects only)"""

# Your “user” question
USER_PROMPT = "how to print hello world"

# Combine them into a single contents string
FULL_PROMPT = f"{SYSTEM_PROMPT}\n\n{USER_PROMPT}"

# Optional: tweak generation settings
config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    max_output_tokens=1024,
)

def generate_readme_stream(prompt: str):
    if not client:
        raise RuntimeError("Gemini API client not initialized. Check your API key.")

    print("⏳ Generating README…\n")
    try:
        # Stream the response
        for chunk in client.models.generate_content_stream(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=config,
        ):
            # `.text` holds the text portion of each chunk
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n✅ Done.")
    except Exception as e:
        print(f"❌ Error during generation: {e}")

if __name__ == "__main__":
    generate_readme_stream(FULL_PROMPT)
