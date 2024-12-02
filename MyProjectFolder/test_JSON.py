import pytest
import logging
from jsonschema import validate
import json
from main import main

# Definizione dello schema JSON
ingredient_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "ViaInhalationRoute": {"type": "string"}
    },
    "required": ["name", "ViaInhalationRoute"]
}

@pytest.fixture
def setup_csv():
    # Percorso del file CSV
    test_csv_path = r"/workspaces/2023-25.BD.UFS14/MyProjectFolder/ingredients.echa.csv"
    test_csv_content = """name,ViaInhalationRoute
Formaldehyde,High Toxicity
Water,Safe
"""
    with open(test_csv_path, "w", encoding="utf-8") as file:
        file.write(test_csv_content)
    yield
    # Pulisce il file CSV dopo il test
    import os
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)

def test_main_with_schema(setup_csv, caplog):
    # Cattura i log durante l'esecuzione di main
    with caplog.at_level(logging.INFO):
        main()

    # Cerca nei log la stringa JSON-like dei dati trovati
    log_output = None
    for record in caplog.records:
        if "Ingrediente trovato:" in record.message:
            log_output = record.message.replace("Ingrediente trovato: ", "").strip()
            break

    # Verifica che i dati siano presenti nei log
    assert log_output is not None, "Nessun dato trovato nei log."

    # Converte i log in un oggetto JSON per validazione
    result = json.loads(log_output)

    # Validazione dello schema JSON
    validate(instance=result, schema=ingredient_schema)

    # Asserzioni aggiuntive sui valori
    assert result["name"] == "Formaldehyde", "Il nome dell'ingrediente è errato."
    assert result["ViaInhalationRoute"] == "High Toxicity", "La ViaInhalationRoute è errata."

