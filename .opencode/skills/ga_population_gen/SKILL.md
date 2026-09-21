---
name: ga_population_gen
description: "Genera o adquiere la población inicial (lote) de un algoritmo genético permutacional: LOTE permutaciones aleatorias válidas de los índices [0..N-1] sin elementos duplicados, con semilla fija. GENÉRICA (parámetros LOTE, SEMILLA, N en config). Incluye implementación Python."
---

# GA Population Generation (genérica, permutacional)

Genera la **población inicial (lote)** directamente, sin pool ni dataset previo.

## Procedimiento genérico
1. Con `SEMILLA` fija, crear `LOTE` permutaciones aleatorias de `[0, 1, ..., N-1]`.
2. Cada cromosoma es una **permutación válida** (cada índice aparece exactamente una vez).
3. La población inicial queda **sin ordenar** (se ordena en aptitud).

## Implementación Python
```python
import random

def generar_poblacion(n, lote, semilla):
    rng = random.Random(semilla)
    return [rng.sample(range(n), n) for _ in range(lote)]
```

## Reglas
- Cada cromosoma sin duplicados (permutación válida).
- Población inicial **sin ordenar**.
- NO evaluar aptitud aquí.
- Confirmar con el usuario antes de evaluar aptitud.