---
name: ga_encoding
description: "Codifica el dominio de un algoritmo genético permutacional. Mapeo bidireccional entre la lista de N elementos genéricos y sus índices de permutación [0..N-1]. Cromosoma = permutación de índices sin repetición. GENÉRICA (parámetro N en config). Incluye implementación Python."
---

# GA Encoding (genérica, permutacional)

Define la codificación del dominio antes de generar la población. Se parametriza en un `config` (`ELEMENTOS`).

## Especificación genérica
- Cromosoma: permutación de los índices `[0, 1, ..., N-1]` de los `N` elementos (sin repetición).
- Mapeo bidireccional `índice ↔ elemento`:
```
índice   = ELEMENTOS.index(elemento)
elemento = ELEMENTOS[índice]
```
- Espacio de búsqueda = `N!` permutaciones válidas.
- El coste de una ruta se evalúa contra una `MATRIZ_COSTES[N][N]` genérica.

## Implementación Python
```python
def indice_de(elemento, elementos):
    return elementos.index(elemento)

def elemento_de(indice, elementos):
    return elementos[indice]

def generar_cromosoma(n, rng):
    return rng.sample(range(n), n)   # permutación válida de índices
```

## Reglas
- NO generar población aquí; solo definir la codificación.
- Documentar fórmula y tabla `índice ↔ elemento` (parcial).
- Confirmar con el usuario antes de continuar.