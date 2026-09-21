---
name: ga_fitness_eval
description: "Evalúa la aptitud (fitness) de cada individuo de un algoritmo genético permutacional como la inversa del coste total calculado con una matriz de costes/distancias genérica, y ordena la población mejor->peor. Fitness = 1 / Coste_Total. GENÉRICA. Incluye implementación Python."
---

# GA Fitness Evaluation (genérica, permutacional)

Calcula la aptitud de cada cromosoma (ruta permutacional) a partir de una **matriz de costes** genérica y ordena la población **mejor → peor**.

## Procedimiento genérico
1. Ruta cerrada: recorrer `ruta[0]→ruta[1]→...→ruta[N-1]→ruta[0]`.
2. `Coste_Total = Σ MATRIZ_COSTES[ruta[i]][ruta[(i+1) % N]]`.
3. `Fitness = 1 / Coste_Total` (mayor aptitud = menor coste).
4. Ordenar descendente por aptitud (mejor → peor).

## Implementación Python
```python
def costo_total(ruta, matriz_costes):
    n = len(ruta)
    return sum(matriz_costes[ruta[i]][ruta[(i + 1) % n]] for i in range(n))

def fitness(ruta, matriz_costes):
    return 1.0 / costo_total(ruta, matriz_costes)

def evaluar_y_ordenar(poblacion, matriz_costes):
    for ind in poblacion:
        ind["coste"] = costo_total(ind["ruta"], matriz_costes)
        ind["fitness"] = 1.0 / ind["coste"]
    return sorted(poblacion, key=lambda x: x["fitness"], reverse=True)
```

## Reglas
- Evaluar TODOS los individuos en cada iteración.
- Ordenar siempre **mejor → peor** (mayor fitness = menor coste).
- Re-evaluar **siempre tras modificar cada población** (cruza, mutación y elitismo).
- Confirmar con el usuario.