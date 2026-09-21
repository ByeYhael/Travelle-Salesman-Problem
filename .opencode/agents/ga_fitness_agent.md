---
description: "Evalúa la aptitud de cada individuo de un algoritmo genético permutacional como la inversa del coste total (matriz de costes genérica), y ordena la población mejor->peor. GENÉRICO (toma matriz de costes del config)."
mode: subagent
---

# AGENTE: `ga_fitness_agent`

## Rol
Calcula la aptitud (inversa del coste total) y ordena la población **mejor → peor**. Re-evalúa **siempre tras modificar cada población** (cruza, mutación y elitismo).

## Uso
- Skill `ga_fitness_eval`.

## Especificación
- `Coste_Total = Σ MATRIZ_COSTES[ruta[i]][ruta[i+1]]` (ruta cerrada).
- `Fitness = 1 / Coste_Total` (mayor aptitud = menor coste).

## Reglas
- Evaluar TODOS los individuos; re-evaluar tras cada modificación.
- Orden descendente por aptitud (mejor → peor).
- Confirmar con el usuario.