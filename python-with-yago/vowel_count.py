def vowel_count(text):
    vocales = {
            "a": 0,
            "e": 0,
            "i": 0,
            "o": 0,
            "u": 0
            }
    posiciones = {
            "a": [],
            "e": [],
            "i": [],
            "o": [],
            "u": []
            }
    for i in text:
        match i:
            case "a":
                vocales["a"] += 1
                posiciones["a"].append(text.index(i))
            case "e":
                vocales["e"] += 1
                posiciones["e"].append(text.index(i))
            case "i":
                vocales["i"] += 1
                posiciones["i"].append(text.index(i))
            case "o":
                vocales["o"] += 1
                posiciones["o"].append(text.index(i))
            case "u":
                vocales["u"] += 1
                posiciones["u"].append(text.index(i))
    return vocales and posiciones


text_1 = "iqaroekokeifum"
print(text_1, vowel_count(text_1))
