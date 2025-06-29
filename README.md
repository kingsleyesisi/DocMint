# DocMint CLI: Your Professional README Generator ✨

Hey there! 👋 DocMint CLI is your go-to command-line tool for generating professional README files without breaking a sweat. Whether you're on Windows, macOS, or Linux, this tool has got you covered. It dives deep into your project, figures out what it's all about, and whips up a comprehensive README.md file that'll make your project shine. ✨

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

- **Automated README Generation**: Say goodbye to README-writing headaches! DocMint CLI analyzes your project files and generates a detailed README in minutes. 🚀
- **Project Type Detection**: It's like magic! DocMint automatically detects your project type (Python, JavaScript, Java, you name it!). 🧙‍♀️
- **Customizable**: Need a README with a specific focus? Use custom prompts and project types to tailor the output. 🎨
- **Configuration**: Tweak the tool to fit your needs. Configure the backend URL, excluded directories, and more. ⚙️
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux. No compatibility nightmares! 💻
- **Contributing Guidelines**: Easily include or exclude a contributing section to encourage community involvement. 🤝
- **Network Check**: Always know if you're connected to the DocMint backend. 🌐
- **File Analysis**: Scans and processes project files, providing a summary of analyzed files. 🔍
- **Colorized Output**: Enjoy informative and visually appealing terminal output. Makes everything easier on the eyes! 🌈

## Technologies Used 🛠️

- **Python**: The heart and soul of DocMint CLI. 🐍
- **requests**: Making HTTP requests to the DocMint backend like a pro. 🌐
- **argparse**: Parsing command-line arguments so you can customize your experience. ⚙️
- **pathlib**: Handling file paths with grace and ease. 🗂️
- **mimetypes**: Determining file types to better understand your project. 📄
- **colorama**: Adding color support in Windows terminals. 🎨

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg?style=flat-square)](https://www.python.org/)
[![requests](https://img.shields.io/badge/requests-2.25.1-brightgreen.svg?style=flat-square)](https://docs.python-requests.org/en/master/)
[![argparse](https://img.shields.io/badge/argparse-blueviolet.svg?style=flat-square)](https://docs.python.org/3/library/argparse.html)

## Installation ⬇️

1. **Prerequisites**:
   - Python 3.6 or higher (because who doesn't love the latest features?).
   - `pip` package installer (your best friend for Python packages).

2. **Install DocMint CLI**:
   First, make sure you have `requests` installed:

   ```bash
   pip install requests
   ```

3. **Clone the Repository**:
   Grab the DocMint CLI repository from GitHub:

   ```bash
   git clone <repository_url>
   cd docmint_cli
   ```

4. **Install Dependencies**:
   (Optional, but highly recommended) Set up a virtual environment to keep your project dependencies tidy:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   pip install -r requirements.txt  # If you have a requirements.txt
   ```

## Usage 💻

### Basic Usage

To generate a README for your project in the current directory, just run:

```bash
python cli.py
```

### Specifying a Directory

Want to analyze a specific directory? Use the `-d` or `--directory` option:

```bash
python cli.py -d /path/to/your/project
```

### Using a Text Prompt

Generate a README from a text prompt with the `-p` or `--prompt` option:

```bash
python cli.py -p "My awesome project is a web application built with Flask and React."
```

### Specifying Project Type and Output File

Specify the project type and output file name using the `-t` or `--type` and `-o` or `--output` options:

```bash
python cli.py -t Python -o MyREADME.md
```

### Excluding Contributing Section

Skip the contributing section with the `--no-contributing` option:

```bash
python cli.py --no-contributing
```

### Using a Custom Backend URL

For those who like to tinker, use a custom backend URL with the `--url` option:

```bash
python cli.py --url http://localhost:8000
```

### Skipping the Banner

Skip the fancy banner display with the `--no-banner` option:

```bash
python cli.py --no-banner
```

## Configuration ⚙️

DocMint CLI uses a configuration file to store settings like the backend URL and excluded directories.

### Configuration File

The configuration file is located at `~/.docmint/config.json`.

### Default Configuration

Here’s what the default configuration looks like:

```json
{
    "backend_url": "https://docmint.onrender.com",
    "default_project_type": "auto",
    "include_contributing": true,
    "max_file_size": 104857600,
    "max_files": 150,
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
        ".conf",
        ".sh",
        ".bash",
        ".zsh",
        ".ps1",
        ".psm1",
        ".sql",
        ".pl",
        ".pyx",
        ".r",
        ".dart",
        ".lua",
        ".groovy",
        ".kotlin",
        ".h",
        ".hpp",
        ".cxx",
        ".m",
        ".t",
        ".swift",
        ".pl",
        ".pm"
    ]
}
```

### Modifying Configuration

Feel free to tweak the configuration file to your liking. For instance, to change the backend URL, just edit the `backend_url` field in the `config.json` file.

## API Documentation 📒

DocMint CLI interacts with a backend server to generate those awesome README files. Here’s a peek at the API endpoints it uses:

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

url = "https://docmint.onrender.com/api/generate-from-files/"
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

## Deployment 🚀

Deployment instructions can vary based on your project's specifics. Here are some general tips:

- **Web Applications**: Deploy to platforms like Netlify, Vercel, or AWS.
- **Python Packages**: Package your code and upload to PyPI.
- **Docker Containers**: Containerize your application using Docker and deploy to container orchestration platforms like Kubernetes.

## Contributing 🤝

We'd love for you to contribute to DocMint CLI! Here's how:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Write tests for your changes.
4.  Submit a pull request.

## License 📄

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments 🙏

- Thanks to all the contributors who've helped make DocMint CLI better.
- Special thanks to the open-source community for the awesome tools and libraries.

## Troubleshooting 💡

### Connection Issues

If you're having trouble connecting to the DocMint backend, check these:

- Verify your internet connection.
- Make sure the backend URL is correct.
- Confirm that the DocMint backend is up and running.

### File Encoding Errors

If you run into file encoding errors, try these:

- Ensure your files are encoded in UTF-8.
- Use the `--encoding` option to specify the file encoding.

### Large Project Issues

For performance issues with large projects:

- Exclude unnecessary directories and files from analysis.
- Increase the timeout value for API requests.

---

[![Built with DocMint](https://img.shields.io/badge/Generated%20by-DocMint-red)](https://github.com/kingsleyesisi/DocMint)