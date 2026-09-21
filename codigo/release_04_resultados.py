import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "outputs"
FIG = OUT / "figuras"
DATO = OUT / "datos"
CHECKPOINT = DATO / "checkpoint.json"

import release_03_ga as g

ck = g.cargar_checkpoint()
ramas = ck["ramas"]
coords = np.load(DATO / "coords.npy")
ciudades = [row[1] for row in np.loadtxt(
    DATO / "ciudades.csv", delimiter=",", dtype=str, skiprows=1)]

mejor_nombre = min(g.BRANCH_NAMES, key=lambda n: ramas[n]["historial"][-1]["mejor"])
mejor_ruta = ramas[mejor_nombre]["historial"][-1]["ruta"]
dist_ga = g.costo_total(mejor_ruta)
ruta_final = g.mejorar_2opt(mejor_ruta, g.MATRIZ)
dist_final = g.costo_total(ruta_final)
cruces_final = len(g.cruces_de_ruta(ruta_final, coords))

print(f"Mejor rama: {mejor_nombre}")
print(f"Distancia GA (gen {ck['gen_actual']}): {dist_ga:.0f} km")
print(f"Distancia final (tras 2-opt, sin cruces): {dist_final:.0f} km")
print(f"Cruces en ruta final: {cruces_final}")
print("\nRUTA OPTIMA (secuencia ordenada de ciudades):")
secuencia = [ciudades[i] for i in ruta_final]
for i, ciudad in enumerate(secuencia):
    print(f"  {i + 1}. {ciudad}")
print(f"  ... regreso a {secuencia[0]} (ruta cerrada)")
print(f"DISTANCIA TOTAL: {dist_final:.0f} km")

g.plot_convergencia(ramas)
g.plot_mejor_ruta(ramas[mejor_nombre])
fig, ax = plt.subplots(figsize=(12, 8))
xs = [coords[i][0] for i in ruta_final] + [coords[ruta_final[0]][0]]
ys = [coords[i][1] for i in ruta_final] + [coords[ruta_final[0]][1]]
ax.plot(xs, ys, "-o", color="crimson", label=f"Ruta 2-opt: {dist_final:.0f} km")
for idx in ruta_final:
    ax.annotate(ciudades[idx], (coords[idx][0], coords[idx][1]), fontsize=8,
                textcoords="offset points", xytext=(4, 4))
ax.set_title(f"Ruta óptima final — {mejor_nombre} ({dist_final:.0f} km)")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "ruta_optima_final.png", dpi=120)
plt.close(fig)

reporte = {
    "mejor_rama": mejor_nombre,
    "generaciones": ck["gen_actual"],
    "distancia_ga_km": dist_ga,
    "distancia_final_km": dist_final,
    "cruces_finales": cruces_final,
    "ruta": ruta_final,
    "secuencia_ciudades": secuencia,
}
with open(DATO / "reporte_final.json", "w", encoding="utf-8") as f:
    json.dump(reporte, f, ensure_ascii=False, indent=2)

print("\nGuardado: outputs/figuras/convergencia.png, ruta_optima.png, "
      "ruta_optima_final.png, outputs/datos/reporte_final.json")