import requests
import os

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.data"
NAMES_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.names"

OUT_DIR = "data"
DATA_FILE = os.path.join(OUT_DIR, "spambase.csv")
NAMES_FILE = os.path.join(OUT_DIR, "spambase.names")

def download_spambase():
    os.makedirs(OUT_DIR, exist_ok=True)
    data = requests.get(URL)
    data.raise_for_status()
    with open(DATA_FILE, "wb") as f:
        f.write(data.content)
    names = requests.get(NAMES_URL)
    names.raise_for_status()
    with open(NAMES_FILE, "wb") as f:
        f.write(names.content)
    print(f"Arquivos salvos em: {OUT_DIR}")

if __name__ == "__main__":
    download_spambase()
