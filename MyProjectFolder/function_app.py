import azure.functions as func
import csv
import os
import logging

app = func.FunctionApp()

# Path del file CSV caricato
CSV_FILE_PATH = r"/workspaces/2023-25.BD.UFS14/MyProjectFolder/ingredients.echa.csv"

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:

    # Recupera il parametro "name" dalla richiesta, valore predefinito "Formaldehyde"
    nome = req.params.get("name", "Formaldehyde")

    # Verifica se il file esiste
    if not os.path.exists(CSV_FILE_PATH):
        logging.error("File CSV non trovato.")
        return func.HttpResponse("File CSV non trovato", status_code=500)

    try:
        # Leggi il file CSV
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Cerca la riga che corrisponde al nome
            for row in reader:
                if row.get("name", "").lower() == nome.lower():
                    
                    # Restituisce il valore della colonna "ViaInhalationRoute" se presente
                    return func.HttpResponse(
                        row.get("ViaInhalationRoute", "Dati non disponibili")
                    )
            # Se il nome non è trovato
            return func.HttpResponse("Ingrediente non trovato", status_code=404)
    except Exception as e:
        logging.error(f"Errore durante la lettura del file CSV: {str(e)}")
        return func.HttpResponse("Errore durante la lettura del file CSV", status_code=500)
