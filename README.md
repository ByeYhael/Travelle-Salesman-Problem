# Algoritmos Genéticos para el Problema del Viajero (TSP)

Resolver el **Problema del Viajero (TSP)** con 18 ciudades de América, determinando la ruta cerrada de distancia mínima que visita cada ciudad exactamente una vez y regresa al punto de partida, mediante un **Algoritmo Genético permutacional**.

## Resultado final

- **Mejor rama:** `rank_PMX_inversion`
- **Distancia (gen 200):** 24 571 km — **0 cruces visuales**, óptima local bajo 2-opt
- **Reducción desde gen 0:** ~50% (de ~49 684 km)

**Ruta óptima:** Montevideo → Brasilia → Bogotá → Caracas → Boston → New York → Washington D.C. → Miami → Mérida → Monterrey → Guadalajara → Ciudad de México → San Salvador → Managua → Panamá → Quito → Mendoza → Buenos Aires.

## Estructura del proyecto

```
.
├── .opencode/                 # Ecosistema modular (Agentes / Skills / Prompts)
│   ├── agents/                #   QUIÉN ejecuta cada fase
│   ├── skills/                #   CÓMO (funciones 100% genéricas)
│   └── prompts/               #   QUÉ (parámetros y datos del problema)
├── codigo/                    # Scripts de ejecución
│   ├── release_02_datos.py    #   Coordenadas + matriz de distancias (geopy)
│   ├── release_03_ga.py       #   Pipeline del algoritmo genético (8 ramas)
│   ├── release_04_resultados.py
│   └── release_04_comparativa.py
├── outputs/                   # Resultados (ignorados por git)
│   ├── datos/                 #   CSV, npy, checkpoint, reportes
│   └── figuras/               #   Gráficas de convergencia y rutas
├── INFORME_COMPORTAMIENTO_GA.md
├── README.md
└── .gitignore
```

## Diseño del algoritmo (diseño corregido)

| Dimensión | Valores |
|---|---|
| Selección (2) | Rank, Torneo (k=3) |
| Cruce (2) | OX (orden), PMX (mapeo parcial) — `p_cross = 0.85` |
| Mutación (2) | Swap, Inversión — **solo los 2 peores de la descendencia** (10% del lote, 1 operación) |
| Elitismo (1) | Pool completo (único tipo) |
| Terminación | Meseta visual (15 generaciones sin mejora), aprobada por el usuario |

**Total: 8 ramas independientes** (2×2×2), cada una con su propia población. Parámetros: lote = 20, semilla = 42.

## Requisitos

- Python 3.10+
- `geopy`, `numpy`, `matplotlib`, `pandas`

```bash
pip install geopy numpy matplotlib pandas
```

## Ejecución

```bash
# 1. Datos (coordenadas de las 18 ciudades + matriz geodésica de distancias)
python3 codigo/release_02_datos.py

# 2. Algoritmo genético (en bloques; re-ejecuta y aprueba la meseta visual)
python3 codigo/release_03_ga.py --generaciones 100
python3 codigo/release_03_ga.py --generaciones 100

# 3. Resultados finales (ruta, distancia, gráficas, reporte)
python3 codigo/release_04_resultados.py
python3 codigo/release_04_comparativa.py   # comparativa visual de rutas
```

## Interpretación de resultados (`outputs/datos/`)

- `matriz_distancias.csv` — distancias geodésicas (km) entre todas las ciudades.
- `historial.csv` — mejor y promedio por rama y generación.
- `tiempos.csv` — tiempo por generación y total (costes de hardware).
- `reporte_final.json` — resumen estructurado del resultado.
- `figuras/convergencia.png` — curvas de convergencia de las 8 ramas.
- `figuras/ruta_optima_final.png` — mapa de la ruta óptima (sin cruces).

## Versionado (releases)

Guardado por versiones con tags SemVer: `v0.1.0` (estructura del ecosistema) → `v0.2.0` (datos) → `v0.3.0` (ejecución del AG) → `v0.4.0` (resultados). Ver el agente/skill `git_release` en `.opencode/`.