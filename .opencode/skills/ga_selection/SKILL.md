---
name: ga_selection
description: "Selecciona individuos en base a aptitud en un algoritmo genético permutacional. Métodos genéricos: torneo, ruleta y rank. El ejercicio usa 2: Rank (probabilidad por posición) y Torneo (k=3, gana el de mayor aptitud). Operan sobre la población ordenada mejor->peor. GENÉRICA. Incluye implementación Python."
---

# GA Selection (genérica, permutacional)

Prepara el conjunto de **padres** para reproducción según el **método de selección parametrizado** en el config.

## Métodos genéricos
1. **Torneo**: tomar `k` individuos aleatorios del ranking; gana el de mayor aptitud.
2. **Ruleta**: probabilidad proporcional a la aptitud (muestreo acumulativo).
3. **Rank**: probabilidad por posición `p ∝ (N - rank + 1)`.

> **Ejercicio (2 tipos usados):** `METODO_SELECCION` ∈ {`rank`, `torneo`} con `k = 3`.

## Implementación Python
```python
import random

def seleccionar_torneo(pob, k, rng):
    muestras = rng.sample(pob, k)
    return max(muestras, key=lambda x: x["fitness"])

def seleccionar_rank(pob, rng):
    n = len(pob)
    total = n * (n + 1) / 2
    r = rng.uniform(0, total)
    acum = 0
    for i, x in enumerate(pob):
        acum += n - i
        if acum >= r:
            return x

def seleccionar_ruleta(pob, rng):
    total = sum(x["fitness"] for x in pob)
    r = rng.uniform(0, total)
    acum = 0
    for x in pob:
        acum += x["fitness"]
        if acum >= r:
            return x

def preparar_padres(pob, metodo, n_padres, rng, k=3):
    sel = {"torneo": lambda: seleccionar_torneo(pob, k, rng),
           "rank": lambda: seleccionar_rank(pob, rng),
           "ruleta": lambda: seleccionar_ruleta(pob, rng)}[metodo]
    return [sel() for _ in range(n_padres)]
```

## Reglas
- Operar siempre sobre la población **ordenada mejor → peor**.
- Elegir el método en el `config` (`METODO_SELECCION`: `rank` o `torneo` en este ejercicio).
- NO cruzar todavía; solo preparar padres.
- Confirmar con el usuario antes de cruzar.