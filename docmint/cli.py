#!/usr/bin/env python3
"""
DocMint CLI - A command-line tool for generating professional README files
Compatible with Windows, macOS, and Linux
"""

import os
import sys
import json
import argparse
import requests
import time
from pathlib import Path
from typing import List, Optional, Dict, Set
import mimetypes

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Windows compatibility
    @staticmethod
    def init_windows():
        if sys.platform == "win32":
            try:
                import colorama
                colorama.init()
            except ImportError:
                # Fallback to empty strings if colorama not available
                for attr in dir(Colors):
                    if not attr.startswith('_') and attr not in ['init_windows', 'strip']:
                        setattr(Colors, attr, '')
    
    @staticmethod
    def strip(text: str) -> str:
        """Remove color codes from text"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

# Initialize colors for Windows
Colors.init_windows()

class DocMintCLI:
    def __init__(self, base_url: str = "https://docmint.onrender.com"):
        self.base_url = base_url.rstrip('/')
        self.supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs',
            '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.html',
            '.css', '.scss', '.sass', '.less', '.vue', '.svelte', '.md', '.txt',
            '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'
        }
        
        # Load configuration
        from .config import get_config
        self.config = get_config()
        
        # Update supported extensions from config
        if 'supported_extensions' in self.config:
            self.supported_extensions.update(self.config['supported_extensions'])
    
    def print_banner(self):
        """Print the DocMint CLI banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ██████╗    ██████╗   ██████╗ ███╗   ███╗██╗███╗   ██╗████████╗  ║
║  ██╔═══██  ██╔═══██╗ ██╔════╝ ████╗ ████║██║████╗  ██║╚══██╔══╝  ║
║  ██║   ██╗ ██║   ██║ ██║      ██╔████╔██║██║██╔██╗ ██║   ██║     ║
║  ██║   ██║ ██║   ██║ ██║      ██║╚██╔╝██║██║██║╚██╗██║   ██║     ║
║  ██████ ╔╝ ╚██████╔╝ ╚██████╗ ██║ ╚═╝ ██║██║██║ ╚████║   ██║     ║
║   ╚═════╝   ╚═════╝   ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝     ║
║                                                                  ║
║    Professional README/Documentation Generator                   ║
║    Compatible with Windows, macOS, and Linux                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
        print(banner)
    
    def print_success(self, message: str):
        print(f"{Colors.GREEN}{Colors.BOLD}✓{Colors.END} {Colors.GREEN}{message}{Colors.END}")
    
    def print_error(self, message: str):
        print(f"{Colors.RED}{Colors.BOLD}✗{Colors.END} {Colors.RED}{message}{Colors.END}")
    
    def print_warning(self, message: str):
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠{Colors.END} {Colors.YELLOW}{message}{Colors.END}")
    
    def print_info(self, message: str):
        print(f"{Colors.BLUE}{Colors.BOLD}ℹ{Colors.END} {Colors.BLUE}{message}{Colors.END}")
    
    def print_progress(self, message: str):
        print(f"{Colors.MAGENTA}{Colors.BOLD}⟳{Colors.END} {Colors.MAGENTA}{message}{Colors.END}")
    
    def animate_loading(self, message: str, duration: float = 2.0):
        """Animate a loading spinner"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        start_time = time.time()
        i = 0
        
        while time.time() - start_time < duration:
            print(f"\r{Colors.CYAN}{chars[i % len(chars)]}{Colors.END} {message}", end="", flush=True)
            time.sleep(0.1)
            i += 1
        
        print(f"\r{Colors.GREEN}✓{Colors.END} {message}")
    
    def check_network_connection(self) -> bool:
        """Check if the backend is reachable"""
        try:
            response = requests.get(f"{self.base_url}/api/health/", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            try:
                # Fallback: try to reach a known endpoint
                response = requests.head(self.base_url, timeout=5)
                return True
            except requests.exceptions.RequestException:
                return False
    
    def parse_exclude_patterns(self, exclude_args: List[str]) -> Set[str]:
        """Parse exclude arguments into a set of patterns"""
        exclude_patterns = set()
        
        for pattern in exclude_args:
            # Handle comma-separated values
            if ',' in pattern:
                exclude_patterns.update(p.strip() for p in pattern.split(','))
            else:
                exclude_patterns.add(pattern.strip())
        
        return exclude_patterns
    
    def should_exclude_path(self, file_path: Path, exclude_dirs: Set[str], exclude_files: Set[str]) -> bool:
        """Check if a path should be excluded based on patterns"""
        path_str = str(file_path)
        path_parts = file_path.parts
        
        # Check directory exclusions
        for exclude_dir in exclude_dirs:
            # Exact directory name match
            if exclude_dir in path_parts:
                return True
            # Pattern matching (simple wildcards)
            if '*' in exclude_dir:
                import fnmatch
                if any(fnmatch.fnmatch(part, exclude_dir) for part in path_parts):
                    return True
        
        # Check file exclusions
        for exclude_file in exclude_files:
            # Exact filename match
            if file_path.name == exclude_file:
                return True
            # Pattern matching (simple wildcards)
            if '*' in exclude_file:
                import fnmatch
                if fnmatch.fnmatch(file_path.name, exclude_file):
                    return True
            # Full path pattern matching
            if '/' in exclude_file or '\\' in exclude_file:
                import fnmatch
                if fnmatch.fnmatch(path_str, exclude_file):
                    return True
        
        return False
    
    def get_project_files(self, directory: str, exclude_dirs: Optional[Set[str]] = None, 
                         exclude_files: Optional[Set[str]] = None) -> List[Path]:
        """Get all supported project files from the directory"""
        if exclude_dirs is None:
            exclude_dirs = set(self.config.get('excluded_dirs', [
                'node_modules', '.git', '__pycache__', '.pytest_cache',
                'venv', 'env', '.env', 'dist', 'build', '.next',
                'target', 'bin', 'obj', '.gradle', 'vendor'
            ]))
        
        if exclude_files is None:
            exclude_files = set()
        
        files = []
        directory_path = Path(directory)
        excluded_count = 0
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file():
                # Check if file should be excluded
                if self.should_exclude_path(file_path, exclude_dirs, exclude_files):
                    excluded_count += 1
                    continue
                
                # Check if file extension is supported
                if file_path.suffix.lower() in self.supported_extensions:
                    # Skip very large files (>1MB by default)
                    max_size = self.config.get('max_file_size', 1024 * 1024)
                    if file_path.stat().st_size < max_size:
                        files.append(file_path)
        
        # Show exclusion summary
        if excluded_count > 0:
            self.print_info(f"Excluded {excluded_count} files/directories based on patterns")
        
        # Limit files based on config
        max_files = self.config.get('max_files', 20)
        return files[:max_files]
    
    def detect_project_type(self, files: List[Path]) -> str:
        """Detect the project type based on files"""
        file_names = [f.name.lower() for f in files]
        extensions = [f.suffix.lower() for f in files]
        
        # Check for specific files that indicate project type
        if 'package.json' in file_names:
            return 'Node.js/JavaScript'
        elif 'requirements.txt' in file_names or 'setup.py' in file_names or 'pyproject.toml' in file_names:
            return 'Python'
        elif 'pom.xml' in file_names or 'build.gradle' in file_names:
            return 'Java'
        elif 'cargo.toml' in file_names:
            return 'Rust'
        elif 'go.mod' in file_names:
            return 'Go'
        elif 'composer.json' in file_names:
            return 'PHP'
        elif 'gemfile' in file_names:
            return 'Ruby'
        elif any('.csproj' in name for name in file_names):
            return 'C#/.NET'
        elif '.swift' in extensions:
            return 'Swift'
        elif '.kt' in extensions or '.kts' in extensions:
            return 'Kotlin'
        elif '.cpp' in extensions or '.cc' in extensions or '.cxx' in extensions:
            return 'C++'
        elif '.c' in extensions:
            return 'C'
        elif '.html' in extensions or '.css' in extensions:
            return 'Web Development'
        else:
            return 'General Software'
    
    def generate_readme_from_prompt(self, prompt: str) -> Optional[str]:
        """Generate README from a text prompt"""
        try:
            self.print_progress("Generating README from prompt...")
            
            payload = {"message": prompt}
            
            response = requests.post(
                f"{self.base_url}/api/generate/",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'answer' in result:
                    return result['answer']
                elif 'error' in result:
                    self.print_error(f"API Error: {result['error']}")
                    return None
            else:
                self.print_error(f"HTTP Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.print_error("Request timed out. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            self.print_error(f"Network error: {str(e)}")
            return None
        except Exception as e:
            self.print_error(f"Unexpected error: {str(e)}")
            return None
    
    def generate_readme_from_files(self, files: List[Path], project_type: str, include_contributing: bool = True) -> Optional[str]:
        """Generate README from project files"""
        try:
            self.print_progress(f"Analyzing {len(files)} files...")
            
            # Prepare files for upload
            files_data = []
            file_contents = {}
            
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if content.strip():  # Only include non-empty files
                            relative_path = str(file_path.relative_to(Path.cwd()))
                            files_data.append(('files', (relative_path, content, 'text/plain')))
                            file_contents[relative_path] = len(content)
                except Exception as e:
                    self.print_warning(f"Could not read {file_path}: {str(e)}")
                    continue
            
            if not files_data:
                self.print_error("No readable files found.")
                return None
            
            # Show file summary
            self.print_info(f"Processing files:")
            for file_tuple in files_data[:10]:  # Show first 10 files
                filename = file_tuple[1][0]
                size = file_contents.get(filename, 0)
                print(f"  {Colors.CYAN}•{Colors.END} {filename} ({size:,} chars)")
            
            if len(files_data) > 10:
                self.print_info(f"... and {len(files_data) - 10} more files")
            
            # Prepare the request
            data = {
                'projectType': project_type,
                'contribution': str(include_contributing).lower()
            }
            
            self.print_progress("Generating README...")
            
            response = requests.post(
                f"{self.base_url}/api/generate-from-files/",
                files=files_data,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and 'answer' in result['result']:
                    return result['result']['answer']
                elif 'error' in result:
                    self.print_error(f"API Error: {result['error']}")
                    return None
            else:
                self.print_error(f"HTTP Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.print_error("Request timed out. The project might be too large. Try with fewer files.")
            return None
        except requests.exceptions.RequestException as e:
            self.print_error(f"Network error: {str(e)}")
            return None
        except Exception as e:
            self.print_error(f"Unexpected error: {str(e)}")
            return None
    
    def save_readme(self, content: str, output_path: str = "README.md") -> bool:
        """Save the generated README content to a file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            self.print_error(f"Could not save README: {str(e)}")
            return False
    
    def run(self):
        """Main CLI execution"""
        parser = argparse.ArgumentParser(
            description="DocMint CLI - Generate professional README files",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
Examples:
  {Colors.GREEN}docmint{Colors.END}                          # Generate from current directory
  {Colors.GREEN}docmint -d /path/to/project{Colors.END}     # Generate from specific directory
  {Colors.GREEN}docmint -p "My awesome project"{Colors.END}  # Generate from text prompt
  {Colors.GREEN}docmint -t Python -o MyREADME.md{Colors.END}  # Specify project type and output
  {Colors.GREEN}docmint --no-contributing{Colors.END}       # Skip contributing section
  {Colors.GREEN}docmint --exclude-dir node_modules,dist{Colors.END}  # Exclude specific directories
  {Colors.GREEN}docmint --exclude-file "*.log,temp*"{Colors.END}     # Exclude specific files
  {Colors.GREEN}docmint --url http://localhost:8000{Colors.END}  # Use local backend

Exclude Patterns:
  {Colors.CYAN}--exclude-dir{Colors.END}    Exclude directories (supports wildcards)
  {Colors.CYAN}--exclude-file{Colors.END}   Exclude files (supports wildcards and patterns)
  
  Examples:
    {Colors.YELLOW}--exclude-dir "temp*,cache,logs"{Colors.END}
    {Colors.YELLOW}--exclude-file "*.log,*.tmp,secret.txt"{Colors.END}
    {Colors.YELLOW}--exclude-file "tests/*,docs/*.md"{Colors.END}
            """
        )
        
        parser.add_argument('-d', '--directory', 
                          default='.', 
                          help='Directory to analyze (default: current directory)')
        
        parser.add_argument('-p', '--prompt', 
                          help='Generate README from text prompt instead of files')
        
        parser.add_argument('-t', '--type', 
                          help='Specify project type (auto-detected if not provided)')
        
        parser.add_argument('-o', '--output', 
                          default='README.md', 
                          help='Output file name (default: README.md)')
        
        parser.add_argument('--no-contributing', 
                          action='store_true',
                          help='Skip contributing section in README')
        
        parser.add_argument('--exclude-dir', 
                          action='append',
                          default=[],
                          help='Exclude directories (can be used multiple times, supports wildcards)')
        
        parser.add_argument('--exclude-file', 
                          action='append',
                          default=[],
                          help='Exclude files (can be used multiple times, supports wildcards)')
        
        parser.add_argument('--url', 
                          default='https://docmint.onrender.com',
                          help='Backend URL (default: https://docmint.onrender.com)')  
        
        parser.add_argument('--no-banner', 
                          action='store_true',
                          help='Skip the banner display')
        
        parser.add_argument('--show-config', 
                          action='store_true',
                          help='Show current configuration and exit')
        
        args = parser.parse_args()
        
        # Show configuration if requested
        if args.show_config:
            self.print_info("Current DocMint Configuration:")
            print(json.dumps(self.config, indent=2))
            return 0
        
        # Update base URL
        self.base_url = args.url.rstrip('/')
        
        # Show banner
        if not args.no_banner:
            self.print_banner()
        
        # Parse exclude patterns
        exclude_dirs = set(self.config.get('excluded_dirs', []))
        exclude_files = set()
        
        if args.exclude_dir:
            custom_exclude_dirs = self.parse_exclude_patterns(args.exclude_dir)
            exclude_dirs.update(custom_exclude_dirs)
            self.print_info(f"Custom excluded directories: {', '.join(custom_exclude_dirs)}")
        
        if args.exclude_file:
            exclude_files = self.parse_exclude_patterns(args.exclude_file)
            self.print_info(f"Custom excluded files: {', '.join(exclude_files)}")
        
        # Check network connection
        self.print_progress("Checking connection to DocMint backend...")
        if not self.check_network_connection():
            self.print_error(f"Cannot connect to DocMint backend at {self.base_url}")
            self.print_info("Please check:")
            self.print_info("1. Your internet connection")
            self.print_info("2. The backend URL is correct")
            self.print_info("3. The DocMint backend is running")
            return 1
        
        self.print_success("Connected to DocMint backend!")
        
        # Generate README
        readme_content = None
        
        if args.prompt:
            # Generate from prompt
            readme_content = self.generate_readme_from_prompt(args.prompt)
        else:
            # Generate from files
            directory = Path(args.directory).resolve()
            
            if not directory.exists() or not directory.is_dir():
                self.print_error(f"Directory not found: {directory}")
                return 1
            
            self.print_info(f"Analyzing project in: {directory}")
            
            # Show exclusion patterns being used
            if exclude_dirs:
                self.print_info(f"Excluding directories: {', '.join(sorted(exclude_dirs))}")
            if exclude_files:
                self.print_info(f"Excluding files: {', '.join(sorted(exclude_files))}")
            
            # Get project files
            files = self.get_project_files(str(directory), exclude_dirs, exclude_files)
            
            if not files:
                self.print_warning("No supported code files found in the directory.")
                self.print_info("Supported file types: " + ", ".join(sorted(self.supported_extensions)))
                
                # Ask if user wants to proceed with a manual prompt
                try:
                    response = input(f"\n{Colors.YELLOW}Would you like to describe your project manually? (y/N): {Colors.END}")
                    if response.lower().startswith('y'):
                        prompt = input(f"{Colors.CYAN}Describe your project: {Colors.END}")
                        if prompt.strip():
                            readme_content = self.generate_readme_from_prompt(prompt)
                    else:
                        return 1
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}Operation cancelled.{Colors.END}")
                    return 1
            else:
                # Detect or use provided project type
                project_type = args.type or self.detect_project_type(files)
                self.print_info(f"Detected project type: {Colors.BOLD}{project_type}{Colors.END}")
                
                # Generate README from files
                readme_content = self.generate_readme_from_files(
                    files, 
                    project_type, 
                    not args.no_contributing
                )
        
        # Save README
        if readme_content:
            self.print_progress("Saving README...")
            
            if self.save_readme(readme_content, args.output):
                self.print_success(f"README generated successfully: {Colors.BOLD}{args.output}{Colors.END}")
                
                # Show file size
                file_size = len(readme_content.encode('utf-8'))
                self.print_info(f"File size: {file_size:,} bytes")
                
                # Show first few lines as preview
                lines = readme_content.split('\n')[:5]
                self.print_info("Preview:")
                for line in lines:
                    print(f"  {Colors.CYAN}│{Colors.END} {line}")
                if len(readme_content.split('\n')) > 5:
                    print(f"  {Colors.CYAN}│{Colors.END} ...")
                
            else:
                return 1
        else:
            self.print_error("Failed to generate README")
            return 1
        
        return 0

def main():
    """Entry point for the CLI"""
    try:
        cli = DocMintCLI()
        return cli.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}")
        return 1
    except Exception as e:
        print(f"{Colors.RED}{Colors.BOLD}Unexpected error:{Colors.END} {Colors.RED}{str(e)}{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())