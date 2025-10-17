import requests
import zipfile
import os
from io import BytesIO

URL = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/f45bkkt8pr-1.zip"
OUT_DIR = "mendeley_data"

def download_mendeley_dataset():
    """
    Baixa e extrai o conjunto de dados de e-mails do Mendeley.
    """
    os.makedirs(OUT_DIR, exist_ok=True)

    r = requests.get(URL, stream=True)
    r.raise_for_status()

    with zipfile.ZipFile(BytesIO(r.content)) as z:
        z.extractall(OUT_DIR)


if __name__ == "__main__":
    download_mendeley_dataset()

