# acmp/agents/optimizer.py
import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from ..utils.helper import extract_code_block
from langchain_groq import ChatGroq
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    # api_key= os.getenv("GROQ_API_KEY")
)


# llm = HuggingFaceEndpoint(
#     repo_id="meta-llama/Llama-3.1-8B-Instruct",
#     task="text-generation",
#     # temperature=0,
#     # max_new_tokens=1024,
#     huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# )
# model=ChatHuggingFace(llm=llm)


def optimizer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fixes failing code using error logs.
    Increments retry counter.
    """

    if not state.get("error_logs"):
        return state

    language = state.get("language", "python")
    language_version = state.get("language_version") or "latest"
    framework = state.get("framework") or None
    framework_version = state.get("framework_version") or None

    version_info = f"Target: {language}"
    if language_version:
        version_info += f" {language_version}"
    if framework and framework.lower() != "none":
        version_info += f" with {framework}"
        if framework_version:
            version_info += f" {framework_version}"

    prompt = f"""
You are a debugging expert.

Target Language and Framework: {version_info}

The following code failed with this error:

ERROR:
{state["error_logs"]}

- Fix the issue causing the error.
- Preserve original logic and functionality.
- Do NOT change behavior.
- Fix legacy syntax and replace deprecated APIs/functions with their modern equivalents for {version_info}.
- Apply modernization improvements compatible with the specified versions.
- Output ONLY valid executable code for {version_info}.
- Do NOT add explanations.
- Do NOT wrap in markdown.
- Do not provide language labels.

Failing Code:
{state["current_code"]}
"""

    response = llm.invoke(prompt)
    # print(f"OPTIMIZER {state['itr']}\n", response.content.strip())
    state["current_code"] = extract_code_block(response.content.strip())
    state["itr"] += 1

    return state
