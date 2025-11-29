from sys import stderr


def estrai_errori(input_path: str, output_path: str):
	tried_encodings = ["utf-8", "cp1252", "latin-1"]

	for enc in tried_encodings:
		try:
			with open(input_path, "r", encoding=enc, errors="ignore") as infile, open(
				output_path, "a", encoding="utf-8"
			) as outfile:
				last_tail = None  # Conterrà la "coda" della riga precedente.
				tail = None  # Conterrà la "coda" della riga corrente.

				for line in infile:
					if " ERRORE " not in line and " ERROR " not in line:
						continue

					# Splitta la riga in massimo 3 parti: prima parola, seconda parola ed il resto.
					parts = line.split(" ", 2)
					if len(parts) > 2:
						tail = parts[2:]

					# Se tail è diverso da last_tail, scriviamo la riga e aggiorniamo last_tail.
					if tail != last_tail:
						outfile.write(line)
						last_tail = tail

			print(f"Errors copied successfully in: {output_path}")
			return
		except UnicodeDecodeError:
			print(
				f"Impossibile decodificare con encoding {enc}, provo il prossimo...",
				file=stderr,
			)
	raise RuntimeError(
		f"Non sono riuscito a leggere {input_path} con nessuna delle encoding previste"
	)


def main():
	input_file = "robocopy_log.txt"
	output_file = "robocopy_errors_log.txt"

	estrai_errori(input_file, output_file)


if __name__ == "__main__":
	main()
