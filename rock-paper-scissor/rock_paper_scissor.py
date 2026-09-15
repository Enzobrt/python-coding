# Este programa simula el juego de piedra, papel y tijera

import random

resultados = [[0, -1, 1],  # Piedra
              [1, 0, -1],  # Papel
              [-1, 1, 0]]  # Tijera

while True:
    usuario = input("Elige (Piedra, Papel, Tijera): ").lower()
    pc = random.choice(["piedra", "papel", "Tijera"]).lower()

    match usuario:
        case "r":
            usuario = "piedra"
        case "p":
            usuario = "papel"
        case "t":
            usuario = "tijera"

    print(f"Has elegido: {usuario}")
    print(f"La maquina ha elegido: {pc}\n")

    match usuario:
        case "piedra":
            usuario_num = 0
        case "papel":
            usuario_num = 1
        case "tijera":
            usuario_num = 2

    match pc:
        case "piedra":
            pc_num = 0
        case "papel":
            pc_num = 1
        case "tijera":
            pc_num = 2

    jugada = "".join(sorted(f"{usuario}{pc}"))

    mensajes = {
        "aaeeiijjrrtt": "Las tijeras se desafilan",  # tijera tijera
        "aadeeiijprrt": "La piedra aplasta a la tijera",  # tijera piedra
        "aaeeijlpprt": "La tijera corta el papel",  # tijera papel
        "aadeeiijprrt": "La piedra aplasta a la tijera",  # piedra tijera
        "aaddeeiipprr": "Las piedra se chocan",  # piedra piedra
        "aadeeilpppr": "El papel envuelve a la piedra",  # piedra papel
        "aaeeijlpprt": "La tijera corta el papel",  # papel tijera
        "aadeeilpppr": "El papel envuelve a la piedra",  # papel piedra
        "aaeellpppp": "Los papeles se doblan",  # papel papel
    }
    print(mensajes[jugada])

    match resultados[usuario_num][pc_num]:
        case 0:
            print("¡Es un empate!")
        case -1:
            print("¡Has perdido!")
        case 1:
            print("¡Has ganado!")

    jugar_otra_vez = input("\n¿Quieres jugar otra vez? (y/n) : ")
    if jugar_otra_vez != "y":
        break
