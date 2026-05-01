El objetivo de este proyecto es convertir exámenes tipo test de ETGOA en tarjetas de estudio de Anki.

## Paso previo manual
Convertir a Markdown con Marker. El documento pdf original incluye todas las áreas, seleccionar manualmente las páginas a extraer.

Repetir el proceso tanto con las preguntas como con las respuestas.

Ejemplo:

```bash
marker_single Examen_ETGOA_2023_Preguntas.pdf --page_range 225-245 --output_dir markdown/
marker_single Examen_ETGOA_2023_Respuestas.pdf --page_range 0,11 --output_dir markdown/
```

## Estructura del script
- Convertir examen a json
    Número, Título, a, b, c, d
- Convertir respuestas a json
    Número, respuesta
- Crear tarjetas Anki a partir de ambos json

## Estructura del markdown
Título de la pregunta en negrita, inicia con un número de 1, 2 o 3 dígitos segudo de punto y espacio.
Precuntas precedidas de guión, espacio, letra mayus A-C, paréntesis y espacio. Y salto de linea.
No siempre hay una linea vacía entre una pregunta y la siguiente.
Creo que todos los títulos tienen encabezado, pero estos son de diferente nivel.Hay alguno que en lugar de encabezado lleva guión.
Hay un texto por ahí que dice "PREGUNTAS DE RESERVA", esto habría que excluirlo.
