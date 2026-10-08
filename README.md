# Análisis de sentimiento de reseñas · Farmacias Occidente Salud

Prototipo que **compara cuatro modelos preentrenados de Hugging Face** para clasificar reseñas de clientes en español como **negativas (NEG), neutrales (NEU) o positivas (POS)**, ejecutado en **Google Colab con GPU T4**. Actividad 4 del curso *Gestión de proyectos de inteligencia artificial* (Universidad Tecmilenio).

## Descripción del proyecto
*Farmacias Occidente Salud* (cadena ficticia, 140 sucursales en el occidente de México) recibe reseñas en Google Reviews, Facebook y encuestas internas que hoy se revisan a mano. El prototipo identifica el modelo más adecuado para clasificarlas automáticamente y alimentar un tablero de alertas por sucursal.

- **Rama de IA:** Procesamiento de Lenguaje Natural (NLP)
- **Tarea Hugging Face:** `text-classification` (sentimiento, 3 clases)
- **Métrica principal:** F1-macro, con piso de recall en la clase negativa

## Modelos comparados
| # | Modelo | Arquitectura | Salida |
|---|---|---|---|
| M1 | [`pysentimiento/robertuito-sentiment-analysis`](https://huggingface.co/pysentimiento/robertuito-sentiment-analysis) | RoBERTa, español | POS/NEU/NEG |
| M2 | [`cardiffnlp/twitter-xlm-roberta-base-sentiment`](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment) | XLM-RoBERTa base | positive/neutral/negative |
| M3 | [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) | BERT multilingüe | 1–5 estrellas |
| M4 | [`lxyuan/distilbert-base-multilingual-cased-sentiments-student`](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student) | DistilBERT multilingüe | positive/neutral/negative |

**Ecosistema Hugging Face:** *Models* (búsqueda, descarga y metadatos con `HfApi`), *Datasets* (`Dataset.from_pandas`, `push_to_hub` opcional) y *Spaces* (demo en `src/app_gradio.py`).

## Estructura del repositorio
```
analisis-sentimiento-farmacias/
├── README.md
├── requirements.txt
├── data/
│   ├── resenas_farmacias.csv        # 300 reseñas sintéticas etiquetadas
│   └── diccionario_datos.md         # origen y descripción de campos
├── notebooks/
│   └── Act4_Comparacion_Modelos_HF.ipynb
├── src/
│   ├── generar_dataset.py           # regenera el dataset (semilla 42)
│   ├── llenar_reporte.py            # inserta resultados en el reporte Word
│   └── app_gradio.py                # demo para Hugging Face Spaces
├── results/                         # métricas, predicciones, gráficas y versiones (se generan al ejecutar)
└── docs/
    └── Analisis_Comparativo_Modelos.docx
```

## Entorno de ejecución
- Google Colab · GPU **NVIDIA T4** · Python 3.10+
- Dependencias en `requirements.txt` (versiones mínimas); las versiones exactas de cada ejecución quedan en `results/entorno_versiones.txt`
- Token de Hugging Face con permiso *Read* guardado en **Colab Secrets** como `HF_TOKEN`

## Pasos de ejecución
1. Abrir `notebooks/Act4_Comparacion_Modelos_HF.ipynb` en Colab (*Archivo → Abrir cuaderno → GitHub*).
2. *Entorno de ejecución → Cambiar tipo de entorno → GPU T4*.
3. Agregar el secreto `HF_TOKEN` (ícono 🔑).
4. Ejecutar celdas 1 y 2; **reiniciar la sesión**.
5. En la celda 4, colocar la URL de este repositorio en `REPO_URL` y ejecutar de la celda 3 a la 15 en orden.
6. Descargar la carpeta `results/` y `docs/Analisis_Comparativo_Modelos_resultados.docx`, y subirlos al repositorio.

Para regenerar el dataset sin Colab: `python src/generar_dataset.py`.

## Umbrales de aceptación
| Métrica | Umbral |
|---|---|
| Accuracy | ≥ 0.80 |
| F1-macro | ≥ 0.75 |
| Recall NEG | ≥ 0.75 |
| Latencia p95 por reseña (T4) | ≤ 100 ms |

Regla: entre los modelos que cumplen todo se elige el de mayor F1-macro; si otro queda a ≤ 0.02, gana el más rápido. Si ninguno cumple, se aplica fine-tuning ligero (celda 16).

## Resultados
Las métricas completas se generan en `results/metricas_modelos.csv` y `results/resumen.md`. *(Pegar aquí la tabla de `results/resumen.md` tras la ejecución.)*

## Conclusiones
- La comparación se hizo con datos del propio caso de uso y umbrales definidos antes de ejecutar, no por popularidad del modelo.
- Los ajustes mínimos (normalización de etiquetas, unificación de salidas, truncado a 128 tokens y uso de GPU) bastan para comparar modelos sin modificar pesos.
- El modelo recomendado y su justificación están en `docs/` y en la celda 14 del notebook.
- **Limitación:** el dataset es sintético; antes de producción debe validarse con reseñas reales etiquetadas.

## Autor
José Gerardo Ortiz Leñero · Master en Inteligencia Artificial, Universidad Tecmilenio
