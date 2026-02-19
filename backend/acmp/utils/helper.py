import re

def extract_code_block(text: str) -> str:
    """
    Extract pure code from model output.
    Removes markdown fences and explanations.
    """
    if not text:
        return ""

    s = text.strip()

    # 1) If the model returned a fenced code block, prefer the first fenced block.
    # Supports ```lang\n...\n``` and ```\n...\n```.
    fenced = re.search(r"```[ \t]*([^\r\n`]*)\r?\n([\s\S]*?)\r?\n?```", s)
    if fenced:
        s = fenced.group(2).strip()
    else:
        # Handle partially fenced responses: strip stray fences if present.
        if s.startswith("```"):
            s = re.sub(r"^```[ \t]*[^\n]*\n?", "", s).strip()
        if s.endswith("```"):
            s = re.sub(r"\n?```$", "", s).strip()

    # 2) Remove a leading language label line like:
    # python\n<code>  OR  JavaScript\r\n<code>  OR  c++\n<code>
    # Only remove if it matches a known language identifier to avoid deleting real code.
    first_line, sep, rest = s.partition("\n")
    if sep:
        fl = first_line.strip().lower()
        known_lang_labels = {
            # Python
            "python", "py",
            # JS/TS
            "javascript", "js", "node", "nodejs", "typescript", "ts",
            # JVM
            "java", "kotlin", "scala",
            # Systems
            "c", "c++", "cpp", "cplusplus", "cc", "cxx", "h", "hpp",
            "rust", "rs",
            "go", "golang",
            "c#", "csharp", "dotnet",
            # Scripting
            "php", "ruby", "rb", "perl", "pl", "r",
            "bash", "sh", "shell",
            "powershell", "ps", "ps1",
            "swift",
        }

        # Also accept "language: <x>" / "lang: <x>"
        lang_prefix = re.match(r"^(language|lang)\s*:\s*([a-z0-9#+.\-]+)\s*$", fl)
        if fl in known_lang_labels:
            s = rest.lstrip()
        elif lang_prefix and lang_prefix.group(2) in known_lang_labels:
            s = rest.lstrip()

    return s.strip()
