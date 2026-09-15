# CALCULAR SI UN AÑO ES BISIESTO
"""
Un año es bisiesto si es divisible entre cuatro,
pero no si es divisible entre 100
a no ser que sea divisible entre 400
"""

año = int(input())

if año % 4 == 0:
    if año % 100 == 0:
        if año % 400 == 0:
            print(año, "es bisiesto")
        else:
            print(año, "no es bisiesto")
    else:
        print(año, "es bisiesto")
else:
    print(año, "no es bisiesto")