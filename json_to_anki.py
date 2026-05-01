#!/usr/bin/env python3
"""Genera un archivo de flashcards Anki a partir de preguntas JSON y respuestas CSV.

Formato de preguntas JSON (salida de preguntas_to_json.py):
  [{"numero": 1, "titulo": "...", "a": "...", "b": "...", "c": "...", "d": "..."}, ...]

Formato de respuestas CSV (salida de respuestas_to_csv.py):
  pregunta,respuesta
  1,A
  2,D
  ...

El archivo de salida es un .txt importable en Anki (campos separados por tabulador,
HTML habilitado). Cada tarjeta tiene:
  - Anverso: pregunta con todas las opciones
  - Reverso: igual, pero la opción correcta marcada con clase CSS "correct"
"""

import argparse
import csv
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
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return {int(row['pregunta']): row['respuesta'] for row in reader}


def main():
    parser = argparse.ArgumentParser(
        description='Genera flashcards Anki desde preguntas JSON y respuestas CSV.'
    )
    parser.add_argument('preguntas', type=Path, help='Archivo de preguntas (.json)')
    parser.add_argument('respuestas', type=Path, help='Archivo de respuestas (.csv)')
    parser.add_argument('salida', nargs='?', type=Path, default=Path('flashcards_anki.txt'),
                        help='Archivo de salida (por defecto: flashcards_anki.txt)')
    parser.add_argument('--tag', metavar='ETIQUETA',
                        help='Etiqueta Anki para todas las tarjetas')
    args = parser.parse_args()

    preguntas_path = args.preguntas
    respuestas_path = args.respuestas
    output_path = args.salida

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

    content = '\n'.join(lines)
    if args.tag:
        content = f'#tags:{args.tag}\n' + content
    output_path.write_text(content, encoding='utf-8')

    total = len(lines)
    print(f'{total} flashcards generadas en {output_path}')
    if skipped:
        print(f'{skipped} preguntas anuladas omitidas')


if __name__ == '__main__':
    main()
