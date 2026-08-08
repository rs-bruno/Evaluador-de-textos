import os
from semantics import evaluate

def printTwoDecimals(floatingPoint):
    return str(floatingPoint)[:str(floatingPoint).index('.') + 3]

def printBookEvaluations(bookName, bookPath):
    bookFile = open(bookPath, "r", encoding="UTF-8")
    details = evaluate(bookFile)
    r = details.richness
    bookFile.close()
    print(bookName)
    print(f"Sintactic richness: {printTwoDecimals(r.getSintacticRichness())}% ({r.getUsedWords()} / {r.getTotalWords()})")
    print(f"Semantic richness: {printTwoDecimals(r.getSemanticRichness())}% ({r.getUsedPrimitives()} / {r.getTotalPrimitives()})")

    dyf = details.getDifficultyAndEffort()
    print(f"Difficulty: {printTwoDecimals(dyf["difficulty"])}")
    print(f"Effort: {printTwoDecimals(dyf["effort"])}")
    print("")

booksPath = os.sep.join([os.curdir, "books", ""])
booksNames = os.listdir(booksPath)

if __name__ == "__main__":
    userInput = None
    while userInput != "q":
        print("1) Evaluate sample books")
        print("2) Evaluate book from file")
        print("Q) Quit")
        userInput = input().strip().lower()
        if userInput == "1":
            for bookName in booksNames:
                bookPath = booksPath + bookName
                printBookEvaluations(bookName, bookPath)
        elif userInput == "2":
            print("File path: ", end="")
            bookPath = input()
            printBookEvaluations("user book", bookPath)

