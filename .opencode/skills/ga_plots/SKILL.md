---
name: ga_plots
description: "Grafica un algoritmo genético permutacional: curva de convergencia (Generación vs Distancia Mínima y Promedio) y mapa de la ruta óptima. La gráfica de cruce define la terminación visual. GENÉRICA. Incluye implementación Python."
---

# GA Plots (genérica, permutacional)

Grafica la convergencia y la ruta final para comparar y decidir la terminación.

## Gráficas
1. **Convergencia** (`convergencia.png`): Generación vs Distancia Mínima y Promedio del lote.
2. **Ruta óptima** (`ruta_optima.png`): la mejor ruta trazada sobre las coordenadas de los elementos.

## Implementación Python
```python
import matplotlib.pyplot as plt

def graficar_convergencia(historial, ruta_out):
    gen = [h["generacion"] for h in historial]
    mejor = [h["mejor_distancia"] for h in historial]
    prom = [h["promedio_distancia"] for h in historial]
    plt.plot(gen, mejor, label="Mejor")
    plt.plot(gen, prom, label="Promedio")
    plt.xlabel("Generación")
    plt.ylabel("Distancia")
    plt.legend()
    plt.grid(True)
    plt.savefig(ruta_out)

def graficar_ruta(mejor_ruta, coords, nombres, ruta_out):
    xs = [coords[i][0] for i in mejor_ruta] + [coords[mejor_ruta[0]][0]]
    ys = [coords[i][1] for i in mejor_ruta] + [coords[mejor_ruta[0]][1]]
    plt.plot(xs, ys, "-o")
    for i in mejor_ruta:
        plt.text(coords[i][0], coords[i][1], str(i))
    plt.title("Ruta óptima")
    plt.savefig(ruta_out)
```

## Reglas
- Ejes: `generación` y `distancia`; etiquetas y leyendas en español.
- Colores distintos por serie.
- Guardar en `outputs/figuras/`.
- La gráfica de cruce se revisa con el usuario para aprobar la terminación.