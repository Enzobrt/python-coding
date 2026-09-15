pareja_1 = [2, 10]
pareja_2 = [4, 5]


def comprobar_producto(pareja_1, pareja_2):
    producto_pareja_1 = pareja_1[0] * pareja_1[1]
    producto_pareja_2 = pareja_2[0] * pareja_2[1]
    if producto_pareja_1 == producto_pareja_2:
        cond_1 = True
    return cond_1


def esta_en_medio(pareja_1, pareja_2):
    if pareja_1[0] < pareja_2[0] and pareja_2[1] < pareja_1[1]:
        cond_2 = True
    elif pareja_2[0] < pareja_1[0] and pareja_1[1] < pareja_2[1]:
        cond_2 = True
    return cond_2


pareja_1 = pareja_1.sort()
pareja_2 = pareja_2.sort()

cond_1 = comprobar_producto
cond_2 = esta_en_medio

if cond_1 and cond_2:
    print("Las parejas cumplen los dos requerimientos")
else:
    print("Las parejas no cumplen los requerimientos")
