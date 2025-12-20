from antlr4 import *
from datetime import date
import sys
from pathlib import Path

# Add backend to path so imports work
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.nlp.CompiledFiles.CaloriesAssistantLexer import CaloriesAssistantLexer
from app.nlp.CompiledFiles.CaloriesAssistantParser import CaloriesAssistantParser
from app.nlp.semantic_visitor import SemanticVisitor
from app.nlp.intent_router import route_frame


def parse_and_print(input_text: str, context: dict):
    input_stream = InputStream(input_text)

    lexer = CaloriesAssistantLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CaloriesAssistantParser(token_stream)

    tree = parser.program()

    print("=== PARSE TREE ===")
    print(tree.toStringTree(recog=parser))

    visitor = SemanticVisitor()
    frames = visitor.visit(tree)

    print("\n=== SEMANTIC OUTPUT ===")
    print(frames)
    
    # NEW: Call handlers
    print("\n=== HANDLER RESULTS ===")
    for i, frame in enumerate(frames, 1):
        result = route_frame(frame, repo=None, context=context)
        print(f"{i}. {result.get('message')}")
        if result.get('result'):
            print(f"   Details: {result.get('result')}")
    
    # Show current context state
    if context.get('exercise_entries'):
        print(f"\n=== STORED ENTRIES ({len(context['exercise_entries'])}) ===")
        for entry in context['exercise_entries']:
            print(f"  - {entry['entry_id']}: {entry['items']}")


if __name__ == "__main__":
    print("Exercise Handler Test REPL")
    print("Type ONE command per line. Type 'exit' to quit.")
    print("\nExamples:")
    print('  exercise: run 30min, do 20 pushups')
    print('  edit ex_001: exercise: run 45min')
    print('  add ex_001: do 30 squats')
    print('  delete ex_001')
    print()
    
    # Create persistent context
    context = {
        "user_id": "test_user",
        "date": date.today()
    }

    while True:
        s = input("> ").strip()
        if s.lower() in ("exit", "quit"):
            break
        if not s:
            continue

        # parse as a one-line program
        try:
            parse_and_print(s, context)
        except Exception as e:
            print(f"Error: {e}")
        print()
