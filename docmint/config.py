
# docmint_cli/config.py
"""
Configuration settings for DocMint CLI
"""

import os
from pathlib import Path

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
        "target", "bin", "obj", ".gradle", "vendor"
    ],
    "supported_extensions": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".cs",
        ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".scala", ".html",
        ".css", ".scss", ".sass", ".less", ".vue", ".svelte", ".md", ".txt",
        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".sh", 
        ".bash", ".zsh", ".ps1", ".psm1", ".sql", ".pl", ".pyx", ".r", ".dart",
        ".lua", ".groovy", ".kotlin", ".h", ".hpp", ".cxx", ".m", ".t", ".swift", 
        ".pl", ".pm",
    ]
}

def get_config():
    """Load configuration from file or return defaults"""
    if CONFIG_FILE.exists():
        try:
            import json
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults for missing keys
                merged_config = DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    try:
        import json
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False
