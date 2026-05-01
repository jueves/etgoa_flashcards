El objetivo de este proyecto es convertir exámenes tipo test de ETGOA en tarjetas de estudio de Anki.

## Paso previo manual
Convertir a Markdown con Marker. El documento pdf original incluye todas las áreas, seleccionar manualmente las páginas a extraer.

Repetir el proceso tanto con las preguntas como con las respuestas.

Ejemplo:

```bash
marker_single Examen_ETGOA_2023_Preguntas.pdf --page_range 225-245 --output_dir markdown/
marker_single Examen_ETGOA_2023_Respuestas.pdf --page_range 0,11 --output_dir markdown/
```

