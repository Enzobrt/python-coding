import random

letters = "abcdefghijklmnñopqrstuvwxyz"
numbers = "1234567890"
punctuation = ",.!#$%&'()*+, -./:;<=>?@[\]^_`{|}~"
characterList = ""

def generate_password(inputLen, characterList):
    password = ""
    for i in range(inputLen):
        # position = random.randint(0, len(characterList))
        # letter = characterList[position]
        letter = random.choice(characterList)
        password += letter
    return password

inputLen = int(input("Longitud contraseña: "))

print("Elige el set de characteres que quieras:\n1. Letras\n2. Números\n3. Characteres especiales\n4. Continuar")

while(True):
    characterChoice = int(input("Elige tus opciones: "))
    match characterChoice:
        case 1:
            characterList += letters
        case 2:
            characterList += numbers
        case 3:
            characterList += punctuation
        case 4:
            break
        case _:
            print("Elige una opción válida!")

print(generate_password(inputLen, characterList))
