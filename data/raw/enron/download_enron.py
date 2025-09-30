import requests
import tarfile
import os

URL = "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz"
OUT_DIR = "data"
OUT_FILE = os.path.join(OUT_DIR, "enron_mail_20150507.tar.gz")

def download_enron():
    os.makedirs(OUT_DIR, exist_ok=True)
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        with open(OUT_FILE, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    with tarfile.open(OUT_FILE, "r:gz") as tar:
        tar.extractall(OUT_DIR)
    print(f"Extraído em: {OUT_DIR}")

if __name__ == "__main__":
    download_enron()
