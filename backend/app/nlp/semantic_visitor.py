from typing import Any, Dict, List, Optional

from CompiledFiles.CaloriesAssistantVisitor import CaloriesAssistantVisitor


class SemanticVisitor(CaloriesAssistantVisitor):
    """
    Skeleton Semantic Visitor for CalorieAssistant.g4

    Output rule (semantic contract):
      Each command returns:
        {"intent": "<string>", "data": {...}}

    program() returns: List[frame]
    """

    # program : line* EOF ;
    def visitProgram(self, ctx) -> List[Dict[str, Any]]:
        frames: List[Dict[str, Any]] = []
        for ln in ctx.line():
            out = self.visit(ln)
            if out is None:
                continue
            # line may return one frame
            frames.append(out)
        return frames

    # line : command (NEWLINE+ | EOF) | NEWLINE+ ;
    def visitLine(self, ctx) -> Optional[Dict[str, Any]]:
        if ctx.command() is None:
            return None
        return self.visit(ctx.command())

    # command : foodCommand | exerciseCommandTop | statsCommand | profileCommand ;
    def visitCommand(self, ctx) -> Dict[str, Any]:
        if ctx.foodCommand():
            return self.visit(ctx.foodCommand())
        if ctx.exerciseCommandTop():
            return self.visit(ctx.exerciseCommandTop())
        if ctx.statsCommand():
            return self.visit(ctx.statsCommand())
        if ctx.profileCommand():
            return self.visit(ctx.profileCommand())

        # Should not happen if grammar is correct
        return {"intent": "unknown", "data": {"reason": "unmatched command"}}

    # ==========================
    # TODO: Member 1 implements FOOD visitors
    #   - visitFoodCommand, visitFoodLog, visitFoodLogBody, ...
    # ==========================

    # ==========================
    # TODO: Member 2 implements EXERCISE visitors
    #   - visitExerciseCommandTop, visitExerciseLog, ...
    # ==========================

    # ==========================
    # TODO: Member 3 implements STATS + PROFILE + UNDO visitors
    #   - visitStatsCommand, visitProfileCommand, visitUndoCommand, ...
    # ==========================
