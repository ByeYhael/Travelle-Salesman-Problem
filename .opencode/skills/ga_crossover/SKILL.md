---
name: ga_crossover
description: "Cruza (reproduce) individuos de un algoritmo genético permutacional con 2 operadores de orden: Order Crossover (OX) que preserva el orden relativo, y PMX (Partially Mapped Crossover) con mapeo parcial. N = lote/2 por generación; luego se reordena mejor->peor. GENÉRICA. Incluye implementación Python."
---

# GA Crossover (genérica, permutacional)

Produce descendencia a partir de los padres seleccionados con **operadores para permutaciones** que respetan la validez (sin duplicados).

## Operadores
1. **Order Crossover (OX)**: copia un segmento de `P1` en `H1`; el resto se rellena con los genes de `P2` en orden, respetando el orden relativo.
2. **PMX (Partially Mapped Crossover)**: intercambia el segmento y repara duplicados con un mapa de correspondencias.

## Parámetros
- `p_cross` (probabilidad de cruzar; si no, clonar padres).
- **N cruces por generación = lote/2**.
- Población **ordenada mejor → peor** antes de cruzar; **reordenada** después.

## Implementación Python
```python
import random

def ox(p1, p2, rng):
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    h1 = [None] * n
    h1[a:b] = p1[a:b]
    pos = b
    for g in p2[b:] + p2[:b]:
        if g not in h1:
            h1[pos % n] = g
            pos += 1
    h2 = [None] * n
    h2[a:b] = p2[a:b]
    pos = b
    for g in p1[b:] + p1[:b]:
        if g not in h2:
            h2[pos % n] = g
            pos += 1
    return h1, h2

def pmx(p1, p2, rng):
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    h1 = p1[:]
    h1[a:b] = p2[a:b]
    mapa_h1 = {p2[i]: p1[i] for i in range(a, b)}
    for i in list(range(a)) + list(range(b, n)):
        while h1[i] in mapa_h1:
            h1[i] = mapa_h1[h1[i]]
    h2 = p2[:]
    h2[a:b] = p1[a:b]
    mapa_h2 = {p1[i]: p2[i] for i in range(a, b)}
    for i in list(range(a)) + list(range(b, n)):
        while h2[i] in mapa_h2:
            h2[i] = mapa_h2[h2[i]]
    return h1, h2

def cruzar(p1, p2, operador, p_cross, rng):
    if rng.random() < p_cross:
        fn = {"ox": ox, "pmx": pmx}[operador]
        return fn(p1, p2, rng)
    return p1[:], p2[:]
```

## Reglas
- Elegir el operador en el `config` (`OPERADOR_CRUCE`).
- **Reordenar mejor → peor** los padres antes de cruzar y la descendencia después de cruzar.
- Tras la cruza → reordenar → mutar los peores → elitismo.
- Confirmar con el usuario.