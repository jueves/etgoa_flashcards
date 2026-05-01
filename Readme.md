El objetivo de este proyecto es convertir exámenes tipo test de ETGOA en tarjetas de estudio de Anki.

## Flujo completo

```
PDF original → (marker) → Markdown → preguntas_to_json.py → JSON
                                   → respuestas_to_csv.py  → CSV
                                                              ↓
                                                        json_to_anki.py → .txt (importar en Anki)
```

---

## Paso 0 — Conversión manual de PDF a Markdown

Usa [Marker](https://github.com/datalab-to/marker) para convertir los PDF. El documento original agrupa todas las áreas, así que selecciona manualmente las páginas que correspondan al área que quieres estudiar.

Repite el proceso con el PDF de preguntas y con el de respuestas.

```bash
marker_single Examen_ETGOA_2023_Preguntas.pdf --page_range 225-245 --output_dir markdown/
marker_single Examen_ETGOA_2023_Respuestas.pdf --page_range 0,11   --output_dir markdown/
```

**Salida esperada:** dos archivos `.md`, uno con las preguntas y otro con la plantilla de respuestas.

---

## Paso 1 — `preguntas_to_json.py`

Convierte el Markdown de preguntas al formato JSON que entiende `json_to_anki.py`.

### Uso

```bash
python preguntas_to_json.py <archivo.md> [salida.json]
```

| Parámetro | Obligatorio | Descripción |
|-----------|-------------|-------------|
| `archivo.md` | Sí | Markdown generado por Marker con las preguntas |
| `salida.json` | No | Ruta del JSON de salida. Por defecto: mismo nombre que la entrada con extensión `.json` |

### Ejemplo

```bash
python preguntas_to_json.py Examen_ETGOA_2023_Preguntas_vigi.md preguntas.json
```

### Salida esperada

```
60 preguntas exportadas a preguntas.json
```

El archivo JSON tiene este formato:

```json
[
  {
    "numero": 1,
    "titulo": "Conforme a lo expuesto en la Constitución española de 1978:",
    "a": "Ningún español de origen podrá ser privado de su nacionalidad",
    "b": "El Estado podrá concertar tratados de doble nacionalidad solo con países iberoamericanos",
    "c": "La extradición se concederá siempre a petición de un tercer país",
    "d": "Se incluyen en la extradición los delitos políticos"
  },
  ...
]
```

---

## Paso 2 — `respuestas_to_csv.py`

Convierte el Markdown de la plantilla de respuestas a un CSV con dos columnas: `pregunta` y `respuesta`.

### Uso

```bash
python respuestas_to_csv.py <entrada.md> [salida.csv]
```

| Parámetro | Obligatorio | Descripción |
|-----------|-------------|-------------|
| `entrada.md` | Sí | Markdown con la plantilla oficial de respuestas (tabla en formato Markdown) |
| `salida.csv` | No | Ruta del CSV de salida. Por defecto: `respuestas.csv` |

### Ejemplo

```bash
python respuestas_to_csv.py Examen_ETGOA_2023_Respuestas.md respuestas.csv
```

### Salida esperada

```
CSV generado: respuestas.csv (60 preguntas)
```

El CSV tiene este formato:

```
pregunta,respuesta
1,A
2,D
3,C
...
```

Las preguntas marcadas como `ANULADA` en la plantilla oficial se incluyen en el CSV y se omiten automáticamente en el paso siguiente.

---

## Paso 3 — `json_to_anki.py`

Combina el JSON de preguntas y el CSV de respuestas para generar un archivo `.txt` importable directamente en Anki.

### Uso

```bash
python json_to_anki.py <preguntas.json> <respuestas.csv> [salida.txt] [--tag ETIQUETA]
```

| Parámetro | Obligatorio | Descripción |
|-----------|-------------|-------------|
| `preguntas.json` | Sí | JSON generado en el paso 1 |
| `respuestas.csv` | Sí | CSV generado en el paso 2 |
| `salida.txt` | No | Ruta del archivo de salida. Por defecto: `flashcards_anki.txt` |
| `--tag ETIQUETA` | No | Etiqueta Anki que se asignará a todas las tarjetas |

### Ejemplo

```bash
python json_to_anki.py preguntas.json respuestas.csv flashcards_anki.txt --tag ETGOA_2023
```

### Salida esperada

```
60 flashcards generadas en flashcards_anki.txt
2 preguntas anuladas omitidas
```

El archivo de salida es un `.txt` con campos separados por tabulador e HTML habilitado. Cada línea es una tarjeta con:
- **Anverso:** la pregunta con todas las opciones sin marcar.
- **Reverso:** la misma pregunta con la opción correcta envuelta en `<span class="correct">`.

Si se especificó `--tag`, la primera línea del archivo es `#tags:<ETIQUETA>`.

### Importar en Anki

1. Abre Anki → **Archivo → Importar**.
2. Selecciona el archivo `.txt` generado.
3. Configura el separador como **Tabulador** y activa **Permitir HTML**.
4. Asigna los campos: campo 1 → Anverso, campo 2 → Reverso.

Para que la opción correcta se muestre resaltada, añade en la plantilla de la carta (CSS) una regla como:

```css
.correct { color: green; font-weight: bold; }
```
