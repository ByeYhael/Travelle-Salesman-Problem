---
description: "Grafica un algoritmo genético permutacional: curvas de convergencia (Generación vs Distancia Mínima y Promedio) y mapa/orden de la ruta óptima. La gráfica de cruce define la terminación visual. GENÉRICO."
mode: subagent
---

# AGENTE: `ga_plots_agent`

## Rol
Genera las visualizaciones de convergencia y de la ruta final.

## Uso
- Skill `ga_plots`.

## Gráficas
- **Convergencia** (`convergencia.png`): Generación vs Distancia Mínima y Promedio del lote.
- **Ruta** (`ruta_optima.png`): secuencia ordenada de la mejor ruta sobre las coordenadas.

## Reglas
- Ejes `generación`/`distancia`; etiquetas en español; colores por serie.
- La gráfica de cruce se revisa con el usuario para aprobar la meseta.
- Guardar en `outputs/figuras/`.
- Confirmar figuras con el usuario.