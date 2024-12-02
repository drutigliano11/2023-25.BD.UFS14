import csv
import logging

# Path del file CSV caricato
CSV_FILE_PATH = "/mnt/data/ingredients.echa.csv"

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Avvio dell'applicazione...")

    # Nome da cercare (input simulato)
    nome = "Formaldehyde"

    # Verifica se il file esiste
    try:
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("name", "").lower() == nome.lower():
                    logging.info(f"Ingrediente trovato: {row}")
                    logging.info(f"ViaInhalationRoute: {row.get('ViaInhalationRoute', 'Dati non disponibili')}")
                    return

            logging.warning("Ingrediente non trovato")
    except FileNotFoundError:
        logging.error("File CSV non trovato.")
    except Exception as e:
        logging.error(f"Errore durante la lettura del file CSV: {str(e)}")

if __name__ == "__main__":
    main()
