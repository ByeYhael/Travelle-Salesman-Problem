---
name: ga_orchestrator
description: "Orquesta un algoritmo genético permutacional de forma procedural y controlada. Bucle: codificar elementos, generar lote inicial (permutaciones), evaluar aptitud (ordenar mejor->peor), terminar visualmente con gráfica de cruce, o seleccionar (2 métodos) -> cruzar (N=lote/2) -> mutar los N_MUTAR peores de la descendencia (fracción del lote) -> elitismo (pool único) -> evaluar. Reordenar antes de cruzar, antes de mutar y antes del elitismo. GENÉRICA."
---

# GA Orchestrator (genérica, permutacional)

Orquesta todo el pipeline de forma **procedural y controlada**, preguntando al usuario antes de cada transición.

## Bucle principal
```
1. Codificar los elementos                (ga_encoding)
2. Generar lote inicial (permutaciones)   (ga_population_gen)
3. Evaluar aptitud (ordenar mejor→peor)   (ga_fitness_eval)
4. Terminación visual (gráfica de cruce)  (ga_convergence + ga_plots)
   ├─ Sí (meseta) → TERMINAR + graficar
   └─ No → 5. seleccionar (2 métodos)     (ga_selection)
            6. cruzar (operador, N=lote/2)(ga_crossover)
            7. mutar los N_MUTAR peores    (ga_mutation)
            8. elitismo (pool completo)    (ga_elitism)
            9. evaluar aptitud             (ga_fitness_eval)
           10. regresar a paso 4
```

## Dimensiones del ejercicio
- **Selección (2):** `rank`, `torneo` (k=3).
- **Cruce (2):** `OX`, `PMX` (N = lote/2).
- **Mutación (2):** `swap`, `inversion` (solo los `N_MUTAR` peores de la descendencia).
- **Elitismo (1):** `pool` completo (único tipo).
- Total: **2 × 2 × 2 = 8 ramas independientes**, cada una con su propia población.

## Disciplina de reordenamiento
- **Antes del cruce**: la población/padres se ordenan mejor → peor.
- **Antes de mutar**: la descendencia se vuelve a ordenar mejor → peor (los peores al final).
- **Antes del elitismo / reemplazo**: el pool (padres + descendencia) se vuelve a ordenar.

## Parámetros (config)
- `ELEMENTOS` (lista de N elementos), `LOTE`, `SEMILLA`, `MATRIZ_COSTES`.
- `METODO_SELECCION` (2), `OPERADOR_CRUCE` (2), `OPERADOR_MUTACION` (2), `P_CROSS`, `FRACCION_MUT` (→ `N_MUTAR = int(FRACCION_MUT * LOTE)`).
- `PATIENCE` (generaciones para sugerir meseta).

## Reglas
- Procedural: orden estricto (selección → cruce → mutación → elitismo); controlado: preguntar antes de cada transición.
- Delegar cada fase; NO implementar la lógica directamente.
- **Re-evaluar y reordenar siempre tras modificar cada población**.
- Terminación aprobada por el usuario con la gráfica de cruce.