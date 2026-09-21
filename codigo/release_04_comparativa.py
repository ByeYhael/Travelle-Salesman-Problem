import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent.parent
FIG = BASE / "outputs" / "figuras"
DATO = BASE / "outputs" / "datos"

import release_03_ga as g

ck = g.cargar_checkpoint()
coords = np.load(DATO / "coords.npy")
ciudades = [row[1] for row in np.loadtxt(
    DATO / "ciudades.csv", delimiter=",", dtype=str, skiprows=1)]

ramas = {
    "ganadora_rank_PMX_inv": "rank_PMX_inversion",
    "torneo_PMX_inv_2opt": "torneo_PMX_inversion",
}

fig, ejes = plt.subplots(1, 2, figsize=(18, 8))
colores = {"ganadora_rank_PMX_inv": "crimson",
           "torneo_PMX_inv_2opt": "royalblue"}

reporte = {}
for etiqueta, nombre in ramas.items():
    ruta_ga = ck["ramas"][nombre]["historial"][-1]["ruta"]
    ruta = g.mejorar_2opt(ruta_ga, g.MATRIZ)
    dist = g.costo_total(ruta)
    cruces = len(g.cruces_de_ruta(ruta, coords))
    reporte[etiqueta] = {"rama": nombre, "distancia_km": dist, "cruces": cruces,
                         "ruta": ruta, "ciudades": [ciudades[i] for i in ruta]}
    xs = [coords[i][0] for i in ruta] + [coords[ruta[0]][0]]
    ys = [coords[i][1] for i in ruta] + [coords[ruta[0]][1]]
    ejes[0 if etiqueta.startswith("ganadora") else 1].plot(
        xs, ys, "-o", color=colores[etiqueta],
        label=f"{nombre} — {dist:.0f} km ({cruces} cruces)")
    for idx in ruta:
        ejes[0 if etiqueta.startswith("ganadora") else 1].annotate(
            str(idx), (coords[idx][0], coords[idx][1]), fontsize=7,
            textcoords="offset points", xytext=(3, 3))

for ax, titulo in zip(ejes, ["Ganadora: rank_PMX_inversion", "Comparativa: torneo_PMX_inversion (2-opt)"]):
    ax.set_title(titulo)
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)
    ax.legend(fontsize=9)

fig.suptitle("Comparativa visual de rutas (ambas localmente optimas bajo 2-opt)", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(FIG / "ruta_comparativa.png", dpi=120)
plt.close(fig)

print(f"torneo_PMX_inversion tras 2-opt: {reporte['torneo_PMX_inv_2opt']['distancia_km']:.0f} km, {reporte['torneo_PMX_inv_2opt']['cruces']} cruces")
print("Secuencia torneo_PMX_inversion (24 012 km):")
for i, c in enumerate(reporte["torneo_PMX_inv_2opt"]["ciudades"], 1):
    print(f"  {i}. {c}")
print("Secuencia ganadora (24 571 km):")
for i, c in enumerate(reporte["ganadora_rank_PMX_inv"]["ciudades"], 1):
    print(f"  {i}. {c}")

with open(DATO / "ruta_torneo_24012.json", "w", encoding="utf-8") as f:
    json.dump(reporte["torneo_PMX_inv_2opt"], f, ensure_ascii=False, indent=2)
print(f"\nGuardado: {FIG / 'ruta_comparativa.png'} y {DATO / 'ruta_torneo_24012.json'}")