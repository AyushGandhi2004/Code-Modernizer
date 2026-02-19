# acmp/agents/engineer.py
import os
from typing import Dict, Any
import json

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


def engineer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Refactors legacy code into modern, secure, optimized version
    using the TransformationPlan.
    """

    transformation_plan = state["transformation_plan"]

    # Convert structured plan to JSON string for prompt clarity
    plan_json = json.dumps(transformation_plan.model_dump(), indent=2)

    language = state.get("language", "python")
    language_version = state.get("language_version") or transformation_plan.language_version or "latest"
    framework = state.get("framework") or transformation_plan.framework
    framework_version = state.get("framework_version") or transformation_plan.framework_version

    version_info = f"Target: {language}"
    if language_version:
        version_info += f" {language_version}"
    if framework and framework.lower() != "none":
        version_info += f" with {framework}"
        if framework_version:
            version_info += f" {framework_version}"

    prompt = f"""
You are a senior software engineer modernizing legacy code.

Target Language and Framework: {version_info}

Follow this transformation plan strictly:

{plan_json}

Rules:
- Preserve original logic and functionality of the complete code.
- Do NOT change behavior.
- Fix legacy syntax and replace deprecated APIs/functions with their modern equivalents for {version_info}.
- Apply modernization improvements compatible with the specified versions.
- Output ONLY valid executable code for {version_info}.
- Do NOT add explanations.
- Do NOT wrap in markdown.
- Do not provide language labels.
- Just provide the new code and no other extra things, not even a single word.

Original Code:
{state["original_code"]}
"""

    response = llm.invoke(prompt)
    # print(f"ENGINEER {state['itr']}: \n", extract_code_block(response.content.strip()))
    state["current_code"] = extract_code_block(response.content.strip())

    return state
