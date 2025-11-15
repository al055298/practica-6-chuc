# Práctica 6: Modelado de problemas en Ingeniería Civil
Descripción del Proyecto
Marco Teórico

El flujo hidráulico en tuberías es un fenómeno fundamental dentro de la Ingeniería Civil, especialmente en áreas como redes de agua potable, alcantarillado, sistemas contra incendios y transporte de fluidos. Para modelar este flujo, es necesario comprender los conceptos de pérdida de energía, fricción, rugosidad, caudal y presión, así como las ecuaciones que los relacionan.

1. Flujo en Tuberías Presurizadas

Cuando el agua se transporta por una tubería a presión, se produce una pérdida de energía debido a:

La fricción entre el fluido y las paredes internas.
Turbulencia generada por accesorios.
Cambios de dirección o sección.
Esta pérdida se traduce en una reducción del nivel energético del sistema, expresada como pérdida de carga (head loss).

𝐻 = Energia por unidad de peso del fluido

2. Caudal y Velocidad

El caudal volumétrico es:

𝑄 = 𝑉 ⋅ 𝐴

donde:

Q = caudal (m³/s)

V = velocidad del flujo (m/s)

A = área transversal de la tubería (m²)

La tubería se modela como un cilindro:

𝐴 = 𝜋𝐷²/4​

3. Número de Reynolds (Re)

Determina el régimen del flujo:

𝑅𝑒 = 𝜌𝑉𝐷/𝜇

donde:

ρ = densidad del agua
μ = viscosidad
D = diámetro

Clasificación del flujo:

Laminar: Re < 2,000
Transicional: 2,000 < Re < 4,000
Turbulento: Re > 4,000

La mayoría de las tuberías civiles trabajan en turbulencia.

4. Pérdidas por Fricción (Pérdidas Mayores)

Se calculan con la ecuación de Darcy–Weisbach:

ℎ𝑓 = 𝑓 ⋅ 𝐿/𝐷 ⋅ 𝑉²/2𝑔​

donde:

f = factor de fricción
L = longitud de tubería
g = gravedad

5. Rugosidad del Material

Cada tubería tiene una rugosidad interna diferente que afecta el flujo:
Material	Rugosidad 𝑒(m)
PVC	      0.0000015
PEAD	    0.000007
Fierro galvanizado	0.00015
Concreto	0.0003

6. Factor de Fricción – Ecuación de Colebrook–White

Para flujo turbulento, el factor f se obtiene con:

1/𝑓 = − 2log₁₀(𝑒/3.7𝐷 + 2.51/𝑅𝑒√f)

Es una ecuación implícita, por lo que el programa la resuelve mediante iteraciones.

7. Pérdidas Menores

Cada accesorio genera una pérdida adicional:

ℎ𝑚 = 𝐾 ⋅ 𝑉²/2𝑔

Ejemplos de valores K:

Codo 90°: 0.75
Válvula globo: 10

8. Pérdida Total de Energía

La suma de todas las pérdidas del sistema es:
​
htotal​ = hf​ + hm​

Esta pérdida se convierte en requerimiento de presión para que el fluido se mueva.

P = ρghtotal​

Importancia del Modelado en Ingeniería Civil

El modelado de flujo en tuberías permite:

Diseñar redes hidráulicas eficientes.
Seleccionar diámetros adecuados.
Determinar la presión necesaria en bombas.
Reducir costos de operación.
Evitar fallas por presión insuficiente.

Tu programa integra todos estos conceptos en una herramienta didáctica con interfaz gráfica que facilita el análisis hidráulico.
