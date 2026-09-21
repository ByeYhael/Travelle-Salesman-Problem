---
name: ga_convergence
description: "Determina el criterio de terminación de un algoritmo genético de forma VISUAL con la gráfica de cruce (aptitud/distancia vs generación). El usuario aprueba detener cuando la curva forma meseta. Sugiere meseta si el mejor no mejora en las últimas patience generaciones. GENÉRICA. Incluye implementación Python."
---

# GA Convergence / Terminación (genérica, permutacional)

El criterio de terminación se decide **visualmente** con la gráfica de cruce, no con un umbral fijo.

## Procedimiento genérico
1. Acumular por generación la **mejor distancia** (y promedio del lote).
2. Graficar distancia vs generación.
3. El usuario **aprueba detener** cuando la curva **forma meseta / se estabiliza**.
4. Copiloto opcional: sugerir meseta si el mejor no mejora en las últimas `patience` generaciones.

## Implementación Python
```python
def es_meseta(mejores, patience, tol=1e-3):
    if len(mejores) < patience:
        return False
    ventana = mejores[-patience:]
    return (max(ventana) - min(ventana)) < tol
```

## Reglas
- Terminación basada en la **gráfica de cruce**, aprobada por el usuario.
- Reporte procedural: generación, mejor, promedio.
- Si no hay meseta → regresar al bucle (selección → cruza → mutación → elitismo).
- Entregar el mejor individuo final + gráficas.