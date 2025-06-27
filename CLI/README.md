# DocMint CLI: Your Professional README Generator 🚀

<p align="center">
  <img src="https://raw.githubusercontent.com/kingsleyesisi/DocMint/main/assets/docmint_logo.png" alt="DocMint CLI Logo" width="200"/>
</p>

DocMint CLI is a command-line tool designed to effortlessly generate professional README files for your projects. Compatible across Windows, macOS, and Linux, DocMint CLI analyzes your project and crafts a comprehensive README, saving you time and ensuring your projects are well-documented.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Troubleshooting](#troubleshooting)

## Features ✨

- **Automated README Generation**: Analyzes your project files and generates a detailed README.
- **Project Type Detection**: Automatically detects the project type (Python, JavaScript, Java, etc.).
- **Customizable**: Supports custom prompts and project types.
- **Configuration**: Allows configuration of backend URL, excluded directories, and more.
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux.
- **Contributing Guidelines**: Option to include or exclude a contributing section.
- **Network Check**: Verifies connectivity to the DocMint backend.
- **File Analysis**: Scans and processes project files, providing a summary of analyzed files.
- **Colorized Output**: Provides informative and visually appealing terminal output.

## Technologies Used 🛠️

- **Python**: Primary language.
- **requests**: For making HTTP requests to the DocMint backend.
- **argparse**: For command-line argument parsing.
- **pathlib**: For working with file paths.
- **mimetypes**: For determining file types.
- **colorama**: For color support in Windows terminals.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg?style=flat-square)](https://www.python.org/)
[![requests](https://img.shields.io/badge/requests-2.25.1-brightgreen.svg?style=flat-square)](https://docs.python-requests.org/en/master/)
[![argparse](https://img.shields.io/badge/argparse-blueviolet.svg?style=flat-square)](https://docs.python.org/3/library/argparse.html)

## Installation ⬇️

1. **Prerequisites**:
   - Python 3.6 or higher.
   - `pip` package installer.

2. **Install DocMint CLI**:
   ```bash
   pip install requests
   ```

3. **Clone the Repository**:
   Clone the DocMint CLI repository from GitHub:

   ```bash
   git clone <repository_url>
   cd docmint_cli
   ```

4. **Install Dependencies**:\
   Optionally, set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt # if you have a requirements.txt
   ```

## Usage 💻

### Basic Usage

To generate a README for your project in the current directory, simply run:

```bash
python cli.py
```

### Specifying a Directory

To analyze a specific directory, use the `-d` or `--directory` option:

```bash
python cli.py -d /path/to/your/project
```

### Using a Text Prompt

To generate a README from a text prompt, use the `-p` or `--prompt` option:

```bash
python cli.py -p "My awesome project is a web application built with Flask and React."
```

### Specifying Project Type and Output File

To specify the project type and output file name, use the `-t` or `--type` and `-o` or `--output` options:

```bash
python cli.py -t Python -o MyREADME.md
```

### Excluding Contributing Section

To skip the contributing section, use the `--no-contributing` option:

```bash
python cli.py --no-contributing
```

### Using a Custom Backend URL

To use a custom backend URL, use the `--url` option:

```bash
python cli.py --url http://localhost:8000
```

### Skipping the Banner

To skip the banner display, use the `--no-banner` option:

```bash
python cli.py --no-banner
```

## Configuration ⚙️

The DocMint CLI uses a configuration file to store settings such as the backend URL, excluded directories, and more.

### Configuration File

The configuration file is located at `~/.docmint/config.json`.

### Default Configuration

The default configuration is as follows:

```json
{
    "backend_url": "https://your-django-backend.com",
    "default_project_type": "auto",
    "include_contributing": true,
    "max_file_size": 1048576,
    "max_files": 20,
    "excluded_dirs": [
        "node_modules",
        ".git",
        "__pycache__",
        ".pytest_cache",
        "venv",
        "env",
        ".env",
        "dist",
        "build",
        ".next",
        "target",
        "bin",
        "obj",
        ".gradle",
        "vendor"
    ],
    "supported_extensions": [
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".php",
        ".rb",
        ".go",
        ".rs",
        ".swift",
        ".kt",
        ".scala",
        ".html",
        ".css",
        ".scss",
        ".sass",
        ".less",
        ".vue",
        ".svelte",
        ".md",
        ".txt",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".cfg",
        ".conf"
    ]
}
```

### Modifying Configuration

You can modify the configuration file to suit your needs. For example, to change the backend URL, edit the `backend_url` field in the `config.json` file.

## API Documentation 📖

The DocMint CLI interacts with a backend server to generate README files. Below are the API endpoints used by the CLI:

### Health Check

- **Endpoint**: `/api/health/`
- **Method**: `GET`
- **Description**: Checks if the backend server is reachable.
- **Response**:
  - Status Code: `200 OK` if the backend is healthy.

### Generate README from Prompt

- **Endpoint**: `/api/generate/`
- **Method**: `POST`
- **Description**: Generates a README file based on a text prompt.
- **Request Body**:

```json
{
  "message": "Your project description here"
}
```

- **Response**:

```json
{
  "answer": "# Your Generated README Content Here"
}
```

### Generate README from Files

- **Endpoint**: `/api/generate-from-files/`
- **Method**: `POST`
- **Description**: Generates a README file based on the project files.
- **Request Body**:
  - `files`: List of project files.
  - `projectType`: Type of the project (e.g., "Python", "JavaScript").
  - `contribution`: Boolean indicating whether to include a contributing section.

- **Example Request (using `requests` library)**:

```python
import requests

url = "https://your-django-backend.com/api/generate-from-files/"
files = [
    ('files', ('file1.py', open('file1.py', 'rb'), 'text/plain')),
    ('files', ('file2.js', open('file2.js', 'rb'), 'text/javascript'))
]
data = {
    'projectType': 'Python',
    'contribution': 'true'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

- **Response**:

```json
{
  "result": {
    "answer": "# Your Generated README Content Here"
  }
}
```

## Deployment 📦

Deployment instructions will vary depending on the nature of your project. Here are some general guidelines:

- **Web Applications**: Deploy to platforms like Netlify, Vercel, or AWS.
- **Python Packages**: Package your code and upload to PyPI.
- **Docker Containers**: Containerize your application using Docker and deploy to container orchestration platforms like Kubernetes.

## Contributing 🤝

We welcome contributions to DocMint CLI! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Write tests for your changes.
4.  Submit a pull request.

## License 📄

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments 🙏

- Thanks to the contributors who have helped improve DocMint CLI.
- Special thanks to the open-source community for providing valuable tools and libraries.

## Troubleshooting 💡

### Connection Issues

If you encounter connection issues with the DocMint backend, check the following:

- Verify your internet connection.
- Ensure the backend URL is correct.
- Confirm that the DocMint backend is running.

### File Encoding Errors

If you encounter errors related to file encoding, try the following:

- Ensure your files are encoded in UTF-8.
- Use the `--encoding` option to specify the file encoding.

### Large Project Issues

If you are working with a large project and encounter performance issues, try the following:

- Exclude unnecessary directories and files from analysis.
- Increase the timeout value for API requests.

---

[![Built with DocMint](https://img.shields.io/badge/Generated%20by-DocMint-red)](https://github.com/kingsleyesisi/DocMint)