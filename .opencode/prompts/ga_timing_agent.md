# ga_timing_agent — Prompt (genérico)

Mide el tiempo de ejecución del AG por generación (todas las ramas) y el total acumulado, para evaluar costes de hardware. Registra tiempo_gen y tiempo_acumulado, guarda `outputs/datos/tiempos.csv` y reporta promedio por generación (ms) y total (s); confirma.