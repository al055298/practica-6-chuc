# Función: calcular_volumenes
def calcular_volumenes(diferencias, area_celda):
    """
    Recorre la matriz de diferencias y suma:
      volumen_corte   = sum(delta * area) para delta > 0
      volumen_relleno = sum(|delta| * area) para delta < 0
    Devuelve (volumen_corte, volumen_relleno) en unidades cúbicas del área ingresada.
    """
    if not isinstance(area_celda, (int, float)) or area_celda <= 0:
        raise ValueError("area_celda debe ser un número positivo.")

    if not isinstance(diferencias, list) or not all(isinstance(f, list) for f in diferencias):
        raise TypeError("diferencias debe ser una matriz (lista de listas).")

    corte = 0.0
    relleno = 0.0

    for fila in diferencias:
        for delta in fila:
            delta = float(delta)
            if delta > 0:
                corte += delta * area_celda
            elif delta < 0:
                relleno += (-delta) * area_celda  # abs(delta)

    return corte, relleno


if __name__ == "__main__":
    dif = [[0.2, -0.1], [0.0, 0.05]]
    print(calcular_volumenes(dif, 25.0))
