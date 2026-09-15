# PROBLEMA:
# Dado un numero entero positivo n, generar una secuencia aplicando el algoritmo:
# si n es par divides entre 2
# si n es impar multiplicas por 3 y sumas
# Repitir hasta que n sea 1
# Calcula la longitud de la secuencia que genera este número
# EJEMPLO:
# 22 → 16
# CASOS ESPECIALES:
# Para números negativos ó 0, devolver 0


def long_secuencia(n):
    if n <= 0:
        return 0
    length = 1
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
        length += 1
    return length


for n in range(-1, 10):
    longitud = long_secuencia(n)
    print(f"número :{n}, longitud de secuencia: {longitud}")
