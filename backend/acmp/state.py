from typing import Any, TypedDict, Optional, List
from pydantic import BaseModel

class LegacyPattern(BaseModel):
    pattern: str
    recommended_fix: str


# class SecurityIssue(BaseModel):
#     issue: str
#     severity: str  # low | medium | high


class TransformationPlan(BaseModel):
    # Target language and framework details for the modernized code
    language: str
    language_version: Optional[str] = None
    framework: Optional[str] = None
    framework_version: Optional[str] = None

    legacy_patterns: List[LegacyPattern]
    # security_issues: List[SecurityIssue]
    modernization_steps: List[str]

class AgentState(TypedDict):
    """
    Shared state that flows through the LangGraph pipeline.
    All agent reads from and writes to this state.
    """
    #file data:
    file_path : str
    original_code : str
    language : str
    framework : Optional[str]
    # Selected target versions used for modernization
    language_version: Optional[str]
    framework_version: Optional[str]

    #auditor_output:
    transformation_plan : Optional[TransformationPlan]

    #Drafted new code:
    current_code : Optional[str]

    #error logs :
    error_logs : Optional[str]

    #iterations:
    itr : int

    #final flag:
    # is_valid : bool