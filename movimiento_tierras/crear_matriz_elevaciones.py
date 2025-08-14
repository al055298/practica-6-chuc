# Función: crear_matriz_elevaciones
def crear_matriz_elevaciones(filas, columnas, valor_inicial=0):
    """
    Crea una matriz (lista de listas) de tamaño filas x columnas
    con todas las celdas inicializadas a valor_inicial.
    """
    if not isinstance(filas, int) or not isinstance(columnas, int):
        raise TypeError("filas y columnas deben ser enteros.")
    if filas <= 0 or columnas <= 0:
        raise ValueError("filas y columnas deben ser > 0.")

    return [[valor_inicial for _ in range(columnas)] for _ in range(filas)]


if __name__ == "__main__":
    m = crear_matriz_elevaciones(3, 4, 12.5)
    for fila in m:
        print(fila)
