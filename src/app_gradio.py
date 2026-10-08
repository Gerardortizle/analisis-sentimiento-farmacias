"""
app_gradio.py — Demo para desplegar el modelo recomendado como Hugging Face Space (SDK: Gradio).
Copiar este archivo como app.py en un Space y agregar requirements: transformers, torch, gradio.
"""
import gradio as gr
from transformers import pipeline

MODELO = "pysentimiento/robertuito-sentiment-analysis"  # <-- reemplazar por el modelo recomendado
clf = pipeline("text-classification", model=MODELO, truncation=True, max_length=128)


def normalizar(label: str) -> str:
    l = label.lower()
    if "star" in l:
        n = int(l[0])
        return "NEG" if n <= 2 else ("NEU" if n == 3 else "POS")
    return {"pos": "POS", "neg": "NEG", "neu": "NEU"}.get(l[:3], label)


def clasificar(texto: str):
    o = clf(texto)[0]
    return {"sentimiento": normalizar(o["label"]), "confianza": round(o["score"], 3)}


demo = gr.Interface(fn=clasificar, inputs=gr.Textbox(lines=3, label="Reseña del cliente"),
                    outputs=gr.JSON(label="Resultado"),
                    title="Farmacias Occidente Salud · Sentimiento de reseñas")

if __name__ == "__main__":
    demo.launch()
