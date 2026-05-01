#!/usr/bin/env python3
"""Convierte el markdown de preguntas ETGOA a JSON."""

import re
import json
import sys
from pathlib import Path


def parse_preguntas(md_text: str) -> list[dict]:
    # Excluir sección de reserva y lo que venga después
    reserva_match = re.search(r'PREGUNTAS DE RESERVA', md_text, re.IGNORECASE)
    if reserva_match:
        md_text = md_text[:reserva_match.start()]

    preguntas = []
    current: dict | None = None
    current_option: str | None = None
    current_lines: list[str] = []

    def save_option():
        if current and current_option and current_lines:
            current[current_option] = ' '.join(current_lines).strip()
            current_lines.clear()

    def save_question():
        save_option()
        if current and current.get('titulo'):
            preguntas.append(current)

    for raw_line in md_text.splitlines():
        line = raw_line.strip()

        # Línea de título: número + punto + espacio, puede tener marcado markdown (##, **, -)
        # Ejemplos: "**1. Texto**", "## 2. Texto", "- 3. Texto"
        title_match = re.match(
            r'^(?:[#\-*_>\s]*)(\d{1,3})\.\s+(.+?)(?:\*\*)?$',
            line
        )

        # Línea de opción: "- A) texto" o "- A) texto"
        option_match = re.match(r'^-\s+([A-D])\)\s+(.*)', line)

        if title_match:
            save_question()
            num = int(title_match.group(1))
            titulo = title_match.group(2).strip().strip('*').strip()
            current = {'numero': num, 'titulo': titulo, 'a': '', 'b': '', 'c': '', 'd': ''}
            current_option = None
            current_lines = []

        elif option_match and current:
            save_option()
            current_option = option_match.group(1).lower()
            current_lines = [option_match.group(2).strip()]

        elif current and current_option and line:
            # Continuación de la opción anterior (texto en múltiples líneas)
            current_lines.append(line)

    save_question()
    return preguntas


def main():
    if len(sys.argv) < 2:
        print(f'Uso: {sys.argv[0]} <archivo.md> [salida.json]')
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_suffix('.json')

    md_text = input_path.read_text(encoding='utf-8')
    preguntas = parse_preguntas(md_text)

    output_path.write_text(
        json.dumps(preguntas, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    print(f'{len(preguntas)} preguntas exportadas a {output_path}')


if __name__ == '__main__':
    main()
