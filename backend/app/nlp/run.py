from antlr4 import *

from CompiledFiles.CaloriesAssistantLexer import CaloriesAssistantLexer
from CompiledFiles.CaloriesAssistantParser import CaloriesAssistantParser
from semantic_visitor import SemanticVisitor


def parse_and_print(input_text: str):
    input_stream = InputStream(input_text)

    lexer = CaloriesAssistantLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CaloriesAssistantParser(token_stream)

    tree = parser.program()

    print("=== PARSE TREE ===")
    print(tree.toStringTree(recog=parser))

    visitor = SemanticVisitor()
    frames = visitor.visit(tree)

    print("=== SEMANTIC OUTPUT ===")
    print(frames)


if __name__ == "__main__":
    print("Type ONE command per line. Type 'exit' to quit.")

    while True:
        s = input("> ").strip()
        if s.lower() in ("exit", "quit"):
            break
        if not s:
            continue

        # parse as a one-line program
        parse_and_print(s)
        print()
