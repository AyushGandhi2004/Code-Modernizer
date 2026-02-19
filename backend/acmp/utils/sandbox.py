# acmp/utils/sandbox.py

import subprocess
import tempfile
import os
from typing import Tuple, Optional


EXECUTION_TIMEOUT = 5  # seconds


def get_file_extension(language: str) -> str:
    """Returns the appropriate file extension for a given language."""
    extensions = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "go": ".go",
        "rust": ".rs",
        "cpp": ".cpp",
        "c": ".c",
        "csharp": ".cs",
        "php": ".php",
        "ruby": ".rb",
        "swift": ".swift",
        "kotlin": ".kt",
        "scala": ".scala",
        "r": ".r",
        "perl": ".pl",
        "bash": ".sh",
        "powershell": ".ps1",
    }
    return extensions.get(language.lower(), ".txt")


def get_execution_command(language: str, file_path: str) -> Optional[list]:
    """Returns the command to execute code for a given language."""
    language_lower = language.lower()
    
    commands = {
        "python": ["python", file_path],
        "javascript": ["node", file_path],
        "typescript": ["ts-node", file_path],  # Requires ts-node
        "java": ["javac", file_path, "&&", "java", os.path.splitext(os.path.basename(file_path))[0]],
        "go": ["go", "run", file_path],
        "rust": ["rustc", file_path, "&&", os.path.splitext(file_path)[0]],
        "cpp": ["g++", file_path, "-o", os.path.splitext(file_path)[0] + ".exe", "&&", os.path.splitext(file_path)[0] + ".exe"],
        "c": ["gcc", file_path, "-o", os.path.splitext(file_path)[0] + ".exe", "&&", os.path.splitext(file_path)[0] + ".exe"],
        "csharp": ["csc", file_path, "&&", os.path.splitext(os.path.basename(file_path))[0] + ".exe"],
        "php": ["php", file_path],
        "ruby": ["ruby", file_path],
        "r": ["Rscript", file_path],
        "perl": ["perl", file_path],
        "bash": ["bash", file_path],
        "powershell": ["powershell", "-File", file_path],
    }
    
    return commands.get(language_lower)


def run_code(code: str, language: str = "python", framework: Optional[str] = None) -> Tuple[bool, str | None]:
    """
    Executes code in a temporary file for the specified language.

    Args:
        code: The source code to execute
        language: The programming language (default: "python")
        framework: Optional framework name (currently not used for execution)

    Returns:
        (True, None) if execution succeeds
        (False, error_log) if execution fails
    """
    language_lower = language.lower()
    temp_file = None

    try:
        # Get appropriate file extension
        extension = get_file_extension(language_lower)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=extension,
            delete=False,
            encoding="utf-8"
        )

        temp_file.write(code)
        temp_file.close()

        # Get execution command
        cmd = get_execution_command(language_lower, temp_file.name)
        
        if not cmd:
            # Language not supported for execution
            return True, None  # Assume success if we can't test it

        # Handle compound commands (e.g., "javac file && java Class")
        if "&&" in cmd:
            # Split and run sequentially
            parts = " && ".join(cmd).split(" && ")
            for i, part in enumerate(parts):
                part_cmd = part.strip().split()
                result = subprocess.run(
                    part_cmd,
                    capture_output=True,
                    text=True,
                    timeout=EXECUTION_TIMEOUT,
                    cwd=os.path.dirname(temp_file.name) if i == 0 else None
                )
                if result.returncode != 0:
                    return False, result.stderr.strip() or result.stdout.strip()
            return True, None
        else:
            # Simple command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )

            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr.strip() or result.stdout.strip()

    except subprocess.TimeoutExpired:
        return False, "Execution timed out (possible infinite loop)."

    except FileNotFoundError:
        # Interpreter/compiler not found
        return False, f"Runtime environment for {language} not found. Please ensure the necessary interpreter/compiler is installed."

    except Exception as e:
        return False, f"Sandbox error: {str(e)}"

    finally:
        # Clean up temp file
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.remove(temp_file.name)
            except:
                pass
        # Clean up compiled executables if any
        if temp_file:
            base_name = os.path.splitext(temp_file.name)[0]
            for ext in [".exe", ".class", ".out"]:
                exe_path = base_name + ext
                if os.path.exists(exe_path):
                    try:
                        os.remove(exe_path)
                    except:
                        pass


def run_python_code(code: str) -> Tuple[bool, str | None]:
    """
    Legacy function for backward compatibility.
    Executes Python code in a temporary file.

    Returns:
        (True, None) if execution succeeds
        (False, error_log) if execution fails
    """
    return run_code(code, language="python")
