import pytest
import logging
import json
from main import main

# Percorso al file CSV per il test
TEST_CSV_PATH = "/mnt/data/test_ingredients.echa.csv"

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

def test_main_snapshot(snapshot, setup_csv, mock_csv_path, caplog):
    # Cattura i log durante l'esecuzione
    with caplog.at_level(logging.INFO):
        main()

    # Crea un oggetto con i log catturati per confrontarli con lo snapshot
    log_output = [record.message for record in caplog.records]

    # Serializza i log come JSON per uno snapshot ordinato
    serialized_log_output = json.dumps(log_output, indent=4)

    # Confronta con lo snapshot salvato usando snapshot
    snapshot.assert_match(serialized_log_output, "main_logs_snapshot")
