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
    version="0.1.3",  # Increment version for new release
    author="Kingsley Esisi",
    author_email="kingsleyesisi@yahoo.com",
    description="DocMint: A professional tool for generating comprehensive README and documentation files effortlessly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kingsleyesisi/docmint",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Documentation",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),  # NOW using the function!
    entry_points={
        "console_scripts": [
            "docmint=docmint.cli:main",  # This creates the CLI command
        ],
    },
    include_package_data=True,
    zip_safe=False,
)