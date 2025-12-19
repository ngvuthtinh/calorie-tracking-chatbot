grammar CaloriesAssistant;

/* =======================
   ROOT
   ======================= */

program
  : line* EOF
  ;

line
  : command (NEWLINE+ | EOF)
  | NEWLINE+
  ;

command
  : foodCommand
  | exerciseCommandTop
  | statsCommand
  | profileCommand
  | undoCommand
  ;

/* =======================
   FOOD (F...)
   ======================= */

foodCommand
  : foodLog
  | foodEdit
  | foodAddToEntry
  | foodMove
  | foodDelete
  ;

foodLog
  : foodLogBody
  ;

/*
Examples:
- breakfast: 2 eggs, 1 cup milk
- eat: pho bo (small), "coconut water"
*/
foodLogBody
  : mealLabel? actionLabel? COLON foodItems
  ;

foodEdit
  : EDIT foodEntryId COLON foodLogBody
  ;

/* add = add items to EXISTING food entry */
foodAddToEntry
  : ADD foodEntryId COLON foodItems
  ;

/* move = assign / reassign meal */
foodMove
  : MOVE foodEntryId TO mealLabel
  ;

foodDelete
  : DELETE foodEntryId
  ;

foodEntryId
  : FOOD_ID
  ;

foodItems
  : foodItem (COMMA foodItem)*
  ;

foodItem
  : quantity? foodName note?
  ;

quantity
  : INT unit?
  ;

unit
  : UNIT
  ;

foodName
  : nameAtom (nameAtom)*
  ;

nameAtom
  : WORD
  | STRING
  ;

note
  : LPAREN noteText RPAREN
  ;

noteText
  : (WORD | STRING | INT | UNIT | DASH | SLASH | DOT)+
  ;

mealLabel
  : BREAKFAST
  | LUNCH
  | DINNER
  | SNACK
  ;

actionLabel
  : EAT
  | DRINK
  ;

/* =======================
   EXERCISE (X...)
   ======================= */

exerciseCommandTop
  : exerciseLog
  | exerciseEdit
  | exerciseAddToEntry
  | exerciseDelete
  ;

/*
Example:
- exercise: run 30 min, do 20 pushups
*/
exerciseLog
  : EXERCISE COLON exerciseItems
  ;

exerciseEdit
  : EDIT exerciseEntryId COLON EXERCISE COLON exerciseItems
  ;

/* add = add items to EXISTING exercise entry */
exerciseAddToEntry
  : ADD exerciseEntryId COLON exerciseItems
  ;

exerciseDelete
  : DELETE exerciseEntryId
  ;

exerciseEntryId
  : EX_ID
  ;

exerciseItems
  : exerciseItem (COMMA exerciseItem)*
  ;

exerciseItem
  : runItem
  | walkItem
  | cyclingItem
  | swimItem
  | plankItem        
  | doItem
  ;

runItem
  : RUN (duration | distance)
  ;

walkItem
  : WALK (duration | distance)
  ;

cyclingItem
  : CYCLING (duration | distance)
  ;

swimItem
  : SWIM duration
  ;

/* plank tính theo thời gian */
plankItem
  : PLANK duration
  ;

/* do = count-based exercises */
doItem
  : DO countableExercise
  ;

duration
  : INT MIN
  ;

distance
  : INT KM
  ;

countableExercise
  : INT PUSHUPS
  | INT SQUATS
  | INT LUNGES
  ;

/* =======================
   UNDO (global or scoped)
   ======================= */

undoCommand
  : UNDO (UNDO_SCOPE)?
  ;

UNDO_SCOPE
  : F_SCOPE
  | X_SCOPE
  ;

/* =======================
   STATS (must start with SHOW)
   ======================= */

statsCommand
  : SHOW summaryToday
  | SHOW summaryDate
  | SHOW weeklyStats
  | SHOW statsThisWeek
  ;

summaryToday
  : SUMMARY TODAY
  ;

summaryDate
  : SUMMARY DATE
  ;

weeklyStats
  : WEEKLY STATS
  ;

statsThisWeek
  : STATS THIS WEEK
  ;

/* =======================
   PROFILE (must start with SET)
   ======================= */

profileCommand
  : setWeight
  | setHeight
  | setGoal
  | setActivity
  ;

setWeight
  : SET WEIGHT (TO)? INT KG
  ;

setHeight
  : SET HEIGHT (TO)? INT CM
  ;

setGoal
  : SET GOAL (TO)? GOAL_TYPE
  ;

setActivity
  : SET ACTIVITY LEVEL (TO)? ACTIVITY_LEVEL
  ;

/* =======================
   LEXER
   ======================= */

STRING : '"' (~["\r\n])* '"' ;

/* Prefixed IDs */
FOOD_ID : [fF] [0-9]+ ;
EX_ID   : [xX] [0-9]+ ;

/* Undo scopes */
F_SCOPE : [fF] ;
X_SCOPE : [xX] ;

/* Core commands */
SHOW    : [sS][hH][oO][wW];
SET     : [sS][eE][tT];
EDIT    : [eE][dD][iI][tT];
ADD     : [aA][dD][dD];
DELETE  : [dD][eE][lL][eE][tT][eE];
UNDO    : [uU][nN][dD][oO];
MOVE    : [mM][oO][vV][eE];
TO      : [tT][oO];

/* Food keywords */
BREAKFAST : [bB][rR][eE][aA][kK][fF][aA][sS][tT];
LUNCH     : [lL][uU][nN][cC][hH];
DINNER    : [dD][iI][nN][nN][eE][rR];
SNACK     : [sS][nN][aA][cC][kK];

EAT       : [eE][aA][tT];
DRINK     : [dD][rR][iI][nN][kK];

/* Exercise label + verbs */
EXERCISE : [eE][xX][eE][rR][cC][iI][sS][eE];

RUN      : [rR][uU][nN];
WALK     : [wW][aA][lL][kK];
CYCLING  : [cC][yY][cC][lL][iI][nN][gG];
SWIM     : [sS][wW][iI][mM];
PLANK    : [pP][lL][aA][nN][kK];
DO       : [dD][oO];

PUSHUPS  : [pP][uU][sS][hH][uU][pP][sS];
SQUATS   : [sS][qQ][uU][aA][tT][sS];
LUNGES   : [lL][uU][nN][gG][eE][sS];

/* Stats keywords */
SUMMARY : [sS][uU][mM][mM][aA][rR][yY];
TODAY   : [tT][oO][dD][aA][yY];
WEEKLY  : [wW][eE][eE][kK][lL][yY];
STATS   : [sS][tT][aA][tT][sS];
THIS    : [tT][hH][iI][sS];
WEEK    : [wW][eE][eE][kK];

DATE : DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT ;
fragment DIGIT : [0-9] ;

/* Profile keywords + values */
WEIGHT  : [wW][eE][iI][gG][hH][tT];
HEIGHT  : [hH][eE][iI][gG][hH][tT];
GOAL    : [gG][oO][aA][lL];
ACTIVITY: [aA][cC][tT][iI][vV][iI][tT][yY];
LEVEL   : [lL][eE][vV][eE][lL];

GOAL_TYPE
  : [lL][oO][sS][eE]
  | [mM][aA][iI][nN][tT][aA][iI][nN]
  | [gG][aA][iI][nN]
  ;

ACTIVITY_LEVEL
  : [lL][oO][wW]
  | [mM][oO][dD][eE][rR][aA][tT][eE]
  | [hH][iI][gG][hH]
  ;

/* Units (Option A: KG/KM/MIN/CM are separate tokens) */
MIN : [mM][iI][nN];
KM  : [kK][mM];
KG  : [kK][gG];
CM  : [cC][mM];

UNIT
  : [gG]
  | [mM][lL]
  | [lL]
  | [pP][iI][eE][cC][eE] [sS]?
  | [bB][oO][wW][lL] [sS]?
  | [cC][uU][pP] [sS]?
  | [gG][lL][aA][sS][sS] ([eE][sS])?
  | [cC][aA][nN] [sS]?
  | [sS][lL][iI][cC][eE] [sS]?
  ;

/* Punctuation */
COLON  : ':';
COMMA  : ',';
LPAREN : '(';
RPAREN : ')';
DASH   : '-';
SLASH  : '/';
DOT    : '.';

INT : [0-9]+;

WORD : [a-zA-Z] [a-zA-Z0-9_]* ;

NEWLINE : ('\r'? '\n')+;
WS : [ \t]+ -> skip;
