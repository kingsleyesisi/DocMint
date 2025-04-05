import os
import requests

# filepath: /home/kingsleyesisi/projects/docmint.worktrees/docmintBack/doc/test_try.py

def test_generate_endpoint():
    url = "http://127.0.0.1:8000/generate"
    results = []

    # Read all files in the current directory
    for filename in os.listdir("."):
        if os.path.isfile(filename):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
                if content.strip():
                    # Send POST request to the endpoint
                    try:
                        response = requests.post(url, files={"files": (filename, content)})
                        response_data = response.json() if response.headers.get('Content-Type') == 'application/json' else {"error": "Invalid JSON response"}
                        results.append({
                            "files": filename,
                            "status_code": response.status_code,
                            "response": response_data
                        })
                    except requests.exceptions.RequestException as e:
                        results.append({
                            "files": filename,
                            "status_code": "Request Failed",
                            "response": str(e)
                        })
                    except ValueError as e:
                        results.append({
                            "file": filename,
                            "status_code": response.status_code,
                            "response": f"JSON decode error: {str(e)}"
                        })

    # Print results for debugging
    for result in results:
        print(f"File: {result['files']}")
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {result['response']}")
        print("-" * 40)

if __name__ == "__main__":
    print("Testing generate endpoint")
    print(test_generate_endpoint())
    print("Done")