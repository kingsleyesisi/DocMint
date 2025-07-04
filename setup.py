from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements properly
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            requirements = []
            for line in fh:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#"):
                    requirements.append(line)
        return requirements
    
    except FileNotFoundError:
        # Fallback to hardcoded requirements if file not found
        return [
            "click>=8.2.0",
            "requests>=2.32.0",
            "rich>=13.9.0",
            "typer>=0.15.0"
        ]

setup(
    name="docmint",
    version="0.2.0",  # Updated version for new release
    author="Kingsley Esisi",
    author_email="kingsleyesisi@yahoo.com",
    description="🌟 DocMint: Professional README & Documentation Generator - Transform your projects into professionally documented masterpieces with AI-powered README generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kingsleyesisi/docmint",
    project_urls={
        "Bug Reports": "https://github.com/kingsleyesisi/docmint/issues",
        "Source": "https://github.com/kingsleyesisi/docmint",
        "Documentation": "https://github.com/kingsleyesisi/docmint#readme",
        "Changelog": "https://github.com/kingsleyesisi/docmint/releases",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="readme documentation generator markdown cli tool python package ai-powered",
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "docmint=docmint.cli:main",  # This creates the CLI command
        ],
    },
    include_package_data=True,
    zip_safe=False,
    # Additional metadata for better discoverability
    platforms=["any"],
    license="MIT",
    # Package data
    package_data={
        "docmint": ["*.md", "*.txt"],
    },
)