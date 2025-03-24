CatalogueAnswer = {
    "1": "A",
    "2": "B",
    "3": "C",
    "4": "D",
    "5": "E",
    "6": "F",
    "7": "G",
}


Answer = "1234"
endAnswer = ""
for a in Answer:
    endAnswer += CatalogueAnswer[a]

print(endAnswer)