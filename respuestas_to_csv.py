import csv
import re
import sys

ANSWERS_FILE = "Examen_ETGOA_2023_Respuestas.md"
OUTPUT_FILE = "respuestas.csv"


def parse_answers(filepath):
    answers = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            # Match table rows with pipe-separated cells
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # Process pairs of (pregunta, respuesta) columns
            for i in range(0, len(cells) - 1, 2):
                q, a = cells[i], cells[i + 1]
                if re.fullmatch(r"\d+", q) and re.fullmatch(r"[A-Da-d]|ANULADA", a):
                    answers[int(q)] = a.upper()
    return answers


def main():
    answers = parse_answers(ANSWERS_FILE)
    if not answers:
        print("No se encontraron respuestas.", file=sys.stderr)
        sys.exit(1)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["pregunta", "respuesta"])
        for q in sorted(answers):
            writer.writerow([q, answers[q]])

    print(f"CSV generado: {OUTPUT_FILE} ({len(answers)} preguntas)")


if __name__ == "__main__":
    main()
