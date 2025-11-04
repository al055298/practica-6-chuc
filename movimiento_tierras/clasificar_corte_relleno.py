# Función: clasificar_corte_relleno

def clasificar_corte_relleno(diferencias, tol=0.0):
    """
    Clasifica cada celda de la matriz de diferencias como 'C' (corte),
    'R' (relleno) o 'N' (neutro) basándose en una tolerancia.
    Devuelve una matriz de clasificaciones de las mismas dimensiones.
    """
    if not isinstance(diferencias, list) or not all(isinstance(f, list) for f in diferencias):
        raise TypeError("diferencias debe ser una matriz (lista de listas).")

    filas = len(diferencias)
    if filas == 0:
        return []
    cols = len(diferencias[0])

    clasificacion = []
    for i in range(filas):
        fila_clasificacion = []
        for j in range(cols):
            delta = float(diferencias[i][j])
            if delta > tol:
                fila_clasificacion.append('C')
            elif delta < -tol:
                fila_clasificacion.append('R')
            else:
                fila_clasificacion.append('N')
        clasificacion.append(fila_clasificacion)
    return clasificacion


if __name__ == "__main__":
    dif = [[0.2, -0.1, 0.05], [-0.005, 0.0, 0.1]]
    print("Diferencias:")
    for f in dif:
        print(f)
    print("\nClasificación (tol=0.0):")
    for f in clasificar_corte_relleno(dif, tol=0.0):
        print(f)
    print("\nClasificación (tol=0.01):")
    for f in clasificar_corte_relleno(dif, tol=0.01):
        print(f)
