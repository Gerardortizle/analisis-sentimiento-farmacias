"""
generar_dataset.py
------------------
Genera de forma reproducible el dataset sintético de reseñas de clientes de
"Farmacias Occidente Salud" (cadena ficticia) utilizado en la Actividad 4.

Origen: reseñas SINTÉTICAS construidas a partir de plantillas redactadas a mano
que imitan el estilo de Google Reviews, Facebook y encuestas internas de
satisfacción. No contiene datos personales reales.

Uso:
    python src/generar_dataset.py                     # 300 registros, semilla 42
    python src/generar_dataset.py --n 500 --seed 7    # otra muestra

Salida: data/resenas_farmacias.csv (UTF-8)
"""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SUCURSALES = [
    ("FOS-GDL-001", "Guadalajara"), ("FOS-GDL-014", "Guadalajara"),
    ("FOS-ZAP-022", "Zapopan"), ("FOS-TLQ-031", "Tlaquepaque"),
    ("FOS-TON-040", "Tonalá"), ("FOS-COL-052", "Colima"),
    ("FOS-TEP-063", "Tepic"), ("FOS-MOR-071", "Morelia"),
    ("FOS-AGS-085", "Aguascalientes"), ("FOS-LEO-097", "León"),
]
CANALES = ["Google Reviews", "Facebook", "Encuesta interna"]
PESOS_CANAL = [0.45, 0.25, 0.30]

PRODUCTOS = ["el antibiótico", "la insulina", "el paracetamol", "las vitaminas",
             "el medicamento de mi mamá", "la leche de fórmula", "el jarabe",
             "el medicamento para la presión", "las gotas para los ojos"]
PERSONAL = ["la cajera", "el farmacéutico", "la dependienta", "el encargado",
            "la química", "el chico del mostrador"]
TIEMPOS = {  # coherentes con el sentimiento de la plantilla
    "positivo": ["3 minutos", "5 minutos", "10 minutos"],
    "neutral": ["15 minutos", "20 minutos"],
    "negativo": ["40 minutos", "una hora", "más de media hora"],
}

# --------------------------------------------------------------------------
# Plantillas por (categoría, sentimiento). {p}=producto, {s}=personal, {t}=tiempo
# --------------------------------------------------------------------------
PLANTILLAS = {
    "atencion": {
        "positivo": [
            "Excelente atención de {s}, me explicó muy bien cómo tomar {p}.",
            "{S} fue muy amable y paciente, se nota que conoce los medicamentos.",
            "Muy buen trato, {s} me ayudó a encontrar una opción más barata.",
            "Siempre me atienden con una sonrisa, da gusto venir a esta sucursal.",
            "Me encantó el servicio, {s} resolvió todas mis dudas sin prisas.",
        ],
        "neutral": [
            "{S} me atendió, sin más. Ni bien ni mal.",
            "La atención fue normal, me dieron lo que pedí.",
            "Me atendieron de forma correcta, nada que destacar.",
            "{S} respondió mi pregunta sobre {p} y ya.",
        ],
        "negativo": [
            "{S} fue grosero y ni siquiera me volteó a ver.",
            "Pésima atención, {s} estaba en el celular mientras yo esperaba.",
            "Me trataron muy mal, no vuelvo a esta sucursal.",
            "{S} me dio indicaciones equivocadas sobre {p}, muy mal.",
        ],
    },
    "surtido": {
        "positivo": [
            "Siempre tienen {p}, nunca me han quedado mal.",
            "Encontré {p} que no había en ninguna otra farmacia, ¡gracias!",
            "Muy bien surtida, tienen de todo.",
        ],
        "neutral": [
            "Tenían {p} pero solo de una marca.",
            "Fui por {p}; había, aunque pocas piezas.",
            "El surtido es el de cualquier farmacia.",
        ],
        "negativo": [
            "Tercera vez que no tienen {p}, es un problema constante.",
            "Nunca hay {p}, me mandan a otra sucursal cada semana.",
            "No tenían {p} y no supieron decirme cuándo llega.",
        ],
    },
    "tiempo_espera": {
        "positivo": [
            "Me atendieron en {t}, súper rápido.",
            "Rapidísimo, entré y salí en {t} con {p}.",
            "La fila avanzó muy rápido aunque había mucha gente.",
        ],
        "neutral": [
            "Esperé unos {t}, lo normal para la hora.",
            "Había fila, tardaron {t} en atenderme.",
        ],
        "negativo": [
            "Esperé {t} para que me surtieran {p}, inaceptable.",
            "Solo una caja abierta y una fila enorme, {t} perdidos.",
            "Tardaron {t} en surtir una receta sencilla.",
        ],
    },
    "precio": {
        "positivo": [
            "Los precios son mejores que en otras cadenas, ahorré bastante en {p}.",
            "Buenas promociones, el 2x1 en {p} me salvó la quincena.",
        ],
        "neutral": [
            "Los precios son similares a los de otras farmacias.",
            "{P} costó lo mismo que en el súper.",
        ],
        "negativo": [
            "Carísimo, {p} cuesta casi el doble que en otro lado.",
            "Me cobraron un precio distinto al de la etiqueta, qué abuso.",
        ],
    },
    "instalaciones": {
        "positivo": [
            "Sucursal limpia, ordenada y con buena iluminación.",
            "Muy cómoda la sucursal y tiene estacionamiento amplio.",
        ],
        "neutral": [
            "La sucursal es pequeña pero cumple.",
            "Instalaciones normales, como cualquier farmacia de barrio.",
        ],
        "negativo": [
            "La sucursal estaba sucia y el aire acondicionado no servía.",
            "No hay rampa de acceso y es imposible entrar con silla de ruedas.",
        ],
    },
}

# Casos difíciles: ironía, sentimiento mixto, negaciones. Etiquetados a mano.
DIFICILES = [
    ("¡Qué maravilla! Solo esperé una hora para comprar {p}.", "negativo", "tiempo_espera"),
    ("Genial, otra vez sin {p}. Ya es tradición.", "negativo", "surtido"),
    ("No está mal, pero tampoco es para tanto.", "neutral", "atencion"),
    ("La atención fue buena, aunque los precios están altos.", "neutral", "precio"),
    ("No me quejo, {s} fue amable aunque tardaron un poco.", "positivo", "atencion"),
    ("Nada que reclamar, todo perfecto como siempre.", "positivo", "atencion"),
    ("Buena ubicación, lástima que nunca tengan {p}.", "negativo", "surtido"),
    ("No es la más barata, pero el trato lo compensa.", "positivo", "precio"),
    ("Pues ahí está, abre a las 8.", "neutral", "instalaciones"),
    ("Increíble que en pleno 2026 no acepten pago con tarjeta.", "negativo", "precio"),
    ("Pensé que me iban a atender mal y fue todo lo contrario.", "positivo", "atencion"),
    ("Ni rápido ni lento, ni caro ni barato.", "neutral", "precio"),
]

ETIQUETAS = ["positivo", "neutral", "negativo"]
PROPORCIONES = [0.55, 0.25, 0.20]  # desequilibrio moderado, similar al caso de T10
PROP_DIFICILES = 0.12


def _rellenar(plantilla: str, rng: random.Random, etiqueta: str = "neutral") -> str:
    s = rng.choice(PERSONAL)
    p = rng.choice(PRODUCTOS)
    return plantilla.format(s=s, S=s[0].upper() + s[1:], p=p,
                            P=p[0].upper() + p[1:], t=rng.choice(TIEMPOS[etiqueta]))


def generar(n: int = 300, seed: int = 42):
    rng = random.Random(seed)
    n_dif = round(n * PROP_DIFICILES)
    n_norm = n - n_dif
    cuotas = [round(n_norm * p) for p in PROPORCIONES]
    cuotas[0] += n_norm - sum(cuotas)

    filas, vistos = [], set()
    for etiqueta, cuota in zip(ETIQUETAS, cuotas):
        intentos = 0
        while cuota > 0 and intentos < 20000:
            intentos += 1
            cat = rng.choice(list(PLANTILLAS))
            texto = _rellenar(rng.choice(PLANTILLAS[cat][etiqueta]), rng, etiqueta)
            if texto in vistos and intentos < 15000:
                continue
            vistos.add(texto)
            filas.append((texto, etiqueta, cat, "normal"))
            cuota -= 1
    for _ in range(n_dif):
        plantilla, etiqueta, cat = rng.choice(DIFICILES)
        filas.append((_rellenar(plantilla, rng, etiqueta), etiqueta, cat, "dificil"))

    rng.shuffle(filas)
    inicio = date(2026, 1, 1)
    registros = []
    for i, (texto, etiqueta, cat, dif) in enumerate(filas, start=1):
        suc, ciudad = rng.choice(SUCURSALES)
        registros.append({
            "id_resena": f"R{i:04d}",
            "fecha": (inicio + timedelta(days=rng.randint(0, 250))).isoformat(),
            "sucursal": suc,
            "ciudad": ciudad,
            "canal": rng.choices(CANALES, PESOS_CANAL)[0],
            "categoria": cat,
            "texto": texto,
            "sentimiento": etiqueta,
            "dificultad": dif,
        })
    return registros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data" / "resenas_farmacias.csv"))
    args = ap.parse_args()
    regs = generar(args.n, args.seed)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(regs[0]))
        w.writeheader()
        w.writerows(regs)
    from collections import Counter
    c = Counter(r["sentimiento"] for r in regs)
    print(f"{len(regs)} reseñas -> {args.out}")
    for k in ETIQUETAS:
        print(f"  {k:9s} {c[k]:4d}  ({c[k] / len(regs):.1%})")


if __name__ == "__main__":
    main()
