from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import os
from pathlib import Path
import logging

from google import genai
from google.genai import types

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Gemini client
API_KEY = getattr(settings, 'GEMINI_API', None)
if not API_KEY:
    logger.error("GEMINI_API key not found in settings")

client = genai.Client(api_key=API_KEY) if API_KEY else None

# System message for README generation
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are DocMint, a professional README generator. Follow these rules strictly:\n"
        "1. Always include the DocMint badge at the bottom using the exact format provided.\n"
        "2. Do not wrap the README content in markdown code blocks. Output the README.md content directly.\n"
        "3. Write in a human-like tone and ensure the README is professional, modern, and engaging.\n"
        "4. Analyze the code structure and provide accurate installation and usage instructions.\n"
        "5. Include relevant badges, emojis, and modern formatting for better visual appeal.\n"
        "6. If it's an API project, provide clear API documentation with example requests/responses.\n"
        "7. Include a table of contents for longer READMEs (note for longer projects only).\n"
        "8. Add troubleshooting section for complex projects. (note for complex projects only)"
    )
}

# tweak generation settings 
config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
)



def validate_gemini_client():
    """Validate if Gemini client is properly initialized"""
    if not client:
        return False, "Gemini API client not initialized. Check your API key."
    return True, None

def get_file_language(filename):
    """Determine the programming language based on file extension"""
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.vue': 'vue',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
    }
    
    ext = Path(filename).suffix.lower()
    return extension_map.get(ext, 'text')

def analyze_project_structure(files_data):
    """Analyze project structure and provide insights"""
    file_stats = {
        'total_files': len(files_data),
        'languages': {},
        'file_types': {},
        'total_lines': 0,
        'config_files': [],
        'main_files': []
    }
    
    for file_info in files_data:
        filename = file_info['name']
        content = file_info['content']
        
        # Count lines
        lines = len(content.split('\n'))
        file_stats['total_lines'] += lines
        
        # Get language
        lang = get_file_language(filename)
        file_stats['languages'][lang] = file_stats['languages'].get(lang, 0) + 1
        
        # Get file type
        ext = Path(filename).suffix.lower()
        file_stats['file_types'][ext] = file_stats['file_types'].get(ext, 0) + 1
        
        # Identify important files
        important_files = [
            'package.json', 'requirements.txt', 'pom.xml', 'cargo.toml',
            'go.mod', 'composer.json', 'gemfile', 'dockerfile', 'docker-compose.yml',
            'makefile', 'cmake', 'setup.py', 'pyproject.toml'
        ]
        
        if filename.lower() in important_files:
            file_stats['config_files'].append(filename)
        
        # Identify main/entry files
        main_patterns = ['main.', 'index.', 'app.', 'server.', '__init__.']
        if any(pattern in filename.lower() for pattern in main_patterns):
            file_stats['main_files'].append(filename)
    
    return file_stats

def generate_readme_content(prompt, files_data=None, project_stats=None):
    """Generate README content using Gemini AI"""
    is_valid, error_msg = validate_gemini_client()
    if not is_valid:
        return {"error": error_msg}
    
    try:
        # Enhanced prompt with project analysis
        if files_data and project_stats:
            enhanced_prompt = f"""
            {prompt}
            
            ## Project Analysis:
            - Total files: {project_stats['total_files']}
            - Total lines of code: {project_stats['total_lines']:,}
            - Primary languages: {', '.join(project_stats['languages'].keys())}
            - Configuration files found: {', '.join(project_stats['config_files']) if project_stats['config_files'] else 'None'}
            - Main entry files: {', '.join(project_stats['main_files']) if project_stats['main_files'] else 'Not identified'}
            
            Use this analysis to provide more accurate and detailed documentation.
            """
        else:
            enhanced_prompt = prompt
        
        user_message = {"role": "user", "content": enhanced_prompt}

        FULL_PROMPT = [json.dumps(SYSTEM_MESSAGE), json.dumps(user_message)]

        # Steraming response 
        for chunk_response in client.models.generate_content_stream(
            model="gemini-2.0-flash-exp",
            contents=FULL_PROMPT,
            config=config,
        ):
        # response = client.models.generate_content_stream(
        #     model="gemini-2.0-flash-exp",
        #     contents=[json.dumps(SYSTEM_MESSAGE), json.dumps(user_message)]
        # )
        
            if chunk_response.text:
                return {"answer": chunk_response.text.strip()}
            else:
                return {"error": "Empty response from Gemini API"}
            
    except Exception as e:
        print(e)
        logger.error(f"Error generating README: {e}")
        return {"error": f"Failed to generate README: {str(e)}"}

@api_view(['GET'])
def health_check(request):
    """Enhanced health check endpoint"""
    try:
        is_valid, error_msg = validate_gemini_client()
        
        health_data = {
            "status": "healthy" if is_valid else "unhealthy",
            "service": "DocMint README Generator",
            "version": "2.0.0",
            "gemini_api": "connected" if is_valid else "disconnected",
            "supported_formats": [
                "Text prompt", "File upload", "Multi-file projects"
            ]
        }
        
        if not is_valid:
            health_data["error"] = error_msg
            return Response(health_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response(health_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "status": "unhealthy",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def generate_from_prompt(request):
    """Generate README from text prompt"""
    try:
        data = json.loads(request.body) if isinstance(request.body, bytes) else request.data
        prompt = data.get("message", "").strip()
        
        if not prompt:
            return Response({
                "error": "Prompt is required",
                "example": "Describe your project: 'A Python web scraper that extracts data from e-commerce sites'"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add some context to the prompt
        enhanced_prompt = f"""
        Generate a comprehensive README.md for the following project:
        
        {prompt}
        
        Please include all standard sections and make it professional and engaging.
        """
        
        result = generate_readme_content(enhanced_prompt)
        
        if "error" in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(result, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response({
            "error": "Invalid JSON payload"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in generate_from_prompt: {e}")
        return Response({
            "error": f"Internal server error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def generate_from_files(request):
    """Generate README from uploaded files"""
    try:
        if 'files' not in request.FILES:
            return Response({
                "error": "Files are required",
                "supported_formats": [
                        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".cs",
                        ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".scala", ".html",
                        ".css", ".scss", ".sass", ".less", ".vue", ".svelte", ".md", ".txt",
                        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".sh", 
                        ".bash", ".zsh", ".ps1", ".psm1", ".sql", ".pl", ".pyx", ".r", ".dart",
                        ".lua", ".groovy", ".kotlin", ".h", ".hpp", ".cxx", ".m", ".t", ".swift", 
                        ".pl", ".pm",
                    ]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        files = request.FILES.getlist('files')
        if not files:
            return Response({
                "error": "No files provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        project_type = request.POST.get('projectType', '').strip()
        if not project_type:
            return Response({
                "error": "Project type is required",
                "supported_types": ["Python", "JavaScript", "Java", "C++", "Web Development", "API", "Mobile App"]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        contribution = request.POST.get('contribution', 'true').lower() == 'true'
        include_api_docs = request.POST.get('includeApiDocs', 'false').lower() == 'true' 
        include_deployment = request.POST.get('includeDeployment', 'true').lower() == 'true'
        
        # Process files
        files_data = []
        supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs',
            '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.html',
            '.css', '.scss', '.sass', '.vue', '.json', '.xml', '.yaml', '.yml',
            '.md', '.txt', '.toml', '.ini', '.cfg', '.conf'
        }
        
        for file in files:
            try:
                filename = file.name
                file_ext = Path(filename).suffix.lower()
                
                # Check file extension
                if file_ext not in supported_extensions:
                    logger.warning(f"Skipping unsupported file: {filename}")
                    continue
                
                # Check file size (max 1MB per file)
                if file.size > 1024 * 1024:
                    logger.warning(f"Skipping large file: {filename} ({file.size} bytes)")
                    continue
                
                content = file.read().decode('utf-8', errors='ignore')
                
                if content.strip():
                    files_data.append({
                        'name': filename,
                        'content': content,
                        'size': len(content),
                        'extension': file_ext
                    })
            
            except Exception as e:
                logger.error(f"Error processing file {file.name}: {e}")
                continue
        
        if not files_data:
            return Response({
                "error": "No valid files found to process"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Analyze project structure
        project_stats = analyze_project_structure(files_data)
        
        # Create file summary
        file_details = []
        combined_content = ""
        
        for file_data in files_data:
            file_details.append(f"- **{file_data['name']}** ({file_data['size']:,} chars)")
            combined_content += f"\n\n## File: {file_data['name']}\n```{get_file_language(file_data['name'])}\n{file_data['content']}\n```"
        
        # Generate comprehensive prompt
        prompt = f"""
        Generate a **professional, comprehensive, and modern README.md** for a **{project_type}** project.

        ## Project Overview:
        This project contains {project_stats['total_files']} files with {project_stats['total_lines']:,} total lines of code.
        
        **Files included:**
        {chr(10).join(file_details)}
        
        **Primary languages:** {', '.join(project_stats['languages'].keys())}
        
        ## Complete Source Code:
        {combined_content}

        ## README Requirements:
        
        ### Required Sections:
        1. **Project Title & Description** - Clear, engaging project description
        2. **Table of Contents** - For easy navigation
        3. **Features** - Key functionality and highlights
        4. **Technologies Used** - Tech stack with badges
        5. **Installation** - Step-by-step setup instructions
        6. **Usage** - Clear usage examples and instructions
        {"7. **API Documentation** - Endpoints, request/response examples" if include_api_docs else ""}
        {"8. **Deployment** - Deployment instructions and considerations" if include_deployment else ""}
        {"9. **Contributing** - Contribution guidelines and process" if contribution else ""}
        10. **License** - License information
        11. **Acknowledgments** - Credits and thanks

        ### Style Guidelines:
        - Use emojis appropriately for better visual appeal
        - Include relevant badges (build status, version, license, etc.)
        - Add code examples with syntax highlighting
        - Use tables for structured information
        - Include screenshots section placeholder if it's a visual project
        - Add troubleshooting section for common issues
        
        ### Special Instructions:
        - Analyze the actual code to provide accurate setup instructions
        - If it's an API, include endpoint documentation with examples
        - For web projects, include both development and production setup
        - Add environment variables section if config files are present and Env example
        - Include testing instructions if test files are detected
        
        ### Footer:
        Always end with this exact badge:
        [![Built with DocMint](https://img.shields.io/badge/Generated%20by-DocMint-red)](https://github.com/kingsleyesisi/DocMint)
        
        ## Output Format:
        Generate the complete README.md content directly without markdown code block wrappers.
        Make it sound human-written and avoid generic boilerplate text.
        """
        
        result = generate_readme_content(prompt, files_data, project_stats)
        
        # Add metadata to response
        if "answer" in result:
            response_data = {
                "result": result,
                "metadata": {
                    "files_processed": len(files_data),
                    "total_lines": project_stats['total_lines'],
                    "primary_languages": list(project_stats['languages'].keys()),
                    "project_type": project_type,
                    "generated_at": json.dumps(None),  # Will be handled by frontend
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        logger.error(f"Error in generate_from_files: {e}")
        return Response({
            "error": f"Internal server error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_supported_formats(request):
    """Get list of supported file formats and project types"""
    return Response({
        "supported_file_extensions": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".cs",
        ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".scala", ".html",
        ".css", ".scss", ".sass", ".less", ".vue", ".svelte", ".md", ".txt",
        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".sh", 
        ".bash", ".zsh", ".ps1", ".psm1", ".sql", ".pl", ".pyx", ".r", ".dart",
        ".lua", ".groovy", ".kotlin", ".h", ".hpp", ".cxx", ".m", ".t", ".swift", 
        ".pl", ".pm",
    ],
        "supported_project_types": [
            "Python", "JavaScript", "TypeScript", "Node.js", "React", "Vue.js",
            "Java", "Spring Boot", "C++", "C#/.NET", "PHP", "Ruby", "Go",
            "Rust", "Swift", "Kotlin", "Web Development", "API", "Mobile App",
            "Machine Learning", "Data Science", "DevOps", "General Software"
        ],
        "max_file_size_mb": 10,
        "max_files_per_request": 20
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def validate_project(request):
    """Validate project structure and provide recommendations"""
    try:
        data = request.data
        files = data.get('files', [])
        project_type = data.get('projectType', '')
        
        if not files:
            return Response({
                "error": "Files list is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Analyze the file structure
        recommendations = []
        warnings = []
        
        file_names = [f.get('name', '') for f in files]
        
        # Check for common missing files
        common_files = {
            'Python': ['requirements.txt', 'setup.py', 'README.md'],
            'JavaScript': ['package.json', 'README.md'],
            'Java': ['pom.xml', 'build.gradle', 'README.md'],
        }
        
        if project_type in common_files:
            for required_file in common_files[project_type]:
                if not any(required_file in name for name in file_names):
                    recommendations.append(f"Consider adding {required_file}")
        
        # Check for README
        has_readme = any('readme' in name.lower() for name in file_names)
        if not has_readme:
            recommendations.append("No README.md found - this tool will generate one for you!")
        
        return Response({
            "valid": True,
            "recommendations": recommendations,
            "warnings": warnings,
            "file_count": len(files),
            "estimated_readme_sections": 8 + len(recommendations)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Legacy endpoint for backward compatibility
@csrf_exempt
def test(request):
    """Legacy test endpoint - kept for backward compatibility"""
    if request.method == "GET":
        try:
            test_prompt = "Write a comprehensive README for a Python project that calculates Fibonacci numbers with CLI interface and web API."
            result = generate_readme_content(test_prompt)
            
            if "error" in result:
                return JsonResponse({"error": result["error"]}, status=500)
            
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only GET method is allowed"}, status=405)

# Legacy endpoint for backward compatibility
@csrf_exempt  
def index(request):
    """Legacy index endpoint - redirects to new API"""
    if request.method == "POST":
        try:
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect('/api/generate/')
        except Exception as e:
            return JsonResponse({"error": "Please use /api/generate/ endpoint"}, status=400)
    else:
        return JsonResponse({
            "message": "DocMint README Generator API",
            "version": "2.0.0",
            "endpoints": {
                "health": "/api/health/",
                "generate_from_prompt": "/api/generate/", 
                "generate_from_files": "/api/generate-from-files/",
                "supported_formats": "/api/formats/",
                "validate_project": "/api/validate/",
                'test': '/test/'
            }
        }, status=200)
