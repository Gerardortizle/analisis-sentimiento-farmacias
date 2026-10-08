"""
llenar_reporte.py
-----------------
Sustituye los marcadores «TOKEN» del reporte Word (docs/Analisis_Comparativo_Modelos.docx)
con las cifras reales generadas por el notebook en results/.

Uso (desde la raíz del repo, después de ejecutar el notebook):
    python src/llenar_reporte.py
Salida: docs/Analisis_Comparativo_Modelos_resultados.docx
"""
import json
from pathlib import Path

import pandas as pd
from docx import Document

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "results"
PLANTILLA = RAIZ / "docs" / "Analisis_Comparativo_Modelos.docx"
SALIDA = RAIZ / "docs" / "Analisis_Comparativo_Modelos_resultados.docx"


def f3(x):
    return "n/d" if pd.isna(x) else f"{x:.3f}"


def f1d(x):
    return "n/d" if pd.isna(x) else f"{x:,.1f}"


def construir_tokens():
    met = pd.read_csv(RES / "metricas_modelos.csv", index_col=0)
    meta = pd.read_csv(RES / "metadatos_modelos.csv", index_col=0)
    ctx = json.loads((RES / "contexto_ejecucion.json").read_text(encoding="utf-8"))
    t = {}
    for alias, r in met.iterrows():
        k = alias.split("_")[0]  # M1..M4
        m = meta.loc[alias] if alias in meta.index else {}
        t.update({
            f"ACC_{k}": f3(r.accuracy), f"PREC_{k}": f3(r.precision_macro), f"REC_{k}": f3(r.recall_macro),
            f"F1_{k}": f3(r.f1_macro), f"RNEG_{k}": f3(r.recall_NEG), f"RNEU_{k}": f3(r.recall_NEU),
            f"P50_{k}": f1d(r.lat_p50_ms), f"P95_{k}": f1d(r.lat_p95_ms), f"LOTE_{k}": f"{r.lat_lote_ms:.2f}",
            f"RPS_{k}": f1d(r.throughput_rps), f"VRAM_{k}": f1d(r.vram_pico_MB), f"PARAMS_{k}": f1d(r.params_M),
            f"DISCO_{k}": f1d(m.get("disco_MB")) if len(m) else "n/d",
            f"LIC_{k}": str(m.get("licencia", "verificar")) if len(m) else "verificar",
            f"CUMPLE_{k}": "Sí" if bool(r.cumple_umbrales) else "No",
        })
    rec, mp, mr = ctx["recomendado"], ctx["mas_preciso"], ctx["mas_rapido"]
    R, P, Q = met.loc[rec], met.loc[mp], met.loc[mr]
    t.update({
        "REC_MODELO": f"{rec} ({R.modelo})", "F1_REC": f3(R.f1_macro), "ACC_REC": f3(R.accuracy),
        "RNEG_REC": f3(R.recall_NEG), "P95_REC": f1d(R.lat_p95_ms), "P50_REC": f1d(R.lat_p50_ms),
        "MAS_PRECISO": mp, "MAS_RAPIDO": mr,
        "FACTOR": f"{P.lat_p50_ms / Q.lat_p50_ms:.1f}",
        "DIF_F1": f"{100 * (P.f1_macro - Q.f1_macro):.1f}",
        "DECISION_FT": ("No se requiere fine-tuning: el modelo recomendado cumple todos los umbrales con ajustes mínimos."
                        if not ctx["requiere_ft"] else
                        "Ningún modelo cumplió todos los umbrales; se recomienda fine-tuning ligero del modelo con mayor F1-macro (celda 16 del notebook)."),
        "FRASE_CUMPLE": ("cumple todos los umbrales de negocio solo con ajustes mínimos, sin modificar sus pesos."
                         if not ctx["requiere_ft"] else
                         "es el de mayor F1-macro, pero ningún candidato alcanzó todos los umbrales sin reentrenar, por lo que el fine-tuning ligero es parte de la recomendación."),
        "FECHA": ctx["fecha"], "GPU": ctx["gpu"], "TRANSFORMERS": ctx["transformers"], "PYTHON": ctx["python"],
        "N_RESENAS": str(ctx["n_resenas"]),
    })
    return t


def _parrafos(contenedor):
    for p in contenedor.paragraphs:
        yield p
    for tabla in getattr(contenedor, "tables", []):
        for fila in tabla.rows:
            for celda in fila.cells:
                yield from _parrafos(celda)


def main():
    tokens = construir_tokens()
    doc = Document(PLANTILLA)
    faltantes = set()
    for p in _parrafos(doc):
        for run in p.runs:
            if "«" in run.text:
                txt = run.text
                for k, v in tokens.items():
                    txt = txt.replace(f"«{k}»", v)
                if txt != run.text:
                    run.text = txt
                    run.font.highlight_color = None
                if "«" in txt:
                    faltantes.add(txt)
    doc.save(SALIDA)
    print(f"Reporte con resultados: {SALIDA}")
    if faltantes:
        print("Marcadores sin valor (revisar):", sorted(faltantes))


if __name__ == "__main__":
    main()
