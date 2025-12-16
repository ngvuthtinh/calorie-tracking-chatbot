# Generated from CaloriesAssistant.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CaloriesAssistantParser import CaloriesAssistantParser
else:
    from CaloriesAssistantParser import CaloriesAssistantParser

# This class defines a complete generic visitor for a parse tree produced by CaloriesAssistantParser.

class CaloriesAssistantVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CaloriesAssistantParser#program.
    def visitProgram(self, ctx:CaloriesAssistantParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#line.
    def visitLine(self, ctx:CaloriesAssistantParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#command.
    def visitCommand(self, ctx:CaloriesAssistantParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodCommand.
    def visitFoodCommand(self, ctx:CaloriesAssistantParser.FoodCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodLog.
    def visitFoodLog(self, ctx:CaloriesAssistantParser.FoodLogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodLogBody.
    def visitFoodLogBody(self, ctx:CaloriesAssistantParser.FoodLogBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodEdit.
    def visitFoodEdit(self, ctx:CaloriesAssistantParser.FoodEditContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodAddToEntry.
    def visitFoodAddToEntry(self, ctx:CaloriesAssistantParser.FoodAddToEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodMove.
    def visitFoodMove(self, ctx:CaloriesAssistantParser.FoodMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodDelete.
    def visitFoodDelete(self, ctx:CaloriesAssistantParser.FoodDeleteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodEntryId.
    def visitFoodEntryId(self, ctx:CaloriesAssistantParser.FoodEntryIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodItems.
    def visitFoodItems(self, ctx:CaloriesAssistantParser.FoodItemsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodItem.
    def visitFoodItem(self, ctx:CaloriesAssistantParser.FoodItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#quantity.
    def visitQuantity(self, ctx:CaloriesAssistantParser.QuantityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#unit.
    def visitUnit(self, ctx:CaloriesAssistantParser.UnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#foodName.
    def visitFoodName(self, ctx:CaloriesAssistantParser.FoodNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#nameAtom.
    def visitNameAtom(self, ctx:CaloriesAssistantParser.NameAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#note.
    def visitNote(self, ctx:CaloriesAssistantParser.NoteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#noteText.
    def visitNoteText(self, ctx:CaloriesAssistantParser.NoteTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#mealLabel.
    def visitMealLabel(self, ctx:CaloriesAssistantParser.MealLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#actionLabel.
    def visitActionLabel(self, ctx:CaloriesAssistantParser.ActionLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseCommandTop.
    def visitExerciseCommandTop(self, ctx:CaloriesAssistantParser.ExerciseCommandTopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseLog.
    def visitExerciseLog(self, ctx:CaloriesAssistantParser.ExerciseLogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseEdit.
    def visitExerciseEdit(self, ctx:CaloriesAssistantParser.ExerciseEditContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseAddToEntry.
    def visitExerciseAddToEntry(self, ctx:CaloriesAssistantParser.ExerciseAddToEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseDelete.
    def visitExerciseDelete(self, ctx:CaloriesAssistantParser.ExerciseDeleteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseEntryId.
    def visitExerciseEntryId(self, ctx:CaloriesAssistantParser.ExerciseEntryIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseItems.
    def visitExerciseItems(self, ctx:CaloriesAssistantParser.ExerciseItemsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#exerciseItem.
    def visitExerciseItem(self, ctx:CaloriesAssistantParser.ExerciseItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#runItem.
    def visitRunItem(self, ctx:CaloriesAssistantParser.RunItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#walkItem.
    def visitWalkItem(self, ctx:CaloriesAssistantParser.WalkItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#cyclingItem.
    def visitCyclingItem(self, ctx:CaloriesAssistantParser.CyclingItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#swimItem.
    def visitSwimItem(self, ctx:CaloriesAssistantParser.SwimItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#plankItem.
    def visitPlankItem(self, ctx:CaloriesAssistantParser.PlankItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#doItem.
    def visitDoItem(self, ctx:CaloriesAssistantParser.DoItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#duration.
    def visitDuration(self, ctx:CaloriesAssistantParser.DurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#distance.
    def visitDistance(self, ctx:CaloriesAssistantParser.DistanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#countableExercise.
    def visitCountableExercise(self, ctx:CaloriesAssistantParser.CountableExerciseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#undoCommand.
    def visitUndoCommand(self, ctx:CaloriesAssistantParser.UndoCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#statsCommand.
    def visitStatsCommand(self, ctx:CaloriesAssistantParser.StatsCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#summaryToday.
    def visitSummaryToday(self, ctx:CaloriesAssistantParser.SummaryTodayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#summaryDate.
    def visitSummaryDate(self, ctx:CaloriesAssistantParser.SummaryDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#weeklyStats.
    def visitWeeklyStats(self, ctx:CaloriesAssistantParser.WeeklyStatsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#statsThisWeek.
    def visitStatsThisWeek(self, ctx:CaloriesAssistantParser.StatsThisWeekContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#profileCommand.
    def visitProfileCommand(self, ctx:CaloriesAssistantParser.ProfileCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#setWeight.
    def visitSetWeight(self, ctx:CaloriesAssistantParser.SetWeightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#setHeight.
    def visitSetHeight(self, ctx:CaloriesAssistantParser.SetHeightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#setGoal.
    def visitSetGoal(self, ctx:CaloriesAssistantParser.SetGoalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CaloriesAssistantParser#setActivity.
    def visitSetActivity(self, ctx:CaloriesAssistantParser.SetActivityContext):
        return self.visitChildren(ctx)



del CaloriesAssistantParser