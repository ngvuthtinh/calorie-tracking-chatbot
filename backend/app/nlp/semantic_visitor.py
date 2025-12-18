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
    # EXERCISE visitors
    # ==========================

    # exerciseCommandTop : exerciseLog | exerciseEdit | exerciseAddToEntry | exerciseDelete | undoCommand ;
    def visitExerciseCommandTop(self, ctx) -> Dict[str, Any]:
        if ctx.exerciseLog():
            return self.visit(ctx.exerciseLog())
        if ctx.exerciseEdit():
            return self.visit(ctx.exerciseEdit())
        if ctx.exerciseAddToEntry():
            return self.visit(ctx.exerciseAddToEntry())
        if ctx.exerciseDelete():
            return self.visit(ctx.exerciseDelete())
        if ctx.undoCommand():
            return self.visit(ctx.undoCommand())
        return {"intent": "unknown", "data": {}}

    # exerciseLog : EXERCISE COLON exerciseItems ;
    def visitExerciseLog(self, ctx) -> Dict[str, Any]:
        items = self.visit(ctx.exerciseItems())
        return {"intent": "log_exercise", "data": {"items": items}}

    # exerciseEdit : EDIT exerciseEntryId COLON EXERCISE COLON exerciseItems ;
    def visitExerciseEdit(self, ctx) -> Dict[str, Any]:
        entry_id = ctx.exerciseEntryId().getText()
        items = self.visit(ctx.exerciseItems())
        return {
            "intent": "edit_exercise_entry",
            "data": {"entry_id": entry_id, "items": items},
        }

    # exerciseAddToEntry : ADD exerciseEntryId COLON exerciseItems ;
    def visitExerciseAddToEntry(self, ctx) -> Dict[str, Any]:
        entry_id = ctx.exerciseEntryId().getText()
        items = self.visit(ctx.exerciseItems())
        return {
            "intent": "add_exercise_items",
            "data": {"entry_id": entry_id, "items": items},
        }

    # exerciseDelete : DELETE exerciseEntryId ;
    def visitExerciseDelete(self, ctx) -> Dict[str, Any]:
        entry_id = ctx.exerciseEntryId().getText()
        return {"intent": "delete_exercise_entry", "data": {"entry_id": entry_id}}

    # exerciseItems : exerciseItem (COMMA exerciseItem)* ;
    def visitExerciseItems(self, ctx) -> List[Dict[str, Any]]:
        items = []
        for item_ctx in ctx.exerciseItem():
            item = self.visit(item_ctx)
            items.append(item)
        return items

    # exerciseItem : runItem | walkItem | cyclingItem | swimItem | plankItem | doItem ;
    def visitExerciseItem(self, ctx) -> Dict[str, Any]:
        if ctx.runItem():
            return self.visit(ctx.runItem())
        if ctx.walkItem():
            return self.visit(ctx.walkItem())
        if ctx.cyclingItem():
            return self.visit(ctx.cyclingItem())
        if ctx.swimItem():
            return self.visit(ctx.swimItem())
        if ctx.plankItem():
            return self.visit(ctx.plankItem())
        if ctx.doItem():
            return self.visit(ctx.doItem())
        return {"type": "unknown"}

    # runItem : RUN (duration | distance) ;
    def visitRunItem(self, ctx) -> Dict[str, Any]:
        result = {"type": "run"}
        if ctx.duration():
            result["duration_min"] = self.visit(ctx.duration())
        elif ctx.distance():
            result["distance_km"] = self.visit(ctx.distance())
        return result

    # walkItem : WALK (duration | distance) ;
    def visitWalkItem(self, ctx) -> Dict[str, Any]:
        result = {"type": "walk"}
        if ctx.duration():
            result["duration_min"] = self.visit(ctx.duration())
        elif ctx.distance():
            result["distance_km"] = self.visit(ctx.distance())
        return result

    # cyclingItem : CYCLING (duration | distance) ;
    def visitCyclingItem(self, ctx) -> Dict[str, Any]:
        result = {"type": "cycling"}
        if ctx.duration():
            result["duration_min"] = self.visit(ctx.duration())
        elif ctx.distance():
            result["distance_km"] = self.visit(ctx.distance())
        return result

    # swimItem : SWIM duration ;
    def visitSwimItem(self, ctx) -> Dict[str, Any]:
        duration_min = self.visit(ctx.duration())
        return {"type": "swim", "duration_min": duration_min}

    # plankItem : PLANK duration ;
    def visitPlankItem(self, ctx) -> Dict[str, Any]:
        duration_min = self.visit(ctx.duration())
        return {"type": "plank", "duration_min": duration_min}

    # doItem : DO countableExercise ;
    def visitDoItem(self, ctx) -> Dict[str, Any]:
        return self.visit(ctx.countableExercise())

    # duration : INT MIN ;
    def visitDuration(self, ctx) -> int:
        return int(ctx.INT().getText())

    # distance : INT KM ;
    def visitDistance(self, ctx) -> int:
        return int(ctx.INT().getText())

    # countableExercise : INT PUSHUPS | INT SQUATS | INT LUNGES ;
    def visitCountableExercise(self, ctx) -> Dict[str, Any]:
        reps = int(ctx.INT().getText())
        
        if ctx.PUSHUPS():
            exercise_type = "pushups"
        elif ctx.SQUATS():
            exercise_type = "squats"
        elif ctx.LUNGES():
            exercise_type = "lunges"
        else:
            exercise_type = "unknown"
        
        return {"type": exercise_type, "reps": reps}

    # ==========================
    # TODO: Member 3 implements STATS + PROFILE + UNDO visitors
    #   - visitStatsCommand, visitProfileCommand, visitUndoCommand, ...
    # ==========================

    # STATS visitors
    def visitStatsCommand(self, ctx) -> Dict[str, Any]:
        if ctx.summaryToday():
            return self.visit(ctx.summaryToday())
        if ctx.summaryDate():
            return self.visit(ctx.summaryDate())
        if ctx.weeklyStats():
            return {"intent": "show_weekly_stats", "data": {}}
        if ctx.statsThisWeek():
            return {"intent": "show_stats_this_week", "data": {}}
        return {"intent": "unknown_stats", "data": {}}

    def visitSummaryToday(self, ctx) -> Dict[str, Any]:
        return {"intent": "show_summary_today", "data": {}}
    
    def visitSummaryDate(self, ctx) -> Dict[str, Any]:
        date_str = ctx.DATE().getText()
        return {"intent": "show_summary_date", "data": {"date": date_str}}

    # PROFILE visitors
    def visitProfileCommand(self, ctx) -> Dict[str, Any]:
        if ctx.setWeight():
            return self.visit(ctx.setWeight())
        if ctx.setHeight():
            return self.visit(ctx.setHeight())
        if ctx.setGoal():
            return self.visit(ctx.setGoal())
        if ctx.setActivity():
            return self.visit(ctx.setActivity())
        return {"intent": "update_profile", "data": {}}

    def visitSetWeight(self, ctx) -> Dict[str, Any]:
        value = int(ctx.INT().getText())
        return {"intent": "update_profile", "data": {"field": "weight", "value": value, "unit": "kg"}}

    def visitSetHeight(self, ctx) -> Dict[str, Any]:
        value = int(ctx.INT().getText())
        return {"intent": "update_profile", "data": {"field": "height", "value": value, "unit": "cm"}}

    def visitSetGoal(self, ctx) -> Dict[str, Any]:
        goal = ctx.GOAL_TYPE().getText().lower()
        return {"intent": "update_profile", "data": {"field": "goal", "value": goal}}

    def visitSetActivity(self, ctx) -> Dict[str, Any]:
        level = ctx.ACTIVITY_LEVEL().getText().lower()
        return {"intent": "update_profile", "data": {"field": "activity_level", "value": level}}

    # UNDO visitor
