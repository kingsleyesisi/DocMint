# DocMint: Your Professional README Generator 🚀

## Table of Contents
1.  [Overview](#overview)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Installation](#installation)
5.  [Usage](#usage)
6.  [API Documentation](#api-documentation)
7.  [Deployment](#deployment)
8.  [Contributing](#contributing)
9.  [License](#license)
10. [Acknowledgments](#acknowledgments)
11. [Troubleshooting](#troubleshooting)

## Overview

DocMint is a powerful tool designed to automatically generate high-quality, professional README files for your projects. This project leverages the Gemini AI model to analyze your code and create comprehensive documentation, saving you time and ensuring your projects are well-documented. Whether you're working on a small script or a large-scale application, DocMint can help you create a README that effectively communicates your project's purpose, usage, and more.

## Features
*   **Automatic README Generation**: Generates README.md files from project files using AI. 🤖
*   **Customizable**: Supports different project types (e.g., Python, JavaScript, API). 🛠️
*   **API Endpoints**:
    *   Generate from text prompt. 📝
    *   Generate from uploaded files. 📂
    *   Health check. 🩺
    *   Supported formats. 🗂️
    *   Project validation. ✅
*   **Multi-File Support**: Handles projects with multiple files. 📚
*   **Project Analysis**: Analyzes the project structure to provide insights into the number of files, languages used, and more. 📊
*   **API Documentation**: Generates API documentation, including endpoints and request/response examples. ⚙️

## Technologies Used
*   Python 🐍
*   Django 🌐
*   FastAPI 🚀
*   Google Gemini AI 🧠
*   dotenv 🔑

## Installation

Follow these steps to set up DocMint locally:

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]
    cd [docmint_directory]
    ```

2.  **Set up a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    *   Create a `.env` file in the project root.
    *   Add your Gemini API key:

        ```
        GEMINI_API=YOUR_GEMINI_API_KEY
        ```

5.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

## Usage
1.  **Run the Django development server:**

    ```bash
    python manage.py runserver
    ```

2.  **Access the API endpoints:**
    *   Health check: `http://127.0.0.1:8000/api/health/`
    *   Generate from prompt: `http://127.0.0.1:8000/api/generate/`
    *   Generate from files: `http://127.0.0.1:8000/api/generate-from-files/`
    *   Supported formats: `http://127.0.0.1:8000/api/formats/`
    *   Validate project: `http://127.0.0.1:8000/api/validate/`

3.  **Using the `try.py` script for testing:**
    *   Ensure the Django development server is running.
    *   Run the script:
        ```bash
        python try.py
        ```
    *   This script sends POST requests to the `/generate` endpoint for each file in the current directory.

## API Documentation

### 1. Health Check
*   **Endpoint**: `/api/health/`
*   **Method**: `GET`
*   **Description**: Checks the health status of the DocMint service and its connection to the Gemini API.
*   **Response**:
    ```json
    {
        "status": "healthy",
        "service": "DocMint README Generator",
        "version": "2.0.0",
        "gemini_api": "connected",
        "supported_formats": [
            "Text prompt",
            "File upload",
            "Multi-file projects"
        ]
    }
    ```

### 2. Generate from Prompt
*   **Endpoint**: `/api/generate/`
*   **Method**: `POST`
*   **Description**: Generates a README.md file based on a provided text prompt.
*   **Request Body**:
    ```json
    {
        "message": "Describe your project: 'A Python web scraper that extracts data from e-commerce sites'"
    }
    ```
*   **Response**:
    ```json
    {
        "answer": "# Web Scraper Project\n\n## Overview\nA Python web scraper that extracts data from e-commerce sites.\n\n## Features\n- Scrapes product information\n- Extracts prices\n- Saves data to a CSV file\n\n## Installation\n```bash\npip install requests beautifulsoup4\n```\n\n## Usage\n```python\nimport scraper\nscraper.run()\n```"
    }
    ```

### 3. Generate from Files
*   **Endpoint**: `/api/generate-from-files/`
*   **Method**: `POST`
*   **Description**: Generates a README.md file based on uploaded project files.
*   **Request Body (multipart/form-data)**:
    *   `files`: List of files to be processed.
    *   `projectType`: Type of the project (e.g., Python, JavaScript).
    *   `contribution`: Boolean to include contribution guidelines (default: true).
    *   `includeApiDocs`: Boolean to include API documentation (default: false).
    *   `includeDeployment`: Boolean to include deployment instructions (default: true).
*   **Example Request (using `requests` library)**:
    ```python
    import requests
    
    url = 'http://127.0.0.1:8000/api/generate-from-files/'
    files = {
        'files': [
            ('file1.py', open('file1.py', 'rb')),
            ('file2.py', open('file2.py', 'rb'))
        ]
    }
    data = {
        'projectType': 'Python',
        'contribution': 'true',
        'includeApiDocs': 'false',
        'includeDeployment': 'true'
    }
    response = requests.post(url, files=files, data=data)
    print(response.json())
    ```
*   **Response**:
    ```json
    {
        "result": {
            "answer": "Your generated README content here..."
        },
        "metadata": {
            "files_processed": 2,
            "total_lines": 200,
            "primary_languages": ["python"],
            "project_type": "Python",
            "generated_at": null
        }
    }
    ```

### 4. Supported Formats
*   **Endpoint**: `/api/formats/`
*   **Method**: `GET`
*   **Description**: Retrieves a list of supported file formats and project types.
*   **Response**:
    ```json
    {
        "supported_file_extensions": [".py", ".js", ...],
        "supported_project_types": ["Python", "JavaScript", ...],
        "max_file_size_mb": 10,
        "max_files_per_request": 20
    }
    ```

### 5. Validate Project
*   **Endpoint**: `/api/validate/`
*   **Method**: `POST`
*   **Description**: Validates the project structure and provides recommendations.
*   **Request Body**:
    ```json
    {
        "files": [
            {"name": "file1.py", "content": "..."}
        ],
        "projectType": "Python"
    }
    ```
*   **Response**:
    ```json
    {
        "valid": true,
        "recommendations": ["Consider adding requirements.txt"],
        "warnings": [],
        "file_count": 1,
        "estimated_readme_sections": 9
    }
    ```

## Deployment
1.  **Configure a production environment:**
    *   Set up a production-ready WSGI server (e.g., Gunicorn, uWSGI).
    *   Configure a reverse proxy (e.g., Nginx, Apache).
2.  **Set environment variables:**
    *   Ensure `GEMINI_API` is set in your production environment.
    *   Set `DEBUG = False` in `settings.py`.
3.  **Collect static files:**

    ```bash
    python manage.py collectstatic
    ```

4.  **Serve static files via the reverse proxy.**
5.  **Deploy the application:**
    *   Deploy the Django application to your production server.
    *   Ensure the server is accessible via the configured domain.

## Contributing
Contributions are welcome! Here's how you can contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Write tests for your changes.
5.  Submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
*   Powered by the Google Gemini AI model.
*   Built with Django and FastAPI.
*   Special thanks to all contributors.

## Troubleshooting

If you encounter issues while using DocMint, here are some common problems and solutions:

1.  **Gemini API Key Issues:**
    *   **Problem**: The Gemini API client is not initialized.
    *   **Solution**: Ensure you have set the `GEMINI_API` environment variable with a valid API key. Restart the Django server after setting the API key.

2.  **Installation Problems:**
    *   **Problem**: Dependency installation fails.
    *   **Solution**: Ensure you have Python 3.7+ installed and that your pip version is up to date. Try running `pip install --upgrade pip` and then `pip install -r requirements.txt`.

3.  **API Endpoint Errors:**
    *   **Problem**: Receiving 400 Bad Request errors.
    *   **Solution**: Check your request body for missing or invalid fields. Refer to the API documentation for the correct request format.

4.  **File Processing Issues:**
    *   **Problem**: Files are not being processed.
    *   **Solution**: Ensure that the files you are uploading have supported extensions and are not larger than 1MB per file. Check the server logs for any file processing errors.

5.  **Empty README Generation:**
    *   **Problem**: The generated README is empty.
    *   **Solution**: Try providing a more detailed and specific prompt. Ensure that the Gemini API is functioning correctly and that there are no errors in the server logs.

[![Built with DocMint](https://img.shields.io/badge/Generated%20by-DocMint-red)](https://github.com/kingsleyesisi/DocMint)