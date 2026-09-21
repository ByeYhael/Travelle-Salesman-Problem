import sys
import time
import csv
from pathlib import Path

import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

BASE = Path(__file__).resolve().parent.parent
OUT_DATOS = BASE / "outputs" / "datos"

CIUDADES = [
    "Ciudad de Mexico, Mexico",
    "Merida, Yucatan, Mexico",
    "Buenos Aires, Argentina",
    "Quito, Ecuador",
    "Washington D.C., USA",
    "New York, USA",
    "Miami, USA",
    "Monterrey, Nuevo Leon, Mexico",
    "Panama City, Panama",
    "San Salvador, El Salvador",
    "Managua, Nicaragua",
    "Brasilia, Brazil",
    "Mendoza, Argentina",
    "Caracas, Venezuela",
    "Montevideo, Uruguay",
    "Guadalajara, Jalisco, Mexico",
    "Boston, USA",
    "Bogota, Colombia",
]


def obtener_coordenadas(geocoder):
    coords = []
    for nombre in CIUDADES:
        try:
            lugar = geocoder.geocode(nombre, timeout=30)
        except Exception as e:
            print(f"ERROR de red al geocodificar '{nombre}': {e}", file=sys.stderr)
            sys.exit(1)
        if lugar is None:
            print(f"ERROR: no se encontro la ciudad '{nombre}'. Detengo el flujo.", file=sys.stderr)
            sys.exit(1)
        coords.append((lugar.latitude, lugar.longitude))
        print(f"  OK {nombre}: ({lugar.latitude:.4f}, {lugar.longitude:.4f})")
        time.sleep(1.1)
    return coords


def main():
    OUT_DATOS.mkdir(parents=True, exist_ok=True)
    geocoder = Nominatim(user_agent="uaq-tsp-genetico")
    print("Geocodificando las 18 ciudades con Nominatim...")
    coords = obtener_coordenadas(geocoder)

    n = len(coords)
    matriz = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            km = geodesic(coords[i], coords[j]).kilometers
            matriz[i][j] = km
            matriz[j][i] = km

    np.save(OUT_DATOS / "coords.npy", np.array(coords))
    np.save(OUT_DATOS / "matriz_distancias.npy", matriz)

    with open(OUT_DATOS / "ciudades.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["indice", "ciudad", "latitud", "longitud"])
        for i, (nombre, (lat, lon)) in enumerate(zip(CIUDADES, coords)):
            writer.writerow([i, nombre.split(",")[0], lat, lon])

    np.savetxt(OUT_DATOS / "matriz_distancias.csv", matriz, delimiter=",", fmt="%.2f")

    print("\nMatriz de distancias (km) construida:")
    print("  " + "".join(f"{i:>9}" for i in range(n)))
    for i in range(n):
        print(f"{i:>2} " + "".join(f"{matriz[i][j]:9.0f}" for j in range(n)))
    print(f"\nGuardado en {OUT_DATOS}")


if __name__ == "__main__":
    main()