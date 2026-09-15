"""
def fizz_buzz(num):
    if num % 3 == 0 and num % 5 == 0:
        print("FizzBuzz")
    elif num % 3 == 0:
        print("Fizz")
    elif num % 5 == 0:
        print("Buzz")
    else:
        print(num)
"""


def fizz_buzz_acumulativo(n):
    cadena_palabras = ""
    if n % 3 == 0:
        cadena_palabras += "Fizz"
    if n % 5 == 0:
        cadena_palabras += "Buzz"
    if n % 7 == 0:
        cadena_palabras += "Bazz"
    if cadena_palabras == "":
        cadena_palabras = str(n)

    print(cadena_palabras)


for i in range(1, 40):
    fizz_buzz_acumulativo(i)
