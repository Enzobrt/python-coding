def es_narcisista(numero: int) -> bool:
    num_str = str(numero)
    suma = 0
    for digito in num_str:
        suma += int(digito) ** len(num_str)
    return suma == numero


print(es_narcisista(int(input())))
