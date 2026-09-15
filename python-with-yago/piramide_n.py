#Un programa que imprima todos los numeros hasta n ese mismo numero de veces

NUMERO = 15

for i in range(NUMERO + 1):
    if i < 10:
        caracter = " " + str(i) + "  "
    else:
        caracter = " " + str(i) + " "
    print(caracter * i)
