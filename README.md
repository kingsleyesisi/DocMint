<div align="center">

# 🌟 DocMint

### *Professional README & Documentation Generator*

[![PyPI version](https://badge.fury.io/py/docmint.svg)](https://badge.fury.io/py/docmint)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/docmint)](https://pepy.tech/project/docmint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

*Transform your projects into professionally documented masterpieces with AI-powered README generation* ✨

[🚀 **Quick Start**](#installation) • [📖 **Documentation**](#usage) • [🎯 **Features**](#features) • [🤝 **Contributing**](#contributing)

---

</div>

## 🎯 What is DocMint?

**DocMint** is a powerful Python package that automatically generates comprehensive, professional README files for your projects. Simply point it at your codebase, and watch as it analyzes your files, understands your project structure, and creates beautiful documentation that makes your project shine.

> 💡 **Perfect for developers who want professional documentation without the hassle!**

### ✨ Key Highlights

🔍 **Smart Analysis** - Automatically detects project type and structure  
🎨 **Beautiful Output** - Generates professional, well-formatted README files  
🌍 **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux  
⚡ **Lightning Fast** - Generate comprehensive docs in seconds  
🛠️ **Highly Configurable** - Customize output to match your needs  
🚫 **Smart Filtering** - Exclude unwanted files and directories with patterns

---

## 🚀 Installation

### Install from PyPI (Recommended)

```bash
pip install docmint
```

### Install from Source

```bash
git clone https://github.com/kingsleyesisi/docmint.git
cd docmint
pip install -e .
```

### Verify Installation

```bash
docmint --help
```

---

## 💻 Usage

### 🎯 Quick Start

Generate a README for your current project:

```bash
docmint
```

### 📁 Analyze Specific Directory

```bash
docmint -d /path/to/your/project
```

### 💬 Generate from Description

```bash
docmint -p "My awesome web application built with Flask and React"
```

### 🚫 Exclude Files and Directories

```bash
# Exclude specific directories
docmint --exclude-dir "temp,cache,logs"

# Exclude specific files (supports wildcards)
docmint --exclude-file "*.log,*.tmp,secret.txt"

# Exclude with patterns
docmint --exclude-file "tests/*,docs/*.md"

# Combine multiple exclusions
docmint --exclude-dir node_modules,dist --exclude-file "*.log,temp*"
```

### 🎨 Advanced Usage

```bash
# Specify project type and output file
docmint -t Python -o MyAwesome-README.md

# Skip contributing section
docmint --no-contributing

# Use custom backend
docmint --url http://localhost:8000

# Silent mode (no banner)
docmint --no-banner

# Show current configuration
docmint --show-config
```

---

## 🛠️ Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--directory` | `-d` | Project directory to analyze | `-d ./my-project` |
| `--prompt` | `-p` | Generate from text description | `-p "Flask API server"` |
| `--type` | `-t` | Specify project type | `-t Python` |
| `--output` | `-o` | Output filename | `-o DOCUMENTATION.md` |
| `--exclude-dir` | | Exclude directories (supports wildcards) | `--exclude-dir "temp*,cache"` |
| `--exclude-file` | | Exclude files (supports wildcards) | `--exclude-file "*.log,secret*"` |
| `--no-contributing` | | Skip contributing section | `--no-contributing` |
| `--url` | | Custom backend URL | `--url http://localhost:8000` |
| `--no-banner` | | Skip banner display | `--no-banner` |
| `--show-config` | | Show current configuration | `--show-config` |
| `--help` | `-h` | Show help message | `--help` |

---

## 🚫 Exclusion Patterns

DocMint provides powerful exclusion capabilities to filter out unwanted files and directories:

### 📁 Directory Exclusions

```bash
# Exclude specific directories
docmint --exclude-dir "node_modules,dist,build"

# Use wildcards
docmint --exclude-dir "temp*,cache*,*_backup"

# Multiple exclude-dir arguments
docmint --exclude-dir node_modules --exclude-dir dist --exclude-dir "temp*"
```

### 📄 File Exclusions

```bash
# Exclude specific files
docmint --exclude-file "secret.txt,config.local.json"

# Use wildcards for file patterns
docmint --exclude-file "*.log,*.tmp,*.cache"

# Exclude files in specific paths
docmint --exclude-file "tests/*,docs/*.md,src/temp*"
```

### 🔧 Default Exclusions

DocMint automatically excludes common directories and files:

**Default Excluded Directories:**
- `node_modules`, `.git`, `__pycache__`, `venv`, `dist`, `build`
- `.next`, `target`, `vendor`, `coverage`, `.vs`, `Pods`

**Default Excluded Files:**
- `*.log`, `*.tmp`, `*.cache`, `*.lock`, `*.pyc`
- `.DS_Store`, `Thumbs.db`, `*.swp`, `*.swo`

---

## 🎨 Features

<div align="center">

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Analysis** | Intelligent project understanding and documentation generation |
| 🔍 **Smart Detection** | Automatically identifies project type, dependencies, and structure |
| 📝 **Professional Templates** | Beautiful, industry-standard README formats |
| 🌈 **Colorful CLI** | Rich terminal output with progress indicators and status updates |
| ⚙️ **Configurable** | Extensive configuration options for customized output |
| 🚫 **Smart Filtering** | Advanced file and directory exclusion with wildcard support |
| 🔗 **API Integration** | Seamless integration with DocMint cloud services |
| 📊 **File Analysis** | Comprehensive project file scanning and summarization |
| 🛡️ **Error Handling** | Robust error handling with helpful diagnostic messages |

</div>

### 🎯 Supported Project Types

- 🐍 **Python** (Django, Flask, FastAPI, etc.)
- 🟨 **JavaScript/TypeScript** (Node.js, React, Vue, Angular)
- ☕ **Java** (Spring, Maven, Gradle)
- 🦀 **Rust** (Cargo projects)
- 🐹 **Go** (Go modules)
- 💎 **Ruby** (Rails, Gems)
- 🐘 **PHP** (Laravel, Composer)
- ⚡ **C/C++** (CMake, Make)
- 🔷 **C#/.NET** (MSBuild projects)
- 🍃 **Swift** (Xcode projects)
- 🎯 **Kotlin** (Android, JVM)
- 🌐 **Web Development** (HTML, CSS, JavaScript)

---

## ⚙️ Configuration

DocMint uses a configuration file located at `~/.docmint/config.json` for persistent settings.

### 📋 Default Configuration

```json
{
    "backend_url": "https://docmint.onrender.com",
    "default_project_type": "auto",
    "include_contributing": true,
    "max_file_size": 104857600,
    "max_files": 150,
    "excluded_dirs": [
        "node_modules", ".git", "__pycache__", 
        "venv", "dist", "build", ".next",
        "coverage", ".vs", "Pods"
    ],
    "excluded_files": [
        "*.log", "*.tmp", "*.cache", "*.lock",
        ".DS_Store", "Thumbs.db", "*.pyc"
    ],
    "supported_extensions": [
        ".py", ".js", ".ts", ".jsx", ".tsx", 
        ".java", ".cpp", ".go", ".rs", ".php"
    ]
}
```

### 🔧 Customization

Edit the configuration file to customize DocMint's behavior:

```bash
# View current configuration
docmint --show-config

# Open configuration file for editing
nano ~/.docmint/config.json
```

### 📝 Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `backend_url` | string | API endpoint URL |
| `max_file_size` | integer | Maximum file size in bytes |
| `max_files` | integer | Maximum number of files to analyze |
| `excluded_dirs` | array | Default directories to exclude |
| `excluded_files` | array | Default file patterns to exclude |
| `supported_extensions` | array | File extensions to include |

---

## 🌐 API Integration

DocMint integrates with cloud services for enhanced README generation:

### 🔗 Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health/` | GET | Health check |
| `/api/generate/` | POST | Generate from prompt |
| `/api/generate-from-files/` | POST | Generate from files |

### 📡 Example API Usage

```python
import requests

# Generate README from prompt
response = requests.post(
    "https://docmint.onrender.com/api/generate/",
    json={"message": "Python web scraping tool"}
)

readme_content = response.json()["answer"]
```

---

## 🚀 Development

### 🛠️ Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/kingsleyesisi/docmint.git
cd docmint

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .
pip install -r requirements.txt
```

### 🧪 Running Tests

```bash
# Run tests (when available)
python -m pytest

# Run with coverage
python -m pytest --cov=docmint
```

### 📦 Building Package

```bash
# Build distribution packages
python -m build

# Upload to PyPI (maintainers only)
python -m twine upload dist/*
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help make DocMint even better:

### 🎯 Ways to Contribute

- 🐛 **Report Bugs** - Found an issue? Let us know!
- 💡 **Suggest Features** - Have ideas for improvements?
- 📝 **Improve Documentation** - Help make our docs clearer
- 🔧 **Submit Code** - Fix bugs or add new features

### 📋 Contribution Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 📜 Code Style

We use [Black](https://github.com/psf/black) for code formatting:

```bash
# Format code
black docmint/

# Check formatting
black --check docmint/
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

<details>
<summary><strong>🔌 Connection Issues</strong></summary>

**Problem**: Cannot connect to DocMint backend

**Solutions**:
- ✅ Check your internet connection
- ✅ Verify backend URL in configuration
- ✅ Try using `--url` flag with alternative endpoint
- ✅ Check firewall settings

</details>

<details>
<summary><strong>📁 File Encoding Errors</strong></summary>

**Problem**: Encoding errors when reading files

**Solutions**:
- ✅ Ensure files are UTF-8 encoded
- ✅ Check for binary files in project directory
- ✅ Add problematic files to exclusion list with `--exclude-file`

</details>

<details>
<summary><strong>⚡ Performance Issues</strong></summary>

**Problem**: Slow processing for large projects

**Solutions**:
- ✅ Use `--exclude-dir` to exclude large directories
- ✅ Use `--exclude-file` to exclude unnecessary files
- ✅ Reduce max_files in configuration
- ✅ Use specific directory targeting with `-d`

</details>

<details>
<summary><strong>🚫 Too Many Files Excluded</strong></summary>

**Problem**: Important files being excluded

**Solutions**:
- ✅ Check your exclusion patterns with `--show-config`
- ✅ Use more specific patterns instead of broad wildcards
- ✅ Review default exclusions in configuration file
- ✅ Test patterns with smaller directories first

</details>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- 🌟 **Contributors** - Thank you to all who have contributed to this project
- 🛠️ **Open Source Community** - For the amazing tools and libraries
- 🤖 **AI Technology** - Powering intelligent documentation generation

---

<div align="center">

### 🌟 Star us on GitHub!

If DocMint helped you create better documentation, please consider giving us a star ⭐

[![GitHub stars](https://img.shields.io/github/stars/kingsleyesisi/docmint.svg?style=social&label=Star)](https://github.com/kingsleyesisi/docmint)

---

**Made with ❤️ by the DocMint Team**

[![Built with DocMint](https://img.shields.io/badge/Generated%20by-DocMint-red?style=flat-square)](https://github.com/kingsleyesisi/docmint)

</div>