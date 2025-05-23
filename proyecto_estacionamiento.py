
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
                codigo += "*"  # Agregar "*" para motos
                contador_moto += 1

            fila.append(codigo)  # Agregar el código a la fila
        matriz.append(fila)  # Agregar la fila a la matriz
    return matriz     

# Configuración inicial del parqueo - Inicio de programa

print("Bienvenido al sistema de parqueo!")

#setup de variables
filas = int(input("\nIngresa la cantidad de filas:"))
espacios_por_fila = int(input("Ingresa la cantidad de espacios por fila:"))
espacios_moto = int(input("Ingresa la cantidad de espacios para motos:"))

# Crear la matriz de estacionamiento
parqueo = crear_matriz_parqueo(filas, espacios_por_fila, espacios_moto)

# Mostrar la matriz de estacionamiento
print("\nEstado inicial del estacionamiento:")

for fila in parqueo:
    print(" ".join(fila))
print("\n")

#Función para mostrar el parqueo
def mostrar_parqueo(parqueo):
    print("\nEstado actual del estacionamiento:")
    for fila in parqueo:
        print(" ".join(fila))
    print("\n")


#Función para convertir codigo a índices
def codigo_a_indices(codigo):
    try:
        partes = codigo.upper().replace("*", " ").split("-")
        fila = ord(partes[0]) - 65  # Convertir letra a número (A=0, B=1, ...)
        columna = int(partes[1]) - 1  # Convertir número a índice (1=0, 2=1, ...)
        return fila, columna
    except:
        return -1, -1 #Este es para codigo invalido

#1. Función para ocupar espacios
def ocupar_espacio(parqueo, tipo_vehiculo, historial, contador_hora):
    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        mostrar_parqueo(parqueo)
        codigo = input(f"Ingrese el código del espacio para {tipo_vehiculo} a ocupar (Ejemplo: A-1): ").upper()
        fila, columna = codigo_a_indices(codigo)

        #Validamos
        if fila < 0 or fila >= len(parqueo) or columna < 0 or columna >= len(parqueo[0]):
            print("⚠️ Código inválido. Intente nuevamente.")
            intentos += 1
            continue

        espacio = parqueo[fila][columna]

        #Si ya está ocupado
        if espacio == "X":
            print("⚠️ El espacio ya está ocupado. Intente nuevamente.")
            intentos += 1
            continue

        #Si el espacio no es para motos y tenemos una moto
        if tipo_vehiculo == "moto" and "*" not in espacio:
            print("⚠️ El espacio no es exclusivo para motos. Intente nuevamente.")
            intentos += 1
            continue

        #Si el espacio es para motos y tenemos un carro
        if tipo_vehiculo == "carro" and "*" in espacio:
            print("El espacio es exclusivo para motos. Intente nuevamente.")
            intentos += 1
            continue

        #Si el espacio es correcto
        parqueo[fila][columna] = "X"
        historial.append((contador_hora, "Entrada", tipo_vehiculo, codigo))
        print("Vehículo registrado exitosamente.")
        print("\n")

        return contador_hora + 1
    
    print("Número máximo de intentos alcanzado. No se pudo registrar el vehículo.")
    return contador_hora

#2. Función para liberar espacio

#comprobación si era un espacio nomral o para motos
def es_espacio_para_moto(fila, columna, filas, columnas, cantidad_motos):
    # calculamos que numero de espacio es y en que orden de fila o columna
    numero_espacio = fila * columnas + columna
    return numero_espacio < cantidad_motos

#liberar espacio
def liberar_espacio(parqueo, historial, contador_hora, filas, columnas, cantidad_motos):
    mostrar_parqueo(parqueo)
    codigo = input("Ingrese el código del espacio a liberar (Ejemplo: A-1): ").upper()
    fila, columna = codigo_a_indices(codigo)

    #Validamos
    if fila < 0 or fila >= len(parqueo) or columna < 0 or columna >= len(parqueo[0]):
        print("⚠️ Código inválido. Intente nuevamente.")
        return contador_hora
    
    if parqueo[fila][columna] != "X":
        print("⚠️ El espacio ya está libre. Intente nuevamente.")
        return contador_hora

    #Vamos a reconstruir el codigo original (puede tener * o no)
    letra = chr(65 + fila)  # Convertir número de fila a letra (A, B, C, ...)
    codigo_base = f"{letra}-{columna + 1}"  # Generar el código de espacio
    if es_espacio_para_moto(fila, columna, filas, columnas, cantidad_motos):
        codigo_base += "*"  # Agregar "*" para motos

    parqueo[fila][columna] = codigo_base
    historial.append((contador_hora, "Salida", "Desconocido", codigo))
    print("Espacio liberado exitosamente.")
    print("\n")

    return contador_hora + 1

#Función para cambiar configuración de la matriz
def cambiar_configuracion():
    print("\nCambiando configuración de parqueo:")
    filas_nuevas = int(input("\nIngresa la nueva cantidad de filas: "))
    columnas_nuevas = int(input("Ingresa la nueva cantidad de espacios por fila: "))
    motos_nuevas = int(input("Ingresa la nueva cantidad de espacios para motos: "))

    nuevo_parqueo = crear_matriz_parqueo(filas_nuevas, columnas_nuevas, motos_nuevas)
    print("\nConfiguración actualizada. El parqueo ha sido reiniciado.")
    print("\n")

    return nuevo_parqueo, filas_nuevas, columnas_nuevas, motos_nuevas, [], 1 #lo hacemos para reiniciar el contador de horas y el historial

#Función para mostrar historial de movimientos
def mostrar_historial(historial):
    print("\nHistorial de movimientos:")
    if not historial:
        print("No hay movimientos registrados.")
        return
    
    print(f"{'Hora':<6} {'Acción':<10} {'Vehículo':<12} {'Código':<8}")
    print("-" * 40)

    for movimiento in historial:
        hora, accion, tipo, codigo = movimiento
        print(f"{hora:<6} {accion:<10} {tipo:<12} {codigo:<8}")
        print("\n")

#MENU PRINCIPAL
historial = []
contador_hora = 1

while True:
    print("MENÚ PRINCIPAL:")
    print("1. Ocupar espacio")
    print("2. Liberar espacio")
    print("3. Mostrar estado del parqueo")
    print("4. Cambiar configuración de parqueo")
    print("5. Mostrar historial de movimientos")
    print("6. Salir")

    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        tipo = input("\nIngrese el tipo de vehículo (carro/moto): ").lower()
        if tipo not in ["carro", "moto"]:
            print("\n❌ Tipo de vehículo inválido. Regresando al menú principal...")
            continue
        contador_hora = ocupar_espacio(parqueo, tipo, historial, contador_hora)

    elif opcion == "2":
        contador_hora = liberar_espacio(parqueo, historial, contador_hora, filas, espacios_por_fila, espacios_moto)

    elif opcion == "3":
        mostrar_parqueo(parqueo)

    elif opcion == "4":
        parqueo, filas, espacios_por_fila, espacios_moto, historial, contador_hora = cambiar_configuracion()

    elif opcion == "5":
        mostrar_historial(historial)

    elif opcion == "6":
        print("Saliendo del programa...")
        break

    else:
        print("Opción no añadida.")
        print("\n")
        continue