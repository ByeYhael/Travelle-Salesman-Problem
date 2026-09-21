---
name: ga_elitism
description: "Aplica elitismo por pool completo en un algoritmo genético: une la población de padres con la descendencia, evalúa y elige los LOTE mejores como nueva generación. Único tipo de elitismo del ejercicio. GENÉRICA. Incluye implementación Python."
---

# GA Elitism (genérica, permutacional)

Conserva el mejor material genético uniendo padres y descendencia, y eligiendo los `LOTE` mejores.

## Procedimiento genérico
1. **Unir** la población de padres con la descendencia (ya mutada en sus `N_MUTAR` peores).
2. **Reordenar** el pool y **evaluar** la aptitud de todos (padres + hijos).
3. **Elegir** los `LOTE` mejores como nueva generación.
4. Ordenar la nueva generación **mejor → peor**.

> El ejercicio usa **un solo tipo de elitismo: pool completo** (se une todo y se filtran los mejores). No se usa élite fija.

## Implementación Python
```python
from ga_fitness_eval import evaluar_y_ordenar

def elitismo_pool(padres, hijos, lote, matriz_costes):
    pool = padres + hijos
    pool = evaluar_y_ordenar(pool, matriz_costes)
    return pool[:lote]
```

## Reglas
- Conservar los `LOTE` mejores sin alterar su orden.
- Tras el elitismo, evaluar aptitud y regresar al bucle.
- Confirmar con el usuario.