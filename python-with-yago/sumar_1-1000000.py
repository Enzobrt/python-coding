def sumar_lista(lista):
    suma = 0
    for i in lista:
        suma += i
    return suma


lista1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(sumar_lista(lista1))

"""
lista = []

for i in range(1000):
    match i:
        case i % 3 == 0:
            lista.append(i)
        case i % 5 == 0:
"""
