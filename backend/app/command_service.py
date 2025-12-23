from datetime import date
from typing import Any, Dict, List, Optional

from app.nlp.nlp_facade import NlpFacade, NlpSyntaxError
# Note: intent_router and handlers must be implemented for this to work fully.
# If handlers are missing, this import might fail at runtime.
try:
    from app.nlp.intent_router import route_frame
except ImportError:
    # Fallback/Mock for development if dependencies are missing
    def route_frame(frame, context):
        return {"status": "mock_routed", "intent": frame.get("intent")}

class CommandService:
    def __init__(self):
        """
        Initialize the command service.
        """
        pass

    def handle_command(self, user_id: str, entry_date: date, text: str) -> Dict[str, Any]:
        """
        Main entry point for the backend logic.
        Parses the text and routes each command frame to the appropriate handler.
        """
        # 1. Parse
        try:
            frames = NlpFacade.parse(text)
        except NlpSyntaxError as e:
            return {
                "success": False,
                "error": str(e),
                "frames": [],
                "results": []
            }
        except Exception as e:
             return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "frames": [],
                "results": []
            }
        
        if not frames:
             # Empty input matches behavior of NlpFacade returning []
             return {
                 "success": True, 
                 "frames": [], 
                 "results": []
             }

        # 2. Route & Execute
        results = []
        context = {
            "user_id": user_id,
            "date": entry_date
        }

        for frame in frames:
            try:
                # route_frame expects (frame, context)
                res = route_frame(frame, context)
                results.append(res)
            except Exception as e:
                # Capture error for this specific frame but verify others if possible?
                # For now, append error to results
                results.append({
                    "error": str(e),
                    "intent": frame.get("intent")
                })

        # 3. Return structured response
        return {
            "success": True,
            "frames": frames,
            "results": results
        }
