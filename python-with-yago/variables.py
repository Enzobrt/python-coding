## TIPOS DE VARIABLES

a = 3  # Variable de tipo entero
print(type(a), a)
b = 3.5  # Variable de tipo decimal
print(type(b), b)
c = True  # Variable de tipo booleano
print(type(c), c)
d = "Hola" # Variable de tipo string 
print(type(d), d)
e = 'Mundo'
print(type(e), e)

print()
################################################################
# Cosas locos de los floats
num1 = 0.3
num2 = 0.1
result = num1 - num2  # 0.3 - 0.1 = 0.2

print(result)

print(num1 - 3 * num2)  # 0.3 - 3*0.1 = 0

print()
#################################################################
# Pruebas con strings

texto1 = "Hola"
texto2 = "Mundo"
textos = texto1 + texto2

print(textos)
print(texto1 + "1")
# print(texto1 + "1")  No probar por favor, da error
# print(texto1 - "1")  No probar por favor, da error

print()
################################################################
# Cosas locos de los numeros pt2
print("Distintas formas de imprimir mil millones")
print(1000000000)
print(1_000_000_000)
print(type(1e9), 1e9)
