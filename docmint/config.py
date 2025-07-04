# docmint_cli/config.py
"""
Configuration settings for DocMint CLI
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any

# Default backend URL
DEFAULT_BACKEND_URL = "https://docmint.onrender.com"

# Configuration file path
CONFIG_DIR = Path.home() / ".docmint"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "backend_url": DEFAULT_BACKEND_URL,
    "default_project_type": "auto",
    "include_contributing": True,
    "max_file_size": 100 * 1024 * 1024,  # 100MB
    "max_files": 150,
    "excluded_dirs": [
        "node_modules", ".git", "__pycache__", ".pytest_cache",
        "venv", "env", ".env", "dist", "build", ".next",
        "target", "bin", "obj", ".gradle", "vendor", "coverage",
        ".nyc_output", ".sass-cache", "bower_components",
        "jspm_packages", "web_modules", ".yarn", ".pnp",
        "Pods", "DerivedData", ".vs", ".vscode/settings.json"
    ],
    "excluded_files": [
        "*.log", "*.tmp", "*.temp", "*.cache", "*.pid",
        "*.lock", "*.swp", "*.swo", "*~", ".DS_Store",
        "Thumbs.db", "desktop.ini", "*.pyc", "*.pyo",
        "*.class", "*.o", "*.so", "*.dll", "*.exe"
    ],
    "supported_extensions": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".cs",
        ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".scala", ".html",
        ".css", ".scss", ".sass", ".less", ".vue", ".svelte", ".md", ".txt",
        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", 
        ".sh", ".bash", ".zsh", ".ps1", ".psm1", ".sql", ".pl", ".pyx", 
        ".r", ".dart", ".lua", ".groovy", ".kotlin", ".h", ".hpp", ".cxx", 
        ".m", ".t", ".swift", ".pl", ".pm", ".dockerfile", ".makefile",
        ".gradle", ".maven", ".sbt", ".clj", ".cljs", ".elm", ".ex", ".exs"
    ]
}

def get_config() -> Dict[str, Any]:
    """Load configuration from file or return defaults"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults for missing keys
                merged_config = DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False

def add_excluded_dir(directory: str) -> bool:
    """Add a directory to the excluded list"""
    config = get_config()
    if directory not in config['excluded_dirs']:
        config['excluded_dirs'].append(directory)
        return save_config(config)
    return True

def add_excluded_file(file_pattern: str) -> bool:
    """Add a file pattern to the excluded list"""
    config = get_config()
    if file_pattern not in config['excluded_files']:
        config['excluded_files'].append(file_pattern)
        return save_config(config)
    return True

def remove_excluded_dir(directory: str) -> bool:
    """Remove a directory from the excluded list"""
    config = get_config()
    if directory in config['excluded_dirs']:
        config['excluded_dirs'].remove(directory)
        return save_config(config)
    return True

def remove_excluded_file(file_pattern: str) -> bool:
    """Remove a file pattern from the excluded list"""
    config = get_config()
    if file_pattern in config['excluded_files']:
        config['excluded_files'].remove(file_pattern)
        return save_config(config)
    return True

def reset_config() -> bool:
    """Reset configuration to defaults"""
    return save_config(DEFAULT_CONFIG.copy())

def show_config() -> str:
    """Return formatted configuration as string"""
    config = get_config()
    return json.dumps(config, indent=2)