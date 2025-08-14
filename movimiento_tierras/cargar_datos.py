# Función: cargar_datos
def cargar_datos():
    """
    Devuelve dos matrices: (actual, diseno) con elevaciones en metros.
    Se usan datos fijos y simples para la práctica (pueden cambiarse).
    """
    actual = [
        [12.5, 12.6, 12.8, 13.0],
        [12.2, 12.4, 12.7, 12.9],
        [12.0, 12.1, 12.3, 12.6]
    ]

    diseno = [
        [12.4, 12.4, 12.6, 12.8],
        [12.3, 12.3, 12.5, 12.7],
        [12.1, 12.1, 12.2, 12.4]
    ]

    return actual, diseno


if __name__ == "__main__":
    a, d = cargar_datos()
    print("Actual:")
    for f in a: print(f)
    print("Diseño:")
    for f in d: print(f)
