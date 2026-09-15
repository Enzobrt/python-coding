import math as m


def coordenadas_del_circulo(r):
    """La funcion coordenadas del circulo recibe como input
    un radio y devuelve la coordenadas de un
    octavo del circulo de ese radio"""
    x_actual = 0
    y_actual = m.floor(r)
    coordenadas = []
    while y_actual >= x_actual:
        coordenadas.append([x_actual, y_actual])
        x_actual += 1
        if x_actual**2 + y_actual**2 > r**2:
            y_actual -= 1
    return coordenadas


radio = float(input("Radio = "))
print(coordenadas_del_circulo(radio))
