import random

list_num = []

for i in range(10):
    list_num.append(random.randint(0, 20))


print(list_num)

# Imprimir los valores pares

list_pares = []

for i in list_num.copy():
    if i % 2 == 0:
        list_pares.append(i)
        list_num.remove(i)

print(list_num)
print(list_pares)

# FUncion que devuevle el número máximo de la lista


def max_list(lista):
    """Devuelve el número más grande de una lista"""
    if len(lista) == 0:
        return None
    maximo = lista[0]
    for i in lista:
        if i > maximo:
            maximo = i
    return maximo


def min_list(lista):
    """Devuelve el número más pequeño de una lista"""
    if len(lista) == 0:
        return None
    minimo = lista[0]
    for i in lista:
        if i < minimo:
            minimo = i
    return minimo


# Suma todos los elementos de la lista
def suma_lista(lista):
    """Suma todos los números de una lista"""
    suma = 0
    for i in lista:
        suma += i
        # print(suma, i)
    return suma


def enzo_sort(lista):
    """Devuelve una lista ordenada y destruye la original"""
    l2 = []
    for i in range(len(lista.copy())):
        minimo = min_list(lista)
        l2.append(minimo)
        # print(i, l2)
        lista.remove(minimo)
    # print(l2, len(l2))
    return l2


"""
l1 = []  # 0
print("Original", l1, ", ordenada", enzo_sort(l1.copy()))
l2 = [7]
print("Original", l2, ", ordenada", enzo_sort(l2.copy()))
l3 = [2] * 5  # 2
print("Original", l3, ", ordenada", enzo_sort(l3.copy()))
l4 = [0, 3, 1, 2, 4, 6]  # 6
print("Original", l4, ", ordenada", enzo_sort(l4.copy()))
l5 = [-1] * 4  # -1
print("Original", l5, ", ordenada", enzo_sort(l5.copy()))
"""


def contar(lista, num):
    """Devuelve las veces que aparece el numero en la lista"""
    print(lista)
    if len(lista) == 0:
        return 0
    """
    if len(lista) == 1 and lista[0] == num:
        return 1
    if len(lista) == 1 and lista[0] != num:
        return 0
    """
    contador = 0
    for i in lista:
        if num == i:
            contador += 1

    return contador


print("n", contar([], 1))
print("n", contar([1], 1))
print("n", contar([1], 2))
l1 = [1, 2, 3] * 3
print("n", contar(l1, 2))
