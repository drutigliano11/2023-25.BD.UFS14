import pytest
import logging
from main import main

# Percorso al file CSV per il test
TEST_CSV_PATH = r"/workspaces/2023-25.BD.UFS14/MyProjectFolder/ingredients.echa.csv"

@pytest.fixture
def setup_csv():
    # Scrive un file CSV temporaneo per il test
    test_csv_content = """name,ViaInhalationRoute
Formaldehyde,High Toxicity
Water,Safe
"""
    with open(TEST_CSV_PATH, "w", encoding="utf-8") as file:
        file.write(test_csv_content)
    yield
    # Pulisce il file dopo il test
    import os
    if os.path.exists(TEST_CSV_PATH):
        os.remove(TEST_CSV_PATH)

@pytest.fixture
def mock_csv_path(monkeypatch):
    # Mock del percorso CSV
    monkeypatch.setattr("main.CSV_FILE_PATH", TEST_CSV_PATH)

def test_main_ingredient_found(setup_csv, mock_csv_path, caplog):
    # Cattura i log durante l'esecuzione
    with caplog.at_level(logging.INFO):
        main()

    # Controlla che il log contenga i messaggi corretti
    assert any("Ingrediente trovato" in record.message for record in caplog.records), "Il messaggio 'Ingrediente trovato' non è stato generato."
    assert any("High Toxicity" in record.message for record in caplog.records), "Il valore 'High Toxicity' non è stato trovato nei log."

def test_main_ingredient_not_found(setup_csv, monkeypatch, caplog):
    # Mock del nome da cercare per simulare un ingrediente non trovato
    monkeypatch.setattr("main.nome", "UnknownIngredient")

    # Cattura i log durante l'esecuzione
    with caplog.at_level(logging.INFO):
        main()

    # Controlla che il log contenga il messaggio "Ingrediente non trovato"
    assert any("Ingrediente non trovato" in record.message for record in caplog.records), "Il messaggio 'Ingrediente non trovato' non è stato generato."

def test_main_csv_not_found(monkeypatch, caplog):
    # Mock del percorso CSV inesistente
    monkeypatch.setattr("main.CSV_FILE_PATH", "/mnt/data/nonexistent.csv")

    # Cattura i log durante l'esecuzione
    with caplog.at_level(logging.ERROR):
        main()

    # Controlla che il log contenga il messaggio "File CSV non trovato."
    assert any("File CSV non trovato." in record.message for record in caplog.records), "Il messaggio 'File CSV non trovato' non è stato generato."
