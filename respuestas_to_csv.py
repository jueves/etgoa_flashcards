import argparse
import csv
import re
import sys
from pathlib import Path


def parse_answers(filepath):
    answers = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            for i in range(0, len(cells) - 1, 2):
                q, a = cells[i], cells[i + 1]
                if re.fullmatch(r"\d+", q) and re.fullmatch(r"[A-Da-d]|ANULADA", a):
                    answers[int(q)] = a.upper()
    return answers


def main():
    parser = argparse.ArgumentParser(
        description="Convierte el markdown de respuestas ETGOA a CSV."
    )
    parser.add_argument("entrada", type=Path, help="Archivo markdown de respuestas")
    parser.add_argument("salida", nargs="?", type=Path, default=Path("respuestas.csv"),
                        help="Archivo CSV de salida (por defecto: respuestas.csv)")
    args = parser.parse_args()

    answers = parse_answers(args.entrada)
    if not answers:
        print("No se encontraron respuestas.", file=sys.stderr)
        sys.exit(1)

    with open(args.salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["pregunta", "respuesta"])
        for q in sorted(answers):
            writer.writerow([q, answers[q]])

    print(f"CSV generado: {args.salida} ({len(answers)} preguntas)")


if __name__ == "__main__":
    main()
