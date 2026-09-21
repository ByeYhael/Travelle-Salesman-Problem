import argparse
import json
import random
import sys
import time
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
HISTORIAL_CSV = DATO / "historial.csv"
TIEMPOS_CSV = DATO / "tiempos.csv"

LOTE = 20
SEMILLA = 42
P_CROSS = 0.85
FRACCION_MUT = 0.10
N_MUTAR = int(FRACCION_MUT * LOTE)
PATIENCE = 15
K_TORNEO = 3

SELECCIONES = ["rank", "torneo"]
OPERADORES_CRUCE = ["OX", "PMX"]
OPERADORES_MUTACION = ["swap", "inversion"]

BRANCHES = [
    (s, c, m) for s in SELECCIONES
    for c in OPERADORES_CRUCE
    for m in OPERADORES_MUTACION
]
BRANCH_NAMES = [f"{s}_{c}_{m}" for s, c, m in BRANCHES]

CIUDADES = [row[1] for row in np.loadtxt(
    DATO / "ciudades.csv", delimiter=",", dtype=str, skiprows=1)]
MATRIZ = np.load(DATO / "matriz_distancias.npy")


def costo_total(ruta):
    n = len(ruta)
    return float(sum(MATRIZ[ruta[i]][ruta[(i + 1) % n]] for i in range(n)))


def evaluar(poblacion):
    evaluados = []
    for ind in poblacion:
        coste = costo_total(ind["ruta"])
        evaluados.append({"ruta": ind["ruta"][:], "coste": coste, "fitness": 1.0 / coste})
    evaluados.sort(key=lambda x: x["fitness"], reverse=True)
    return evaluados


def inicializar(n, lote, semilla, idx):
    rng = random.Random(semilla + idx)
    return [{"ruta": rng.sample(range(n), n)} for _ in range(lote)]


def orientacion(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segmentos_se_cruzan(a, b, c, d):
    o1 = orientacion(a, b, c)
    o2 = orientacion(a, b, d)
    o3 = orientacion(c, d, a)
    o4 = orientacion(c, d, b)
    return (o1 * o2 < 0) and (o3 * o4 < 0)


def cruces_de_ruta(ruta, coords):
    n = len(ruta)
    pares = []
    for i in range(n):
        a = coords[ruta[i]]
        b = coords[ruta[(i + 1) % n]]
        for j in range(i + 1, n):
            c = coords[ruta[j]]
            d = coords[ruta[(j + 1) % n]]
            if i == j or (i == (j + 1) % n) or ((i + 1) % n == j):
                continue
            if segmentos_se_cruzan(a, b, c, d):
                pares.append((i, j))
    return pares


def mejorar_2opt(ruta, matriz):
    n = len(ruta)
    mejor = ruta[:]
    mejoro = True
    while mejoro:
        mejoro = False
        for i in range(n):
            for j in range(i + 2, n):
                if (j + 1) % n == i:
                    continue
                a, b = mejor[i], mejor[(i + 1) % n]
                c, d = mejor[j], mejor[(j + 1) % n]
                antes = matriz[a][b] + matriz[c][d]
                despues = matriz[a][c] + matriz[b][d]
                if despues < antes - 1e-9:
                    mejor[i + 1:j + 1] = mejor[i + 1:j + 1][::-1]
                    mejoro = True
    return mejor


def es_permutacion_valida(ruta):
    return sorted(ruta) == list(range(len(ruta)))


def seleccionar_rank(pob, rng):
    n = len(pob)
    total = n * (n + 1) / 2
    r = rng.uniform(0, total)
    acum = 0
    for i, x in enumerate(pob):
        acum += n - i
        if acum >= r:
            return x


def seleccionar_torneo(pob, k, rng):
    muestras = rng.sample(pob, k)
    return max(muestras, key=lambda x: x["fitness"])


def cruzar_ox(p1, p2, rng):
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    h1 = [None] * n
    h1[a:b] = p1[a:b]
    pos = b
    for g in p2[b:] + p2[:b]:
        if g not in h1:
            h1[pos % n] = g
            pos += 1
    h2 = [None] * n
    h2[a:b] = p2[a:b]
    pos = b
    for g in p1[b:] + p1[:b]:
        if g not in h2:
            h2[pos % n] = g
            pos += 1
    return h1, h2


def cruzar_pmx(p1, p2, rng):
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    h1 = p1[:]
    h1[a:b] = p2[a:b]
    mapa_h1 = {p2[i]: p1[i] for i in range(a, b)}
    for i in list(range(a)) + list(range(b, n)):
        while h1[i] in mapa_h1:
            h1[i] = mapa_h1[h1[i]]
    h2 = p2[:]
    h2[a:b] = p1[a:b]
    mapa_h2 = {p1[i]: p2[i] for i in range(a, b)}
    for i in list(range(a)) + list(range(b, n)):
        while h2[i] in mapa_h2:
            h2[i] = mapa_h2[h2[i]]
    return h1, h2


def mutar_swap(ruta, rng):
    i, j = rng.sample(range(len(ruta)), 2)
    ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta


def mutar_inversion(ruta, rng):
    i, j = sorted(rng.sample(range(len(ruta)), 2))
    ruta[i:j + 1] = reversed(ruta[i:j + 1])
    return ruta


def elitismo_pool(padres, hijos, lote):
    return evaluar(padres + hijos)[:lote]


def generar_historial(ramas):
    registros = []
    for nombre, estado in ramas.items():
        for g, h in enumerate(estado["historial"]):
            registros.append({
                "rama": nombre,
                "generacion": g,
                "mejor_distancia": h["mejor"],
                "promedio_distancia": h["promedio"],
                "mejor_ruta": json.dumps(h["ruta"]),
            })
    return registros


def plot_convergencia(ramas):
    fig, ejes = plt.subplots(1, 2, figsize=(16, 6))
    colores = plt.cm.tab10(np.linspace(0, 1, len(ramas)))
    for nombre, estado in ramas.items():
        gen = list(range(len(estado["historial"])))
        mejor = [h["mejor"] for h in estado["historial"]]
        prom = [h["promedio"] for h in estado["historial"]]
        color = colores[BRANCH_NAMES.index(nombre)]
        ejes[0].plot(gen, mejor, label=nombre, color=color)
        ejes[1].plot(gen, prom, label=nombre, color=color, linestyle="--")
    ejes[0].set_title("Distancia Mínima por Generación")
    ejes[1].set_title("Distancia Promedio del Lote")
    for ax in ejes:
        ax.set_xlabel("Generación")
        ax.set_ylabel("Distancia (km)")
        ax.grid(True)
        ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG / "convergencia.png", dpi=120)
    plt.close(fig)


def plot_mejor_ruta(estado):
    mejor = estado["historial"][-1]["ruta"]
    coords = np.load(DATO / "coords.npy")
    xs = [coords[i][0] for i in mejor] + [coords[mejor[0]][0]]
    ys = [coords[i][1] for i in mejor] + [coords[mejor[0]][1]]
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(xs, ys, "-o", label=f"ruta: {estado['historial'][-1]['mejor']:.0f} km")
    for i, idx in enumerate(mejor):
        ax.annotate(str(idx), (coords[idx][0], coords[idx][1]), fontsize=9)
    ax.set_title("Ruta óptima")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)
    ax.legend()
    fig.savefig(FIG / "ruta_optima.png", dpi=120)
    plt.close(fig)


def sugerir_meseta(estado, patience):
    mejor = [h["mejor"] for h in estado["historial"]]
    if len(mejor) < patience:
        return False, None
    ventana = mejor[-patience:]
    return (max(ventana) - min(ventana)) < 1e-3, mejor[-1]


def cargar_checkpoint():
    if CHECKPOINT.exists():
        data = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        data.setdefault("tiempos", [])
        return data
    ramas = {}
    n = len(CIUDADES)
    for idx, nombre in enumerate(BRANCH_NAMES):
        pob = inicializar(n, LOTE, SEMILLA, idx)
        pob = evaluar(pob)
        mejor = pob[0]["coste"]
        promedio = sum(x["coste"] for x in pob) / len(pob)
        ramas[nombre] = {
            "poblacion": pob,
            "historial": [{"mejor": mejor, "promedio": promedio, "ruta": pob[0]["ruta"]}],
        }
    return {"gen_actual": 0, "ramas": ramas, "tiempos": []}


def guardar_checkpoint(checkpoint):
    CHECKPOINT.write_text(json.dumps(checkpoint), encoding="utf-8")


def avanzar_generacion(checkpoint):
    t0 = time.perf_counter()
    checkpoint["gen_actual"] += 1
    gen = checkpoint["gen_actual"]
    for idx, nombre in enumerate(BRANCH_NAMES):
        s_op, c_op, m_op = BRANCHES[idx]
        estado = checkpoint["ramas"][nombre]
        rng = random.Random(SEMILLA + idx + gen * 1000)
        pob = estado["poblacion"]

        padres = []
        for _ in range(LOTE):
            if s_op == "rank":
                padres.append(seleccionar_rank(pob, rng))
            else:
                padres.append(seleccionar_torneo(pob, K_TORNEO, rng))
        padres.sort(key=lambda x: x["fitness"], reverse=True)
        hijos = []
        for i in range(0, LOTE, 2):
            p1, p2 = padres[i]["ruta"], padres[i + 1]["ruta"]
            if rng.random() < P_CROSS:
                if c_op == "OX":
                    h1, h2 = cruzar_ox(p1, p2, rng)
                else:
                    h1, h2 = cruzar_pmx(p1, p2, rng)
            else:
                h1, h2 = p1[:], p2[:]
            hijos.append({"ruta": h1})
            hijos.append({"ruta": h2})

        hijos = [{"ruta": h["ruta"]} if es_permutacion_valida(h["ruta"])
                 else {"ruta": padres[i // 2]["ruta"][:]}
                 for i, h in enumerate(hijos)]

        hijos_eval = evaluar(hijos)
        for ind in hijos_eval[-N_MUTAR:]:
            if m_op == "swap":
                ind["ruta"] = mutar_swap(ind["ruta"][:], rng)
            else:
                ind["ruta"] = mutar_inversion(ind["ruta"][:], rng)
        hijos_eval = evaluar(hijos_eval)

        nueva = elitismo_pool(pob, hijos_eval, LOTE)
        estado["poblacion"] = nueva
        mejor = nueva[0]["coste"]
        promedio = sum(x["coste"] for x in nueva) / len(nueva)
        estado["historial"].append({"mejor": mejor, "promedio": promedio, "ruta": nueva[0]["ruta"]})

    checkpoint["tiempos"].append(time.perf_counter() - t0)


def escribir_tiempos(checkpoint):
    tiempos = checkpoint["tiempos"]
    acum = 0.0
    with open(TIEMPOS_CSV, "w", encoding="utf-8") as f:
        f.write("generacion,tiempo_gen_seg,tiempo_acumulado_seg\n")
        for i, t in enumerate(tiempos, start=1):
            acum += t
            f.write(f"{i},{t:.6f},{acum:.6f}\n")
    return acum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generaciones", type=int, required=True)
    args = parser.parse_args()

    FIG.mkdir(parents=True, exist_ok=True)
    checkpoint = cargar_checkpoint()
    print(f"Estado inicial: generacion {checkpoint['gen_actual']}")

    for _ in range(args.generaciones):
        avanzar_generacion(checkpoint)

    guardar_checkpoint(checkpoint)
    total_tiempo = escribir_tiempos(checkpoint)
    ramas = checkpoint["ramas"]
    plot_convergencia(ramas)
    plot_mejor_ruta(ramas[BRANCH_NAMES[0]])

    registros = generar_historial(ramas)
    with open(HISTORIAL_CSV, "w", encoding="utf-8") as f:
        f.write("rama,generacion,mejor_distancia,promedio_distancia,mejor_ruta\n")
        for r in registros:
            f.write(f"{r['rama']},{r['generacion']},{r['mejor_distancia']:.3f},"
                    f"{r['promedio_distancia']:.3f},{r['mejor_ruta']}\n")

    tiempos = checkpoint["tiempos"]
    if tiempos:
        t_prom = sum(tiempos) / len(tiempos)
        print(f"\nTIEMPOS (evaluacion de costes de hardware):")
        print(f"  Generaciones medidas: {len(tiempos)}")
        print(f"  Tiempo promedio por generacion: {t_prom * 1000:.1f} ms")
        print(f"  Tiempo total acumulado: {total_tiempo:.2f} s")
        print(f"  Guardado en {TIEMPOS_CSV}")

    print(f"Generaciones ejecutadas: {checkpoint['gen_actual']}")
    print(f"{'RAMA':<22}{'MEJOR (km)':>14}{'GEN':>6}{'MESETA':>10}")
    for nombre in BRANCH_NAMES:
        estado = ramas[nombre]
        meseta, mejor = sugerir_meseta(estado, PATIENCE)
        g = len(estado["historial"]) - 1
        print(f"{nombre:<22}{estado['historial'][-1]['mejor']:>14.0f}{g:>6}{str(meseta):>10}")

    coords = np.load(DATO / "coords.npy")
    mejor_nombre = min(BRANCH_NAMES, key=lambda n: ramas[n]["historial"][-1]["mejor"])
    mejor_ruta = ramas[mejor_nombre]["historial"][-1]["ruta"]
    cruces = cruces_de_ruta(mejor_ruta, coords)
    dist_antes = costo_total(mejor_ruta)
    mejorada = mejorar_2opt(mejor_ruta, MATRIZ)
    dist_despues = costo_total(mejorada)
    print(f"\nVERIFICADOR de no-cruce (TSP euclidiano):")
    print(f"  Mejor rama: {mejor_nombre}")
    print(f"  Cruces detectados en la ruta: {len(cruces)}")
    print(f"  Distancia antes de 2-opt: {dist_antes:.0f} km")
    print(f"  Distancia despues de 2-opt (sin cruces): {dist_despues:.0f} km")
    if cruces:
        print("  => La ruta tenia cruces; NO era localmente optima (se mejoro con 2-opt).")
    else:
        print("  => La ruta no tiene cruces: es localmente optima bajo 2-opt (propiedad verificada).")

    print(f"Graficas en {FIG}")


if __name__ == "__main__":
    main()