from pydantic import BaseModel
from typing import Optional

class ModernizeRequest(BaseModel):
    file_name: str
    code: str  # The raw source code from the frontend
    language : str
    framework : Optional[str] = "None"

class SaveRequest(BaseModel):
    file_path: str
    code: str