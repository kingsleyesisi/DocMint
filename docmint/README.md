<div align="center">

# 🌟 DocMint Package

### *Core Python Package for Professional Documentation Generation*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

*The heart of DocMint - A powerful Python package for automated README generation* ✨

---

</div>

## 📦 Package Overview

This directory contains the core **DocMint** Python package that powers the command-line interface and provides the main functionality for generating professional README files.

## 🏗️ Package Structure

```
docmint/
├── __init__.py          # Package initialization and metadata
├── cli.py              # Command-line interface implementation
├── config.py           # Configuration management
└── README.md           # This file
```

## 🔧 Core Components

### 📋 `__init__.py`
- Package metadata and version information
- Main package exports and initialization
- Author and contact information

### 🖥️ `cli.py`
- Complete command-line interface implementation
- Cross-platform terminal support with colorized output
- Network connectivity and API integration
- File analysis and project type detection
- README generation from files or prompts

### ⚙️ `config.py`
- Configuration file management
- Default settings and user customization
- Supported file extensions and exclusion patterns
- Backend URL and API settings

## 🎯 Key Features

### 🤖 Intelligent Analysis
- **Project Type Detection**: Automatically identifies project type from files
- **File Scanning**: Recursively scans project directories
- **Smart Filtering**: Excludes unnecessary files and directories
- **Content Analysis**: Reads and processes supported file types

### 🎨 Professional Output
- **Markdown Generation**: Creates well-formatted README files
- **Template System**: Uses professional documentation templates
- **Customizable Sections**: Include/exclude contributing guidelines
- **Rich Formatting**: Proper headings, lists, and code blocks

### 🌐 API Integration
- **Cloud Backend**: Connects to DocMint cloud services
- **Health Checks**: Verifies backend connectivity
- **File Upload**: Sends project files for analysis
- **Prompt Processing**: Generates documentation from text descriptions

### 💻 Cross-Platform Support
- **Windows Compatibility**: Full Windows terminal support
- **macOS Support**: Native macOS terminal integration
- **Linux Support**: Complete Linux compatibility
- **Color Support**: Colorized output with fallbacks

## 🛠️ Technical Implementation

### 📊 Supported File Types
```python
SUPPORTED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx',      # Web & Python
    '.java', '.cpp', '.c', '.cs',             # Compiled languages
    '.php', '.rb', '.go', '.rs',              # Server languages
    '.swift', '.kt', '.scala',                # Mobile & JVM
    '.html', '.css', '.scss', '.vue',         # Frontend
    '.md', '.txt', '.json', '.yaml'           # Documentation & Config
}
```

### 🚫 Excluded Directories
```python
EXCLUDED_DIRS = [
    'node_modules', '.git', '__pycache__',
    'venv', 'env', 'dist', 'build',
    '.next', 'target', 'vendor'
]
```

### 🎨 Color System
- **Success**: Green indicators for completed operations
- **Error**: Red indicators for failures and issues
- **Warning**: Yellow indicators for cautions
- **Info**: Blue indicators for information
- **Progress**: Magenta indicators for ongoing operations

## 🔗 API Endpoints

### Health Check
```
GET /api/health/
```
Verifies backend service availability.

### Generate from Prompt
```
POST /api/generate/
Content-Type: application/json

{
    "message": "Project description"
}
```

### Generate from Files
```
POST /api/generate-from-files/
Content-Type: multipart/form-data

files: [project files]
projectType: string
contribution: boolean
```

## 🚀 Usage Examples

### Basic CLI Usage
```bash
# Install the package
pip install docmint

# Generate README for current directory
docmint

# Analyze specific directory
docmint -d /path/to/project

# Generate from description
docmint -p "Python web scraping tool"
```

### Programmatic Usage
```python
from docmint.cli import DocMintCLI

# Initialize CLI
cli = DocMintCLI()

# Generate from prompt
readme = cli.generate_readme_from_prompt("My awesome project")

# Save to file
cli.save_readme(readme, "README.md")
```

## 🔧 Configuration

### Default Configuration Location
```
~/.docmint/config.json
```

### Configuration Options
- `backend_url`: API endpoint URL
- `default_project_type`: Auto-detection or manual override
- `include_contributing`: Include contributing section
- `max_file_size`: Maximum file size for processing
- `max_files`: Maximum number of files to analyze
- `excluded_dirs`: Directories to skip during analysis
- `supported_extensions`: File types to include

## 🐛 Error Handling

The package includes comprehensive error handling for:
- **Network Issues**: Connection timeouts and failures
- **File System Errors**: Permission and encoding issues
- **API Errors**: Backend service failures
- **Configuration Problems**: Invalid settings and missing files

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest docmint/

# Run with coverage
pytest --cov=docmint docmint/
```

## 📈 Performance Considerations

- **File Limits**: Maximum 20 files per analysis to prevent API overload
- **Size Limits**: Files larger than 1MB are automatically excluded
- **Timeout Handling**: 30-60 second timeouts for API requests
- **Memory Management**: Efficient file reading with error handling

## 🔮 Future Enhancements

- **Local Processing**: Offline README generation capabilities
- **Template Customization**: User-defined README templates
- **Plugin System**: Extensible architecture for custom processors
- **Batch Processing**: Multiple project analysis in single run
- **Integration APIs**: Direct integration with Git platforms

---

<div align="center">

**Part of the DocMint Ecosystem**

[![Built with DocMint](https://img.shields.io/badge/Generated%20by-DocMint-red?style=flat-square)](https://github.com/kingsleyesisi/docmint)

</div>