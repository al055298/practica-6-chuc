from cargar_datos import cargar_datos
from calcular_diferencias import calcular_diferencias
from clasificar_corte_relleno import clasificar_corte_relleno
from calcular_volumenes import calcular_volumenes
from mostrar_resultados import mostrar_resultados

# Función: modelo_corte_relleno
def modelo_corte_relleno(area_celda=25.0, tol_neutro=0.0):
    """
    Flujo principal:
      1) Cargar matrices actual y diseño
      2) Calcular diferencias
      3) Clasificar celdas
      4) Calcular volúmenes totales
      5) Mostrar resultados
    Parámetros:
      - area_celda: área de cada celda (m^2, por ej. 5m x 5m => 25.0)
      - tol_neutro: tolerancia para considerar delta ~ 0 como 'N'
    """
    actual, diseno = cargar_datos()
    diferencias = calcular_diferencias(actual, diseno)
    clasificacion = clasificar_corte_relleno(diferencias, tol=tol_neutro)
    vol_corte, vol_relleno = calcular_volumenes(diferencias, area_celda)
    mostrar_resultados(actual, diseno, diferencias, clasificacion, vol_corte, vol_relleno)
    return vol_corte, vol_relleno


if __name__ == "__main__":
    modelo_corte_relleno(area_celda=25.0, tol_neutro=0.001)
