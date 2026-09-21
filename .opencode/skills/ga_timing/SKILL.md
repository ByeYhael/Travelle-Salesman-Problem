---
name: ga_timing
description: "Mide el tiempo de ejecución de un algoritmo genético de forma sencilla: tiempo por generación (todas las ramas), tiempo acumulado y total. Guarda un CSV (generacion, tiempo_gen, tiempo_acumulado) para evaluar costes de hardware. GENÉRICA. Incluye implementación Python."
---

# GA Timing (genérica)

Registra el **coste de cómputo** del algoritmo para evaluar costes de hardware.

## Procedimiento genérico
1. Al iniciar cada generación, tomar `t0 = time.perf_counter()`.
2. Ejecutar el ciclo completo (selección → cruce → mutación → elitismo → evaluación) de **todas las ramas**.
3. Al terminar, `t_gen = time.perf_counter() - t0` y **acumular** en una lista persistente (checkpoint).
4. Al guardar, escribir CSV con columnas:
   `generacion, tiempo_gen_seg, tiempo_acumulado_seg`.

## Implementación Python
```python
import time

def avanzar_con_tiempo(checkpoint, avanzar):
    t0 = time.perf_counter()
    avanzar(checkpoint)                      # 1 generación (todas las ramas)
    checkpoint["tiempos"].append(time.perf_counter() - t0)

def escribir_tiempos(tiempos, ruta_csv):
    acum = 0.0
    with open(ruta_csv, "w", encoding="utf-8") as f:
        f.write("generacion,tiempo_gen_seg,tiempo_acumulado_seg\n")
        for i, t in enumerate(tiempos, start=1):
            acum += t
            f.write(f"{i},{t:.6f},{acum:.6f}\n")
```

## Reglas
- Medir por **generación completa** (todas las ramas) y **total acumulado**.
- Persistir los tiempos entre ejecuciones por bloques (acumular en checkpoint).
- Guardar en `outputs/datos/tiempos.csv`.
- Reportar: promedio por generación, total, y ubicación del CSV.
- Confirmar con el usuario.