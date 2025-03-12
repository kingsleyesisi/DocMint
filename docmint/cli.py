#!/usr/bin/env python
import os
import subprocess
import getpass
import json
import click
import rich
from rich.console import Console
from rich.prompt import Confirm
from rich.progress import Progress

console = Console()

def get_user_info():
    try:
        git_name = subprocess.check_output(
            ["git", "config", "--get", "user.name"], text=True
        ).strip()
        git_email = subprocess.check_output(
            ["git", "config", "--get", "user.email"], text=True
        ).strip()
        if git_name and git_email:
            return {"username": git_name, "email": git_email}
    except subprocess.CalledProcessError:
        pass

    return {"username": getpass.getuser(), "email": os.getenv("USER", "Unknown")}

def extract_full_code(project_files, project_dir):
    snippets = []
    for file in project_files:
        if file.endswith(('.py', '.js', '.json', '.html', '.go', '.ejs', '.mjs', '.rs', '.c', '.cs', '.cpp', '.h', '.hpp', '.java', '.kt', '.swift', '.php', '.rb', '.dart', '.scala', '.lua', '.sh', '.bat', '.asm', '.vb', '.cshtml', '.razor', '.m')):
            try:
                with open(os.path.join(project_dir, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                snippets.append(f"## {file}\n```{os.path.splitext(file)[1][1:]}\n{content}\n```\n")
            except Exception as e:
                console.print(f"[red]Error reading {file}: {e}[/red]")
    return ''.join(snippets) if snippets else "No code snippets available"

def detect_project_type(project_dir):
    files = os.listdir(project_dir)

    lang_map = {
        "vite.config.ts": "React/Typescript (Vite + React)",
        "vite.config.js": "React/JavaScript (Vite + React)",
        "next.config.ts": "Next.js (Typescript)",
        "next.config.js": "Next.js (JavaScript)",
        "nuxt.config.ts": "Nuxt.js (Typescript)",
        "nuxt.config.js": "Nuxt.js (JavaScript)",
        "svelte.config.js": "Svelte",
        "angular.json": "Angular",
        "vue.config.js": "Vue.js",
        "src/main.tsx": "React/Typescript",
        "src/main.jsx": "React/JavaScript",
        "src/App.vue": "Vue.js",
        "src/main.svelte": "Svelte",
        "src/main.ts": "Typescript",
        "src/main.js": "JavaScript",
        "go.mod": "Golang",
        "Cargo.toml": "Rust",
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java (Gradle)",
        "composer.json": "PHP",
        "Gemfile": "Ruby",
        "package.json": "Node.js",
        "pubspec.yaml": "Flutter/Dart",
        "android/build.gradle": "Android (Kotlin/Java)",
        "ios/Podfile": "iOS (Swift/Objective-C)",
        "Dockerfile": "Docker",
        "docker-compose.yml": "Docker Compose",
        "terraform.tf": "Terraform",
        "serverless.yml": "Serverless Framework",
        "k8s/deployment.yaml": "Kubernetes",
        "Makefile": "C/C++",
        "CMakeLists.txt": "C++",
        "Program.cs": "C# / .NET",
        "Main.kt": "Kotlin",
        "App.swift": "Swift",
    }

    folder_checks = {
        "src/components": "React/Typescript or React/JavaScript",
        "src/views": "Vue.js",
        "src/routes": "Svelte",
        "src/app": "Angular",
        "src/lib": "Svelte",
        "src/pages": "Next.js or Nuxt.js",
        "public": "Static Site (HTML/CSS/JS)",
        "dist": "Built Project",
    }

    def check_package_json():
        package_json_path = os.path.join(project_dir, "package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_json = json.load(f)
            dependencies = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}
            if "react" in dependencies:
                return "React/JavaScript"
            if "vue" in dependencies:
                return "Vue.js"
            if "svelte" in dependencies:
                return "Svelte"
            if "@angular/core" in dependencies:
                return "Angular"
            if "next" in dependencies:
                return "Next.js"
            if "nuxt" in dependencies:
                return "Nuxt.js"
        return None

    detected_file = next((lang_map[file] for file in files if file in lang_map), None)
    if detected_file:
        return detected_file

    detected_folder = next((folder_checks[folder] for folder in folder_checks if os.path.exists(os.path.join(project_dir, folder))), None)
    if detected_folder:
        return detected_folder

    package_json_detection = check_package_json()
    if package_json_detection:
        return package_json_detection

    return "Unknown"

def scan_files(dir):
    ignore_dirs = {"node_modules", "dist", ".git", ".next", "coverage", "out", "test", "uploads", "docs", "build", ".vscode", ".idea", "logs", "public", "storage", "bin", "obj", "lib", "venv", "cmake-build-debug"}
    ignore_files = {"CHANGELOG.md", "style.css", "main.css", "output.css", ".gitignore", ".npmignore", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "tsconfig.json", "jest.config.js", "README.md", ".DS_Store", ".env", "Thumbs.db", "tsconfig.*", "*.iml", ".editorconfig", ".prettierrc*", ".eslintrc*"}

    files = []
    queue = [dir]

    while queue:
        folder = queue.pop(0)
        try
::contentReference[oaicite:1]{index=1}
 
