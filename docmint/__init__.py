"""
🌟 DocMint - Professional README & Documentation Generator

DocMint is a powerful Python package that automatically generates comprehensive, 
professional README files for your projects. Simply point it at your codebase, 
and watch as it analyzes your files, understands your project structure, and 
creates beautiful documentation that makes your project shine.

Key Features:
- 🤖 AI-Powered Analysis: Intelligent project understanding
- 🔍 Smart Detection: Automatically identifies project type and structure  
- 📝 Professional Templates: Beautiful, industry-standard README formats
- 🌈 Colorful CLI: Rich terminal output with progress indicators
- ⚙️ Configurable: Extensive configuration options
- 🌍 Cross-Platform: Works on Windows, macOS, and Linux

Usage:
    $ pip install docmint
    $ docmint                    # Generate README for current directory
    $ docmint -d /path/to/proj   # Analyze specific directory
    $ docmint -p "My project"    # Generate from description

For more information, visit: https://github.com/kingsleyesisi/docmint
"""

__version__ = "0.2.0"
__author__ = "Kingsley Esisi"
__email__ = "kingsleyesisi@yahoo.com"
__license__ = "MIT"
__description__ = "Professional README & Documentation Generator"
__url__ = "https://github.com/kingsleyesisi/docmint"

# Package metadata
__title__ = "docmint"
__summary__ = "🌟 Transform your projects into professionally documented masterpieces with AI-powered README generation"
__keywords__ = ["readme", "documentation", "generator", "markdown", "cli", "ai-powered"]

# Version info tuple for programmatic access
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Export main components for programmatic access
from .cli import DocMintCLI, main

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__license__",
    "__description__",
    "__url__",
    "DocMintCLI",
    "main",
    "VERSION_INFO"
]

# Package banner for CLI
BANNER = """
🌟 DocMint v{version}
Professional README & Documentation Generator
Made with ❤️  by {author}
""".format(version=__version__, author=__author__)