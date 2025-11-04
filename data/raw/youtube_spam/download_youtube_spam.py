import os
import requests
import zipfile

BASE_OUT_DIR = "datasets"
YOUTUBE_SPAM_DIR = os.path.join(BASE_OUT_DIR, "youtube_spam_collection")


def download_youtube_spam():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00380/YouTube-Spam-Collection-v1.zip"
    zip_path = os.path.join(YOUTUBE_SPAM_DIR, "youtube_spam.zip")

    print("--- Baixando YouTube Spam Collection ---")
    try:
        os.makedirs(YOUTUBE_SPAM_DIR, exist_ok=True)
        print(f"Baixando de: {url}")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Download concluído. Extraindo arquivos para {YOUTUBE_SPAM_DIR}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(YOUTUBE_SPAM_DIR)
        
        os.remove(zip_path)
        print("Extração do YouTube Spam Collection concluída com sucesso.\n")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o YouTube Spam Collection: {e}\n")


if __name__ == "__main__":
    download_youtube_spam()