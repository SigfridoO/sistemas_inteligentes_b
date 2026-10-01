from Varios import nuevo_tema

nuevo_tema("Diccionarios")

laboratorio = {
    "motores": 4,
    "modulos": 4,
    "extras": "tablero de control",
    "mesas": 4,
    "materias": ["microcontroladores", "sistemas inteligentes", \
                 "neumática", "manufactura", "taller de investigación", \
                 "seguridad y normatividad", "desarrollo organizacional", \
                 "programación"]
}

print("laboratorio: ", laboratorio)

alumno = {
    "nombre": "Francisco",
    "apellido": "Reyes Lima",
    "estatura": 1.70,
    "edad": 95
}

print("alumno: ", alumno)

# Obteniendo el valor de un elemento del diccionario
print('alumno.get("nombre"):',  alumno.get("nombre"))

# Obteniendo los elementos del diccionario
print('alumno.items():',  alumno.items())

# Obteniendo las llaves del diccionario
print('alumno.keys():',  alumno.keys())

# Obteniendo los valores del diccionario
print('alumno.values():',  alumno.values())


# Modificando un valor
print('alumno:',  alumno)
alumno.update({"nombre": "Sebastian"})
print('alumno:',  alumno)

for llave, valor in alumno.items() :
    print(f"{llave}- {valor}")



