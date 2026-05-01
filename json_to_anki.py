#!/usr/bin/env python3
"""Genera un archivo de flashcards Anki a partir de preguntas y respuestas JSON.

Formato de preguntas JSON (salida de preguntas_to_json.py):
  [{"numero": 1, "titulo": "...", "a": "...", "b": "...", "c": "...", "d": "..."}, ...]

Formato de respuestas JSON:
  {"1": "A", "2": "D", ...}   (clave = número de pregunta, valor = letra A-D o ANULADA)

El archivo de salida es un .txt importable en Anki (campos separados por tabulador,
HTML habilitado). Cada tarjeta tiene:
  - Anverso: pregunta con todas las opciones
  - Reverso: igual, pero la opción correcta marcada con clase CSS "correct"
"""

import json
import sys
from pathlib import Path


OPTIONS = ['a', 'b', 'c', 'd']


def build_question_html(pregunta: dict, correct: str | None) -> str:
    """Construye el HTML de una pregunta. Si correct es None, sin marcar."""
    lines = [f'<p class="question_title">{pregunta["titulo"]}</p>']
    lines.append('<ul>')
    for opt in OPTIONS:
        letter = opt.upper()
        text = pregunta.get(opt, '')
        if correct and letter == correct.upper():
            lines.append(f'  <li><span class="correct">{letter}) {text}</span></li>')
        else:
            lines.append(f'  <li>{letter}) {text}</li>')
    lines.append('</ul>')
    return ''.join(lines)


def load_respuestas(path: Path) -> dict[int, str]:
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        return {int(k): v for k, v in data.items()}
    if isinstance(data, list):
        return {int(item['pregunta']): item['respuesta'] for item in data}
    raise ValueError(f'Formato de respuestas no reconocido en {path}')


def main():
    if len(sys.argv) < 3:
        print(f'Uso: {sys.argv[0]} <preguntas.json> <respuestas.json> [salida.txt]')
        sys.exit(1)

    preguntas_path = Path(sys.argv[1])
    respuestas_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else Path('flashcards_anki.txt')

    preguntas: list[dict] = json.loads(preguntas_path.read_text(encoding='utf-8'))
    respuestas = load_respuestas(respuestas_path)

    lines = []
    skipped = 0
    for p in preguntas:
        num = p['numero']
        correct = respuestas.get(num)
        if correct == 'ANULADA':
            skipped += 1
            continue

        front = build_question_html(p, correct=None)
        back = build_question_html(p, correct=correct)
        lines.append(f'{front}\t{back}')

    output_path.write_text('\n'.join(lines), encoding='utf-8')

    total = len(lines)
    print(f'{total} flashcards generadas en {output_path}')
    if skipped:
        print(f'{skipped} preguntas anuladas omitidas')


if __name__ == '__main__':
    main()
