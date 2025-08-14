# Función: mostrar_resultados

def _formatea_matriz(m, dec=3, ancho=7):
    """
    Convierte una matriz en un string tabular.
    - Números con decimales: formatea con 'dec' decimales.
    - Cadenas/char: imprime tal cual.
    """
    lineas = []
    for fila in m:
        celdas = []
        for v in fila:
            if isinstance(v, (int, float)):
                celdas.append(f"{v:>{ancho}.{dec}f}")
            else:
                celdas.append(f"{str(v):>{ancho}}")
        lineas.append(" ".join(celdas))
    return "\n".join(lineas)

def mostrar_resultados(actual, diseno, diferencias, clasificacion, volumen_corte, volumen_relleno):
    """
    Imprime matrices y resultados finales de corte y relleno.
    """
    print("=== Elevaciones actuales (m) ===")
    print(_formatea_matriz(actual))
    print("\n=== Elevaciones de diseño (m) ===")
    print(_formatea_matriz(diseno))
    print("\n=== Diferencias Δh = actual - diseño (m) ===")
    print(_formatea_matriz(diferencias))
    print("\n=== Clasificación (C=corte, R=relleno, N=neutro) ===")
    print(_formatea_matriz(clasificacion, dec=0))

    print("\n=== Volúmenes totales ===")
    print(f"Volumen de CORTE   : {volumen_corte:.3f} unidades³")
    print(f"Volumen de RELLENO : {volumen_relleno:.3f} unidades³")


if __name__ == "__main__":
    # Demo rápida
    actual = [[12.5, 12.6], [12.2, 12.4]]
    diseno = [[12.4, 12.4], [12.3, 12.3]]
    dif = [[a - b for a, b in zip(fa, fb)] for fa, fb in zip(actual, diseno)]
    clas = [['C' if v > 0 else 'R' if v < 0 else 'N' for v in f] for f in dif]
    mostrar_resultados(actual, diseno, dif, clas, 10.0, 5.0)
