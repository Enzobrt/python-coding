## CONDICIONALES

a = 0

if a > 0:
    print("Es positivo")
elif a == 0:
    print("Es cero")
else:
    print("Es negativo")

# Calculadora
num1 = 10  # float(input())
num2 = 17  # float(input())

if num2 == 0:
    print("No se puede dividir entre cero")
else:
    print(num1 / num2)

######################################################
## BUCLES

# While
contador = 10

while contador >= 0:
    print(contador)
    contador -= 1

# nº divisible entre 2, 3 y 5 menor que 100
num = 0
divisores = "2, 3, 5"

while num <= 100:
    if num == 0:
        pass
    elif (num % 2 == 0) and (num % 3 == 0) and (num % 5 == 0):
        print(num, "es divisible entre", divisores)
        break
    num += 1

print()
# For
abecedario = "abcdefghijklmnñopqrstuvwxyz0123456789^+¨,.-_/"
vocales = "aeiou"

for i in abecedario:
    if i in vocales:
        print(i)
    if i > "v":
        continue

# Calculadora h,min,s