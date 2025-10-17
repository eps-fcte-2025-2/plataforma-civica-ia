import requests
import zipfile
import io
import os

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
OUT_DIR = "data"
OUT_FILE = os.path.join(OUT_DIR, "SMSSpamCollection.txt")

def download_sms_spam():
    os.makedirs(OUT_DIR, exist_ok=True)
    response = requests.get(URL)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(OUT_DIR)
    print(f" Arquivo salvo em: {OUT_FILE}")

if __name__ == "__main__":
    download_sms_spam()
