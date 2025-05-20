
#creando matriz de estacionamiento
def crear_matriz_parqueo(filas, espacios_por_fila, espacios_moto):
    matriz = []
    contador_moto = 0

    # Inicializar la matriz con espacios vacíos
    for i in range(filas):
        fila = []
        for j in range(espacios_por_fila):
            letra_fila = chr(65 + i)  # Convertir el número de fila a letra (A, B, C, ...)
            codigo = f"{letra_fila}-{j + 1}"  # Generar el código de espacio

            if contador_moto < espacios_moto:
                codigo += "M"  # Agregar "M" para motos
                contador_moto += 1

            fila.append(codigo)  # Agregar el código a la fila
        matriz.append(fila)  # Agregar la fila a la matriz
    return matriz     

# Configuración inicial del parqueo - Inicio de programa

print("Bienvenido al sistema de parqueo!")

#setup de variables
filas = int(input("Ingresa la cantidad de filas:"))
espacios_por_fila = int(input("Ingresa la cantidad de espacios por fila:"))
espacios_moto = int(input("Ingresa la cantidad de espacios para motos:"))

# Crear la matriz de estacionamiento
parqueo = crear_matriz_parqueo(filas, espacios_por_fila, espacios_moto)

# Mostrar la matriz de estacionamiento
print("Estado inicial del estacionamiento:")

for fila in parqueo:
    print(" ".join(fila))