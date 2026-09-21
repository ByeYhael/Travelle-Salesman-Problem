---
name: ga_mutation
description: "Mutación en un algoritmo genético permutacional: cada generación se seleccionan los N_MUTAR individuos de PEOR aptitud de la descendencia (fracción FRACCION_MUT del lote) y se les aplica 1 operación del operador único del lote: Swap (intercambia 2 posiciones) o Inversión (invierte un segmento). Mantiene la validez de la permutación. GENÉRICA. Incluye implementación Python."
---

# GA Mutation (genérica, permutacional)

Aplica mutación sobre la **descendencia** para mantener diversidad genética. Por regla del ejercicio: **solo se muta una fracción del lote por generación** (típicamente el 10% = los `N_MUTAR` individuos de peor aptitud).

## Procedimiento genérico
1. Tras el **cruce**, evaluar y **ordenar** la descendencia mejor → peor.
2. Seleccionar los `N_MUTAR = int(FRACCION_MUT * LOTE)` individuos de **PEOR aptitud** (los últimos del orden).
3. Aplicar a cada uno **1 sola operación** del operador único del lote (`OPERADOR_MUTACION`).
4. **Re-evaluar y reordenar** la descendencia tras mutar.

## Operadores (1 operación por individuo)
1. **Swap Mutation**: intercambia 2 posiciones al azar.
2. **Inversion Mutation**: invierte el orden de un segmento contiguo al azar.

## Parámetros
- `FRACCION_MUT` (fracción del lote a mutar; `N_MUTAR = int(FRACCION_MUT * LOTE)`), config.
- `OPERADOR_MUTACION` (único por lote: `swap` o `inversion`), config.

## Implementación Python
```python
import random

def mutar_swap(ruta, rng):
    i, j = rng.sample(range(len(ruta)), 2)
    ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

def mutar_inversion(ruta, rng):
    i, j = sorted(rng.sample(range(len(ruta)), 2))
    ruta[i:j + 1] = reversed(ruta[i:j + 1])
    return ruta

def mutar_peores(descendencia_ordenada, operador, n_mutar, rng):
    fn = {"swap": mutar_swap, "inversion": mutar_inversion}[operador]
    for ind in descendencia_ordenada[-n_mutar:]:
        ind["ruta"] = fn(ind["ruta"][:], rng)
    return descendencia_ordenada
```

## Reglas
- Cada lote (rama) usa **un solo operador** de mutación.
- Aplicar a los `N_MUTAR` **peores** de la descendencia, ya ordenada.
- **Reordenar** la descendencia antes y después de mutar; respetar la permutación (sin duplicados).
- Tras la mutación → elitismo (reordenar de nuevo) → evaluar aptitud.
- Confirmar con el usuario.