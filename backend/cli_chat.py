import sys
import os
import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend.app.command_service import CommandService
    from backend.app.repositories.users_repo import get_or_create_user
    from backend.app.repositories.day_session_repo import get_or_create_day_session
    from backend.app.db.connection import get_connection
except ImportError:
    # Fallback if running from root directory
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
    from backend.app.command_service import CommandService
    from backend.app.repositories.users_repo import get_or_create_user
    from backend.app.repositories.day_session_repo import get_or_create_day_session
    from backend.app.db.connection import get_connection

def main():
    print("="*50)
    print("Calorie Tracking Chatbot - CLI Test Interface")
    print("="*50)
    print("Type 'exit' or 'quit' to stop.")
    print("Type your command (e.g., 'eta: 2 eggs', 'exercise: run 30 min').")
    print("-" * 50)

    # 1. Setup default user and session for testing
    user_email = "cli_tester@example.com"
    try:
        user_id = get_or_create_user(user_email)
        print(f"[Info] Logged in as: {user_email} (ID: {user_id})")
    except Exception as e:
        print(f"[Error] Database connection failed: {e}")
        print("Please check your .env file and ensure the database is running.")
        return

    # Default to today
    current_date = datetime.date.today()
    print(f"[Info] Date set to: {current_date}")

    # Ensure session exists
    try:
        session_id = get_or_create_day_session(user_id, str(current_date))
        print(f"[Info] Session ID: {session_id}")
    except Exception as e:
        print(f"[Error] Failed to create session: {e}")
        return

    # Service initialization (No repo needed, handlers use direct imports)
    service = CommandService()

    while True:
        try:
            user_input = input("\n> ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue

            # Process command
            response = service.handle_command(user_id, current_date, user_input)
            
            if response.get("success"):
                print("Bot Response:")
                results = response.get("results", [])
                if not results:
                    print("  (No action taken or empty result)")
                for res in results:
                    print(f"  - {res}")
            else:
                print(f"Error: {response.get('error')}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Runtime Error: {e}")

if __name__ == "__main__":
    main()
