# Diccionario de datos · `resenas_farmacias.csv`

**Origen:** dataset sintético generado con `src/generar_dataset.py` (semilla 42) a partir de plantillas redactadas a mano que imitan reseñas de Google Reviews, Facebook y encuestas internas de la cadena ficticia *Farmacias Occidente Salud*. No contiene datos personales.

**Registros:** 300 · **Codificación:** UTF-8 · **Separador:** coma

| Campo | Tipo | Descripción |
|---|---|---|
| `id_resena` | texto | Identificador único (R0001…R0300) |
| `fecha` | fecha ISO | Fecha de la reseña (enero–septiembre 2026) |
| `sucursal` | texto | Clave de sucursal `FOS-<ciudad>-<número>` |
| `ciudad` | texto | Ciudad de la sucursal |
| `canal` | categórico | Google Reviews · Facebook · Encuesta interna |
| `categoria` | categórico | atencion · surtido · tiempo_espera · precio · instalaciones |
| `texto` | texto | Contenido de la reseña en español |
| `sentimiento` | categórico | Etiqueta real: positivo · neutral · negativo |
| `dificultad` | categórico | normal · dificil (ironía, sentimiento mixto, negación; 12 %) |

**Distribución:** positivo 160 (53.3 %) · neutral 76 (25.3 %) · negativo 64 (21.3 %).

**Regenerar:** `python src/generar_dataset.py` (mismo resultado) o `python src/generar_dataset.py --n 500 --seed 7` (variante).
