from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models import ModernizeRequest
from services import run_modernization_stream

router = APIRouter()

@router.post("/modernize")
async def modernize_code(request: ModernizeRequest):
    # We pass file_name and code directly to the service
    return StreamingResponse(
        run_modernization_stream(request.file_name, request.code, request.language, request.framework),
        media_type="text/event-stream"
    )