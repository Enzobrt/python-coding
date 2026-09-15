def segundos(seg: int):
    minutos = seg // 60
    segundos = seg % 60
    horas = minutos // 60
    minutos = minutos % 60
    print(f'{seg} segundos → {horas:02d}:{minutos:02d}:{segundos:02d}')


"""
lista_segundos = (59, 60, 61, 359, 360, 361, 3599, 3600, 3601, 3661)


for i in lista_segundos:
    segundos(i)
"""

####################################################################


def pitagoraras(a: int, b: int, c: int) -> bool:
    """Comprueba si a, b y c son una terna pitagorica"""
    if a**2 + b**2 == c**2:
        print(f'{a}, {b}, {c} son números pitagoricos')
    else:
        print(f'{a}, {b}, {c} no son números pitagoricos')


"""
pitagoraras(3, 4, 5)
pitagoraras(0, 1, 1)
pitagoraras(3, 3, 3)
"""
pitagoraras(c=5, a=3, b=4)

####################################################################


def maximo(a, b):
    if a > b:
        return a
    else:
        return b


maximo(10, 3)

####################################################################


def minimo(a, b):
    if a < b:
        return a
    else:
        return b


minimo(10, 3)
