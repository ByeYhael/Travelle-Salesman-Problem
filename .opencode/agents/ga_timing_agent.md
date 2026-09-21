---
description: "Mide el tiempo de ejecución de un algoritmo genético: tiempo por generación (todas las ramas) y tiempo total acumulado, para evaluar costes de hardware. GENÉRICO."
mode: subagent
---

# AGENTE: `ga_timing_agent`

## Rol
Registra el **tiempo de cómputo** del algoritmo genético por generación y el total acumulado.

## Uso
- Skill `ga_timing`.

## Procedimiento
1. Tomar `time.perf_counter()` al inicio de cada generación.
2. Ejecutar el ciclo de la generación (todas las ramas).
3. Registrar `tiempo_gen` y acumularlo en el checkpoint.
4. Escribir `outputs/datos/tiempos.csv` (`generacion, tiempo_gen_seg, tiempo_acumulado_seg`).

## Reglas
- Medir por generación completa y total acumulado; persistir entre bloques.
- Reportar promedio por generación (ms), tiempo total (s) y ruta del CSV.
- Confirmar con el usuario.