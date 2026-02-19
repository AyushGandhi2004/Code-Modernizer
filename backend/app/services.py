import json
import asyncio
from typing import AsyncGenerator, cast
from acmp.graph import graph
from acmp.state import AgentState

async def run_modernization_stream(file_name: str, code: str, language: str, framework:str) -> AsyncGenerator[str, None]:
    """Streams graph updates for a single uploaded file string."""
    
    # Initial state using the code provided by the frontend
    state: AgentState = {
        "file_path": file_name,
        "original_code": code,
        "language" : language,
        "framework" : framework,
        "language_version": None,
        "framework_version": None,
        "transformation_plan": None,
        "current_code": None,
        "error_logs": None,
        "itr": 0,
    }

    try:
        # Stream node updates using LangGraph
        async for chunk in graph.astream(cast(AgentState, state), stream_mode="updates"):
            # print("UPDATE : \n",chunk)
            for node_name, node_data in chunk.items():
                payload = {
                    "node": node_name,
                    "file_path": file_name,
                    "current_code": node_data.get("current_code"),
                    "error_logs": node_data.get("error_logs"),
                    "original_code": code if node_name == "auditor" else None,
                    "language": node_data.get("language", language),
                    "language_version": node_data.get("language_version"),
                    "framework": node_data.get("framework", framework),
                    "framework_version": node_data.get("framework_version")
                }
                yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.sleep(0.1)
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"