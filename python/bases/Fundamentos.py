from Varios import nuevo_tema

print("hola mundo")
# Esto es un comentario
"""Este es un comentario
 de 
 muchas 
 lineas"""

# =========================== variables  ===========================
nuevo_tema("variables")
#int:
edad = 21
#float:
estatura = 1.50
#str:
nombre = "Rodolfo"
#bool:
fuma = False


print("edad:",edad)
print("estatura:",estatura)
print("nombre:",nombre)
print("fuma:",fuma)

# =========================== operadores aritméticos  ===========================
nuevo_tema("operadores aritméticos")
a = 13
b = 3

print("a:", a)
print("b:", b)

print ("a + b: ", a + b)
print ("a - b: ", a - b)
print ("a * b: ", a * b)
print ("a / b: ", a / b)
print ("a % b: ", a % b)
print ("a ** b: ", a ** b)


# =========================== operadores de comparación  ===========================
nuevo_tema("operadores de comparación")
numero_1 = 5
numero_2 = 6

print("numero_1:", numero_1)
print("numero_2:", numero_2)

print("numero_1 > numero_2 :", numero_1 > numero_2)
print("numero_1 < numero_2 :", numero_1 < numero_2)
print("numero_1 >= numero_2 :", numero_1 >= numero_2)
print("numero_1 <= numero_2 :", numero_1 <= numero_2)
print("numero_1 == numero_2 :", numero_1 == numero_2)

# =========================== operadores boleanos  ===========================
nuevo_tema("operadores boleanos")
x = True
y = False;

print("x: ", x)
print("y: ", y)
print("x or y:", x or y)
print("x and y:", x and y)
print("not x", not x)

# =========================== operadores nivel de bits  ===========================
nuevo_tema("operadores a nivel de bits")
numero_1 = 9
numero_2 = 3

print("numero_1:", numero_1)
print("numero_2:", numero_2)

print("numero_1 | numero_2:", numero_1 | numero_2)
print("numero_1 & numero_2:", numero_1 & numero_2)
print("numero_1 ^ numero_2:", numero_1 ^ numero_2)
print("~numero_1:", ~numero_1)
print("numero_1 >> 1:", numero_1 >> 1)
print("numero_1 << 2:", numero_1 << 1)

# =========================== listas  ===========================
nuevo_tema("listas")
vehiculos = []
animales = list()

cosas = ["flor", 23, 89.2, True]
frutas = ['platanos', 'manzanas', "cerezas", "kiwis", \
          "melones", "sandias", "mangos", "mandarinas"]

print("frutas:", frutas)
# seleccionando un elemento
print("frutas[2]:", frutas[2])
# seleccionando un rango
print("frutas[2:5]:", frutas[2:5])
# seleccionando el ultimo elemento
print("frutas[-1]:", frutas[-1])
# seleccionando el penúltimo elemento
print("frutas[-2]:", frutas[-2])
# obteniendo la longitud de la lista
print("len(frutas:", len(frutas))
# seleccionando del elmento 1 al 7 de dos en dos
print("frutas[1:8:2]:", frutas[1:8:2])

print("------- Agregando un elemento")
print("frutas:", frutas)
# agragando un elemento
frutas.append("guayabas")

print("frutas:", frutas)

print("------- Removiendo un elemento")
# quitando un elemento
frutas.remove("platanos")

print("frutas:", frutas)



# =========================== Instrucciones de control  ===========================
# --------------------- ciclo for
nuevo_tema("instrucciones de control")
print ("--------------------- ciclo for")
for indice in range(1,4):
    print(indice)

print ("-----------------")
for indice in range(-4, 4, 1):
    print(indice)
print ("-----------------")
for fruta in frutas:
    print(fruta)

print ("-----------------")
for i, fruta in enumerate(frutas):
    print(i, fruta)


print ("--------------------- if-else")

numero_1 = 4
numero_2 = 8

if numero_1 > numero_2: 
    print(f"numero_1 { numero_1} es mayor a numero_2 {numero_2}")
else:
    print(f"numero_1 { numero_1} es no mayor a numero_2 { numero_2}")


nuevo_tema("funciones")    