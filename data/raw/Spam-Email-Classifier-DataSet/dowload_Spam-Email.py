import requests
import zipfile
import os
from io import BytesIO

URL = "https://github.com/zrz1996/Spam-Email-Classifier-DataSet/blob/master/spam.zip"
OUT_DIR = "data"

def download_spam_dataset():
    """
    Baixa e extrai o conjunto de dados de e-mails de spam.
    """
    os.makedirs(OUT_DIR, exist_ok=True)

    r = requests.get(URL, stream=True)
    r.raise_for_status()

    with zipfile.ZipFile(BytesIO(r.content)) as z:
        z.extractall(OUT_DIR)


if __name__ == "__main__":
    download_spam_dataset()

