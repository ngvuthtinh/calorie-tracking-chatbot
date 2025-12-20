# Generated from CaloriesAssistant.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CaloriesAssistantParser import CaloriesAssistantParser
else:
    from CaloriesAssistantParser import CaloriesAssistantParser

# This class defines a complete listener for a parse tree produced by CaloriesAssistantParser.
class CaloriesAssistantListener(ParseTreeListener):

    # Enter a parse tree produced by CaloriesAssistantParser#program.
    def enterProgram(self, ctx:CaloriesAssistantParser.ProgramContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#program.
    def exitProgram(self, ctx:CaloriesAssistantParser.ProgramContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#line.
    def enterLine(self, ctx:CaloriesAssistantParser.LineContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#line.
    def exitLine(self, ctx:CaloriesAssistantParser.LineContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#command.
    def enterCommand(self, ctx:CaloriesAssistantParser.CommandContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#command.
    def exitCommand(self, ctx:CaloriesAssistantParser.CommandContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodCommand.
    def enterFoodCommand(self, ctx:CaloriesAssistantParser.FoodCommandContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodCommand.
    def exitFoodCommand(self, ctx:CaloriesAssistantParser.FoodCommandContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodLog.
    def enterFoodLog(self, ctx:CaloriesAssistantParser.FoodLogContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodLog.
    def exitFoodLog(self, ctx:CaloriesAssistantParser.FoodLogContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodLogBody.
    def enterFoodLogBody(self, ctx:CaloriesAssistantParser.FoodLogBodyContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodLogBody.
    def exitFoodLogBody(self, ctx:CaloriesAssistantParser.FoodLogBodyContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodEdit.
    def enterFoodEdit(self, ctx:CaloriesAssistantParser.FoodEditContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodEdit.
    def exitFoodEdit(self, ctx:CaloriesAssistantParser.FoodEditContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodAddToEntry.
    def enterFoodAddToEntry(self, ctx:CaloriesAssistantParser.FoodAddToEntryContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodAddToEntry.
    def exitFoodAddToEntry(self, ctx:CaloriesAssistantParser.FoodAddToEntryContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodMove.
    def enterFoodMove(self, ctx:CaloriesAssistantParser.FoodMoveContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodMove.
    def exitFoodMove(self, ctx:CaloriesAssistantParser.FoodMoveContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodDelete.
    def enterFoodDelete(self, ctx:CaloriesAssistantParser.FoodDeleteContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodDelete.
    def exitFoodDelete(self, ctx:CaloriesAssistantParser.FoodDeleteContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodEntryId.
    def enterFoodEntryId(self, ctx:CaloriesAssistantParser.FoodEntryIdContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodEntryId.
    def exitFoodEntryId(self, ctx:CaloriesAssistantParser.FoodEntryIdContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodItems.
    def enterFoodItems(self, ctx:CaloriesAssistantParser.FoodItemsContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodItems.
    def exitFoodItems(self, ctx:CaloriesAssistantParser.FoodItemsContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodItem.
    def enterFoodItem(self, ctx:CaloriesAssistantParser.FoodItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodItem.
    def exitFoodItem(self, ctx:CaloriesAssistantParser.FoodItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#quantity.
    def enterQuantity(self, ctx:CaloriesAssistantParser.QuantityContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#quantity.
    def exitQuantity(self, ctx:CaloriesAssistantParser.QuantityContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#unit.
    def enterUnit(self, ctx:CaloriesAssistantParser.UnitContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#unit.
    def exitUnit(self, ctx:CaloriesAssistantParser.UnitContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#foodName.
    def enterFoodName(self, ctx:CaloriesAssistantParser.FoodNameContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#foodName.
    def exitFoodName(self, ctx:CaloriesAssistantParser.FoodNameContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#nameAtom.
    def enterNameAtom(self, ctx:CaloriesAssistantParser.NameAtomContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#nameAtom.
    def exitNameAtom(self, ctx:CaloriesAssistantParser.NameAtomContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#note.
    def enterNote(self, ctx:CaloriesAssistantParser.NoteContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#note.
    def exitNote(self, ctx:CaloriesAssistantParser.NoteContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#noteText.
    def enterNoteText(self, ctx:CaloriesAssistantParser.NoteTextContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#noteText.
    def exitNoteText(self, ctx:CaloriesAssistantParser.NoteTextContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#mealLabel.
    def enterMealLabel(self, ctx:CaloriesAssistantParser.MealLabelContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#mealLabel.
    def exitMealLabel(self, ctx:CaloriesAssistantParser.MealLabelContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#actionLabel.
    def enterActionLabel(self, ctx:CaloriesAssistantParser.ActionLabelContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#actionLabel.
    def exitActionLabel(self, ctx:CaloriesAssistantParser.ActionLabelContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseCommandTop.
    def enterExerciseCommandTop(self, ctx:CaloriesAssistantParser.ExerciseCommandTopContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseCommandTop.
    def exitExerciseCommandTop(self, ctx:CaloriesAssistantParser.ExerciseCommandTopContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseLog.
    def enterExerciseLog(self, ctx:CaloriesAssistantParser.ExerciseLogContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseLog.
    def exitExerciseLog(self, ctx:CaloriesAssistantParser.ExerciseLogContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseEdit.
    def enterExerciseEdit(self, ctx:CaloriesAssistantParser.ExerciseEditContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseEdit.
    def exitExerciseEdit(self, ctx:CaloriesAssistantParser.ExerciseEditContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseEditItem.
    def enterExerciseEditItem(self, ctx:CaloriesAssistantParser.ExerciseEditItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseEditItem.
    def exitExerciseEditItem(self, ctx:CaloriesAssistantParser.ExerciseEditItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseAddToEntry.
    def enterExerciseAddToEntry(self, ctx:CaloriesAssistantParser.ExerciseAddToEntryContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseAddToEntry.
    def exitExerciseAddToEntry(self, ctx:CaloriesAssistantParser.ExerciseAddToEntryContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseDelete.
    def enterExerciseDelete(self, ctx:CaloriesAssistantParser.ExerciseDeleteContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseDelete.
    def exitExerciseDelete(self, ctx:CaloriesAssistantParser.ExerciseDeleteContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseEntryId.
    def enterExerciseEntryId(self, ctx:CaloriesAssistantParser.ExerciseEntryIdContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseEntryId.
    def exitExerciseEntryId(self, ctx:CaloriesAssistantParser.ExerciseEntryIdContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseItems.
    def enterExerciseItems(self, ctx:CaloriesAssistantParser.ExerciseItemsContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseItems.
    def exitExerciseItems(self, ctx:CaloriesAssistantParser.ExerciseItemsContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#exerciseItem.
    def enterExerciseItem(self, ctx:CaloriesAssistantParser.ExerciseItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#exerciseItem.
    def exitExerciseItem(self, ctx:CaloriesAssistantParser.ExerciseItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#runItem.
    def enterRunItem(self, ctx:CaloriesAssistantParser.RunItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#runItem.
    def exitRunItem(self, ctx:CaloriesAssistantParser.RunItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#walkItem.
    def enterWalkItem(self, ctx:CaloriesAssistantParser.WalkItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#walkItem.
    def exitWalkItem(self, ctx:CaloriesAssistantParser.WalkItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#cyclingItem.
    def enterCyclingItem(self, ctx:CaloriesAssistantParser.CyclingItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#cyclingItem.
    def exitCyclingItem(self, ctx:CaloriesAssistantParser.CyclingItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#swimItem.
    def enterSwimItem(self, ctx:CaloriesAssistantParser.SwimItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#swimItem.
    def exitSwimItem(self, ctx:CaloriesAssistantParser.SwimItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#plankItem.
    def enterPlankItem(self, ctx:CaloriesAssistantParser.PlankItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#plankItem.
    def exitPlankItem(self, ctx:CaloriesAssistantParser.PlankItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#doItem.
    def enterDoItem(self, ctx:CaloriesAssistantParser.DoItemContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#doItem.
    def exitDoItem(self, ctx:CaloriesAssistantParser.DoItemContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#duration.
    def enterDuration(self, ctx:CaloriesAssistantParser.DurationContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#duration.
    def exitDuration(self, ctx:CaloriesAssistantParser.DurationContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#distance.
    def enterDistance(self, ctx:CaloriesAssistantParser.DistanceContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#distance.
    def exitDistance(self, ctx:CaloriesAssistantParser.DistanceContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#countableExercise.
    def enterCountableExercise(self, ctx:CaloriesAssistantParser.CountableExerciseContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#countableExercise.
    def exitCountableExercise(self, ctx:CaloriesAssistantParser.CountableExerciseContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#undoCommand.
    def enterUndoCommand(self, ctx:CaloriesAssistantParser.UndoCommandContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#undoCommand.
    def exitUndoCommand(self, ctx:CaloriesAssistantParser.UndoCommandContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#statsCommand.
    def enterStatsCommand(self, ctx:CaloriesAssistantParser.StatsCommandContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#statsCommand.
    def exitStatsCommand(self, ctx:CaloriesAssistantParser.StatsCommandContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#summaryToday.
    def enterSummaryToday(self, ctx:CaloriesAssistantParser.SummaryTodayContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#summaryToday.
    def exitSummaryToday(self, ctx:CaloriesAssistantParser.SummaryTodayContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#summaryDate.
    def enterSummaryDate(self, ctx:CaloriesAssistantParser.SummaryDateContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#summaryDate.
    def exitSummaryDate(self, ctx:CaloriesAssistantParser.SummaryDateContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#weeklyStats.
    def enterWeeklyStats(self, ctx:CaloriesAssistantParser.WeeklyStatsContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#weeklyStats.
    def exitWeeklyStats(self, ctx:CaloriesAssistantParser.WeeklyStatsContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#statsThisWeek.
    def enterStatsThisWeek(self, ctx:CaloriesAssistantParser.StatsThisWeekContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#statsThisWeek.
    def exitStatsThisWeek(self, ctx:CaloriesAssistantParser.StatsThisWeekContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#profileCommand.
    def enterProfileCommand(self, ctx:CaloriesAssistantParser.ProfileCommandContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#profileCommand.
    def exitProfileCommand(self, ctx:CaloriesAssistantParser.ProfileCommandContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#setWeight.
    def enterSetWeight(self, ctx:CaloriesAssistantParser.SetWeightContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#setWeight.
    def exitSetWeight(self, ctx:CaloriesAssistantParser.SetWeightContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#setHeight.
    def enterSetHeight(self, ctx:CaloriesAssistantParser.SetHeightContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#setHeight.
    def exitSetHeight(self, ctx:CaloriesAssistantParser.SetHeightContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#setGoal.
    def enterSetGoal(self, ctx:CaloriesAssistantParser.SetGoalContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#setGoal.
    def exitSetGoal(self, ctx:CaloriesAssistantParser.SetGoalContext):
        pass


    # Enter a parse tree produced by CaloriesAssistantParser#setActivity.
    def enterSetActivity(self, ctx:CaloriesAssistantParser.SetActivityContext):
        pass

    # Exit a parse tree produced by CaloriesAssistantParser#setActivity.
    def exitSetActivity(self, ctx:CaloriesAssistantParser.SetActivityContext):
        pass



del CaloriesAssistantParser