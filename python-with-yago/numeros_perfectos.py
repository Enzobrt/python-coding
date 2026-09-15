def lista_divisores(n):
    "Da una lista a partir de un número"
    lista = []
    for i in range(1, n):
        if n % i == 0:
            lista.append(i)
    return lista


lista_numeros = [1, 6, 7, 28, 496, 60]

for i in lista_numeros:
    print(lista_divisores(i))


def sumar_lista(lista: list) -> int:
    "Suma los números de la lista"
    suma = 0
    for i in lista:
        suma = suma + i
    return suma


lista_1 = [1, 2, 3]
lista_2 = [1]
lista_3 = [1, 2, 4, 7, 14]

print(sumar_lista(lista_1))
print(sumar_lista(lista_2))
print(sumar_lista(lista_3))


def es_perfecto(n):
    "Devuelve true si n es perfecto y false si no"
    lista_div = lista_divisores(n)
    suma = sumar_lista(lista_div)
    if n == suma:
        return True
    else:
        return False


for i in lista_numeros:
    print(i, es_perfecto(i))
