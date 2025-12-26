from fastapi import APIRouter, HTTPException
from backend.app.schemas.chat_schema import ChatRequest, ChatActionResponse
from backend.app.command_service import CommandService
from backend.app.nlp.nlp_facade import NlpSyntaxError
from datetime import datetime, date
from typing import List, Dict, Any

router = APIRouter()
command_service = CommandService()


# --- Endpoint ---
@router.post("/", response_model=ChatActionResponse)
async def chat_endpoint(request: ChatRequest) -> ChatActionResponse:
    """
    Main chatbot endpoint - the "Brain" of the application.
    
    Receives user text, parses semantics via NLP, routes to the correct handler
    (Food Log, Exercise, Stats/Profile), and returns a structured response with
    suggested action chips.
    
    Strict Contract:
    - Input: user_id, entry_date (YYYY-MM-DD), text
    - Output: success, message, data, actions (list of ActionChips)
    
    Args:
        request: ChatRequest with user_id, entry_date, and text
        
    Returns:
        ChatActionResponse with success status, message, data, and action chips
    """
    
    
    # 1. Process command via CommandService (Xử lý lệnh)
    try:
        # request.entry_date đã được validate và convert sang date object bởi Schema
        result = command_service.handle_command(
            user_id=str(request.user_id),
            entry_date=request.entry_date,
            text=request.text
        )
        
        # 2. Handle errors (Xử lý lỗi)
        if not result.get("success", False):
            error_msg = result.get("error", "Failed to process your request.")
            
            # Syntax error (Lỗi cú pháp câu lệnh)
            if "syntax" in error_msg.lower() or "error at line" in error_msg.lower():
                user_message = "I didn't understand that. Please try rephrasing your request."
            else:
                user_message = error_msg
            
            return ChatActionResponse(
                success=False,
                message=user_message,
                data={"error": error_msg}
            )
        
        # 3. Extract results (Lấy kết quả xử lý)
        frames = result.get("frames", [])
        results = result.get("results", [])
        
        if not frames or not results:
            return ChatActionResponse(
                success=True,
                message="No action detected. How can I help you?",
                data=None
            )
        
        # 4. Generate response (Tạo phản hồi JSON)
        return _build_response(frames, results)
    
    except NlpSyntaxError as e:
        return ChatActionResponse(
            success=False,
            message="I didn't understand that. Please try rephrasing your request.",
            data={"error": str(e)}
        )
    
    except Exception as e:
        return ChatActionResponse(
            success=False,
            message="An unexpected error occurred. Please try again.",
            data={"error": str(e)}
        )


def _build_response(frames: List[Dict[str, Any]], results: List[Dict[str, Any]]) -> ChatActionResponse:
    """
    Helper function to build JSON response.
    Hàm phụ trợ để đóng gói dữ liệu trả về theo format chuẩn.
    """
    # Case 1: Single Intent (Chỉ có 1 ý định)
    if len(frames) == 1:
        frame = frames[0]
        res = results[0]
        intent = frame.get("intent", "")
        
        # Check success status
        handler_success = res.get("success", False)
        handler_message = res.get("message", "Action completed.")
        handler_result = res.get("result", None)
        
        return ChatActionResponse(
            success=handler_success,
            message=handler_message,
            data={
                "intent": intent,
                "result": handler_result,
                "frame": frame
            },
            frame=frame
        )
    
    # Case 2: Multiple Intents (Có nhiều ý định trong 1 câu)
    else:
        intents = [f.get("intent", "") for f in frames]
        all_success = all(r.get("success", False) for r in results)
        
        # Combine messages (Gộp các thông báo lại)
        messages = [r.get("message", "") for r in results if r.get("message")]
        combined_message = " ".join(messages) if messages else "Multiple actions completed."
        
        return ChatActionResponse(
            success=all_success,
            message=combined_message,
            data={
                "intents": intents,
                "results": results,
                "frames": frames
            },
            frame=frames[0] if frames else None
        )

