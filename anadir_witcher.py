# -*- coding: utf-8 -*-
"""Añade las pistas de The Witcher 3 al repositorio de musica.

Los ficheros llegan con el nombre del disco ("Percival - Silver For
Monsters.mp3"): con espacios, con tildes y con la 'ł' de Przybyłowicz.
Eso no vale para una URL — los espacios se vuelven %20 y la ł se
rompe — asi que se renombran al patron del repositorio, numerados a
continuacion de los que ya hay.

Tambien deja el CSV listo para el "Import csv" de Tracks.

    python anadir_witcher.py            # en seco
    python anadir_witcher.py --aplica   # renombra y escribe el CSV
"""
import csv
import io
import os
import pathlib
import sys

os.chdir(pathlib.Path(__file__).resolve().parent)

# La consola de Windows viene en cp1252 y revienta al imprimir la 'ł'
# de Przybyłowicz — que es justo uno de los motivos del renombrado.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "https://raw.githubusercontent.com/Juan-Exe/musica-dnd/main"
CSV = pathlib.Path("tracks-musica.csv")

# (fichero tal como llego, numero, nombre nuevo, titulo en Tracks, etiquetas)
#
# Las etiquetas siguen las que ya usan las 26 primeras, para que al
# buscar "combate" salgan todas juntas. "ciudad" es nueva: hasta ahora
# solo habia "pueblo", y Oxenfurt no es Phandalin.
NUEVAS = [
    ("Percival - Silver For Monsters.mp3", 27, "plata-para-monstruos",
     "[Witcher 3] Plata para Monstruos", "combate,monstruo,tension"),
    ("Percival - ...Steel For Humans.mp3", 28, "acero-para-humanos",
     "[Witcher 3] Acero para Humanos", "combate,bandidos,tension"),
    ("Percival - The Nightingale.mp3", 29, "el-ruisenor",
     "[Witcher 3] El Ruisenor", "taberna,alegre,pueblo"),
    ("Percival - Cloak And Dagger.mp3", 30, "capa-y-daga",
     "[Witcher 3] Capa y Daga", "sigilo,intriga,tension"),
    ("Percival Schuttenbach - Lazare.mp3", 31, "lazare",
     "[Witcher 3] Lazare", "taberna,alegre,fiesta"),
    ("Marcin Przybyłowicz - The Hunt Is Coming.mp3", 32, "la-caceria-se-acerca",
     "[Witcher 3] La Caceria se Acerca", "jefe,epico,amenaza,dragon"),
    ("Mikolai Stroinski - Eyes Of The Wolf.mp3", 33, "ojos-del-lobo",
     "[Witcher 3] Ojos del Lobo", "viaje,exploracion,oscuro"),
    ("Mikolai Stroinski - Whispers Of Oxenfurt.mp3", 34, "susurros-de-oxenfurt",
     "[Witcher 3] Susurros de Oxenfurt", "ciudad,intriga,misterio"),
    ("Mikolai Stroinski - City Of Intrigues.mp3", 35, "ciudad-de-intrigas",
     "[Witcher 3] Ciudad de Intrigas", "ciudad,intriga,villano"),
    ("Mikolai Stroinski - Blood On The Cobblestones.mp3", 36,
     "sangre-en-los-adoquines",
     "[Witcher 3] Sangre en los Adoquines", "tension,oscuro,combate"),
    ("Mikolai Stroinski - After The Storm.mp3", 37, "despues-de-la-tormenta",
     "[Witcher 3] Despues de la Tormenta", "emotivo,triste,descanso"),
]


def main() -> int:
    aplica = "--aplica" in sys.argv

    # lo que ya hay, para no repetir ni perderlo
    filas = []
    if CSV.exists():
        with io.open(CSV, encoding="utf-8", newline="") as f:
            filas = list(csv.reader(f))
    cabecera = filas[0] if filas else ["title", "url", "tags"]
    yaestan = {r[0] for r in filas[1:]}

    nuevas, faltan = [], []
    for viejo, num, corto, titulo, tags in NUEVAS:
        p = pathlib.Path(viejo)
        nombre = f"{num}-{corto}.mp3"
        destino = pathlib.Path(nombre)

        if not p.exists() and not destino.exists():
            faltan.append(viejo)
            continue

        if p.exists():
            print(f"  {viejo}\n    -> {nombre}")
            if aplica:
                p.rename(destino)
        else:
            print(f"  (ya renombrado) {nombre}")

        if titulo not in yaestan:
            nuevas.append([titulo, f"{BASE}/{nombre}", tags])

    print(f"\n{len(NUEVAS) - len(faltan)} pistas, {len(nuevas)} al CSV")
    if faltan:
        print("\nno encuentro:")
        for x in faltan:
            print("  ", x)

    if aplica and nuevas:
        with io.open(CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(cabecera)
            for r in filas[1:]:
                w.writerow(r)
            for r in nuevas:
                w.writerow(r)
        print(f"\n{CSV} con {len(filas) - 1 + len(nuevas)} pistas")

    if not aplica:
        print("\nen seco: no se ha tocado nada (usa --aplica).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
