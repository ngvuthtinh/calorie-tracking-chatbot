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
    # FOOD visitors
    # ==========================

    # foodCommand
    #   : foodLog
    #   | foodEdit
    #   | foodAddToEntry
    #   | foodMove
    #   | foodDelete
    #   | undoCommand
    #   ;
    def visitFoodCommand(self, ctx) -> Dict[str, Any]:
        if ctx.foodLog():
            return self.visit(ctx.foodLog())
        if ctx.foodEdit():
            return self.visit(ctx.foodEdit())
        if ctx.foodAddToEntry():
            return self.visit(ctx.foodAddToEntry())
        if ctx.foodMove():
            return self.visit(ctx.foodMove())
        if ctx.foodDelete():
            return self.visit(ctx.foodDelete())

        # If it's undoCommand, Member 3 will handle it; return a safe fallback
        if ctx.undoCommand():
            return self.visit(ctx.undoCommand())

        return {"intent": "unknown_food", "data": {"reason": "unmatched food command"}}

    # foodLog : foodLogBody ;
    def visitFoodLog(self, ctx) -> Dict[str, Any]:
        body = self.visit(ctx.foodLogBody())
        return {
            "intent": "log_food",
            "data": body
        }

    # foodLogBody : mealLabel? actionLabel? COLON foodItems ;
    def visitFoodLogBody(self, ctx) -> Dict[str, Any]:
        meal = self.visit(ctx.mealLabel()) if ctx.mealLabel() else None
        action = self.visit(ctx.actionLabel()) if ctx.actionLabel() else None
        items = self.visit(ctx.foodItems())
        out: Dict[str, Any] = {"items": items}
        if meal is not None:
            out["meal"] = meal
        if action is not None:
            out["action"] = action
        return out

    # foodItems : foodItem (COMMA foodItem)* ;
    def visitFoodItems(self, ctx) -> List[Dict[str, Any]]:
        return [self.visit(fi) for fi in ctx.foodItem()]

    # foodItem : quantity? foodName note? ;
    def visitFoodItem(self, ctx) -> Dict[str, Any]:
        item: Dict[str, Any] = {}

        if ctx.quantity():
            q = self.visit(ctx.quantity())  # {"qty": int, "unit": Optional[str]}
            item.update(q)

        name = self.visit(ctx.foodName())  # string
        item["name"] = name

        if ctx.note():
            note_text = self.visit(ctx.note())  # string (no parentheses)
            item["note"] = note_text

        return item

    # quantity : INT unit? ;
    def visitQuantity(self, ctx) -> Dict[str, Any]:
        qty = int(ctx.INT().getText())
        out: Dict[str, Any] = {"qty": qty}
        if ctx.unit():
            out["unit"] = self.visit(ctx.unit())
        return out

    # unit : UNIT ;
    def visitUnit(self, ctx) -> str:
        # Keep it normalized to lowercase for consistent downstream handling
        return ctx.UNIT().getText().lower()

    # foodName : nameAtom (nameAtom)* ;
    def visitFoodName(self, ctx) -> str:
        # nameAtom is WORD or STRING; join with spaces to preserve multi-word names
        atoms = [self.visit(a) for a in ctx.nameAtom()]
        # Ensure clean spacing; do NOT use .split()
        return " ".join(atoms).strip()

    # nameAtom : WORD | STRING ;
    def visitNameAtom(self, ctx) -> str:
        if ctx.WORD():
            return ctx.WORD().getText()
        # STRING includes quotes; strip them
        if ctx.STRING():
            s = ctx.STRING().getText()
            if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
                return s[1:-1]
            return s
        return ""

    # note : LPAREN noteText RPAREN ;
    def visitNote(self, ctx) -> str:
        # noteText is a sequence of tokens; use getText then normalize separators lightly
        # NOTE: getText() removes WS because WS is skipped. We'll re-insert single spaces
        # between tokens based on children to keep it readable, without split().
        parts: List[str] = []
        for ch in ctx.noteText().children or []:
            t = ch.getText()
            parts.append(t)
        # This yields something like ['small'] or ['low', '-', 'sugar'] etc.
        # We'll join by space, then fix common punctuation spacing.
        raw = " ".join(parts).strip()
        raw = raw.replace(" - ", "-").replace(" / ", "/").replace(" . ", ".")
        return raw

    # mealLabel : BREAKFAST | LUNCH | DINNER | SNACK ;
    def visitMealLabel(self, ctx) -> str:
        # Return normalized lowercase meal name
        return ctx.getText().lower()

    # actionLabel : EAT | DRINK ;
    def visitActionLabel(self, ctx) -> str:
        return ctx.getText().lower()

    # foodEdit : EDIT foodEntryId COLON foodLogBody ;
    def visitFoodEdit(self, ctx) -> Dict[str, Any]:
        entry_id = ctx.foodEntryId().getText()
        body = self.visit(ctx.foodLogBody())
        return {
            "intent": "edit_food_entry",
            "data": {
                "entry_id": entry_id,
                **body
            }
        }

    # foodAddToEntry : ADD foodEntryId COLON foodItems ;
    def visitFoodAddToEntry(self, ctx) -> Dict[str, Any]:
        entry_id = ctx.foodEntryId().getText()
        items = self.visit(ctx.foodItems())
        return {
            "intent": "add_food_items",
            "data": {
                "entry_id": entry_id,
                "items": items
            }
        }

    # foodMove : MOVE foodEntryId TO mealLabel ;
    def visitFoodMove(self, ctx) -> Dict[str, Any]:
        entry_id = ctx.foodEntryId().getText()
        meal = self.visit(ctx.mealLabel())
        return {
            "intent": "move_food_entry",
            "data": {
                "entry_id": entry_id,
                "meal": meal
            }
        }

    # foodDelete : DELETE foodEntryId ;
    def visitFoodDelete(self, ctx) -> Dict[str, Any]:
        entry_id = ctx.foodEntryId().getText()
        return {
            "intent": "delete_food_entry",
            "data": {
                "entry_id": entry_id
            }
        }

    # ==========================
    # TODO: Member 2 implements EXERCISE visitors
    #   - visitExerciseCommandTop, visitExerciseLog, ...
    # ==========================

    # ==========================
    # TODO: Member 3 implements STATS + PROFILE + UNDO visitors
    #   - visitStatsCommand, visitProfileCommand, visitUndoCommand, ...
    # ==========================
