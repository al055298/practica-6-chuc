# Función: calcular_diferencias

def _dimensiones_iguales(m1, m2):
    return (
        isinstance(m1, list) and isinstance(m2, list) and
        len(m1) == len(m2) and
        all(isinstance(f, list) for f in m1) and
        all(isinstance(f, list) for f in m2) and
        all(len(m1[i]) == len(m2[i]) for i in range(len(m1)))
    )

def calcular_diferencias(actual, diseno):
    """
    Calcula delta h = actual - diseno, celda a celda.
    Devuelve una matriz de mismas dimensiones.
    """
    if not _dimensiones_iguales(actual, diseno):
        raise ValueError("Las matrices actual y diseno deben tener las mismas dimensiones.")

    filas = len(actual)
    cols = len(actual[0]) if filas else 0

    dif = []
    for i in range(filas):
        fila = []
        for j in range(cols):
            fila.append(float(actual[i][j]) - float(diseno[i][j]))
        dif.append(fila)
    return dif


if __name__ == "__main__":
    a = [[12.5, 12.6],[12.2, 12.4]]
    d = [[12.4, 12.4],[12.3, 12.3]]
    for f in calcular_diferencias(a, d):
        print(f)
