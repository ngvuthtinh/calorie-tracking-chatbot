from typing import List, Dict, Any
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from app.nlp.CompiledFiles.CaloriesAssistantLexer import CaloriesAssistantLexer
from app.nlp.CompiledFiles.CaloriesAssistantParser import CaloriesAssistantParser
from app.nlp.semantic_visitor import SemanticVisitor

class NlpSyntaxError(Exception):
    """Raised when the input text violates the grammar."""
    pass

class ThrowingErrorListener(ErrorListener):
    """
    Custom error listener that raises an exception on syntax errors
    instead of printing to stderr.
    """
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Format a clean error message
        raise NlpSyntaxError(f"Error at line {line}:{column}: {msg}")

class NlpFacade:
    @staticmethod
    def parse(text: str) -> List[Dict[str, Any]]:
        """
        Parses the input text and returns a list of semantic frames.
        Raises NlpSyntaxError if the syntax is invalid.
        """
        if not text or not text.strip():
            return []

        # 1. Setup Input & Lexer
        input_stream = InputStream(text)
        lexer = CaloriesAssistantLexer(input_stream)
        
        # Remove default console listener, add our throwing listener
        lexer.removeErrorListeners()
        lexer.addErrorListener(ThrowingErrorListener())

        # 2. Setup Tokens & Parser
        token_stream = CommonTokenStream(lexer)
        parser = CaloriesAssistantParser(token_stream)
        
        parser.removeErrorListeners()
        parser.addErrorListener(ThrowingErrorListener())

        # 3. Parse (this will trigger syntaxError if invalid)
        try:
            tree = parser.program()
        except NlpSyntaxError:
            raise
        except Exception as e:
            raise NlpSyntaxError(f"Unexpected parsing error: {e}")

        # 4. Visit tree to build semantic frames
        visitor = SemanticVisitor()
        frames = visitor.visit(tree)
        
        # Ensure we return a list
        return frames if frames is not None else []
