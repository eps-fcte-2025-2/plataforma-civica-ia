import logging
import pandas as pd
import requests
from requests.exceptions import RequestException
import torch
import os
import time
import re
from typing import List, Dict
from transformers import MarianMTModel, MarianTokenizer
from dotenv import load_dotenv

class DatasetTranslator:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.transformers_model = "Helsinki-NLP/opus-mt-tc-big-en-pt"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.sensitive_terms = {
            'RT', 'FBI', 'CIA', 'GDPR', 'LGPD', 'CPF', 'CNPJ', 'OAB', 'STF', 'STJ',
            'MP', 'DEA', 'INTERPOL', 'UEFA', 'FIFA', 'CBF', 'COB', 'TSE', 'PIX'
        }

    # -------------------------
    # Utilitários internos
    # -------------------------
    def create_translation_prompt(self, text: str) -> str:
        return f"""
        TRADUZA o seguinte texto para português brasileiro PRESERVANDO termos sensíveis.

        REGRAS:
        - Preserve termos jurídicos, siglas, nomes próprios e técnicos.
        - Preserve estrutura e formato.
        - Mantenha linguagem ofensiva no contexto.
        - NÃO traduza: {', '.join(self.sensitive_terms)}

        TEXTO: "{text}"
        TRADUÇÃO:
        """

    def extract_sensitive_terms(self, text: str) -> List[str]:
        return [w for w in re.findall(r'\b[A-Z]{2,}\b', text) if w in self.sensitive_terms]

    # -------------------------
    # Tradução via API DeepSeek
    # -------------------------
    def translate_text(self, text: str, max_retries: int = 3) -> str:
        if pd.isna(text) or not text.strip():
            return text

        for attempt in range(max_retries):
            try:
                payload = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": self.create_translation_prompt(text)}],
                    "temperature": 0.1,
                    "max_tokens": 1000
                }

                r = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
                if r.status_code == 200:
                    return r.json()['choices'][0]['message']['content'].strip()
                time.sleep(2)
            except RequestException as e:
                self.logger.warning("Tentativa %d falhou: %s", attempt + 1, e)
                time.sleep(2)

        return text  # fallback

    def translate_dataset(self, input_path: str, output_dir: str, sample_size: int = None):
        df = pd.read_csv(input_path)
        if sample_size:
            df = df.head(sample_size)

        self.logger.info("Iniciando tradução de %d registros com DeepSeek API...", len(df))
        df["translated_text"] = ""
        translations_log = []

        for i, row in df.iterrows():
            text = row["text"]
            self.logger.debug("Traduzindo %d/%d...", i+1, len(df))
            translated = self.translate_text(text)

            df.at[i, "translated_text"] = translated
            
            translations_log.append({
                "index": i,
                "original": text,
                "translated": translated,
                "preserved_terms": self.extract_sensitive_terms(text)
            })
            time.sleep(0.5)

        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "dataset_traduzido.csv")
        df.to_csv(out_path, index=False, encoding="utf-8")
        self.generate_report(translations_log, output_dir, "DeepSeek API")

        self.logger.info("Tradução concluída. Arquivo salvo em %s", out_path)
        return df, translations_log

    # -------------------------
    # Tradução via HuggingFace
    # -------------------------
    def translate_dataset_with_transformers(self, input_path: str, output_dir: str, text_column_name: str, sample_size: int = None):
        df = pd.read_csv(input_path)
        if sample_size:
            df = df.head(sample_size)

        self.logger.info("Iniciando tradução de %d registros com Hugging Face Transformers...", len(df))

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer = MarianTokenizer.from_pretrained(self.transformers_model)
        model = MarianMTModel.from_pretrained(self.transformers_model).to(device)

        def _translate_text(text: str) -> str:
            if not isinstance(text, str) or not text.strip():
                return text
            batch = tokenizer([text], return_tensors="pt", truncation=True).to(device)
            with torch.no_grad():
                gen = model.generate(**batch, max_length=512)
            return tokenizer.decode(gen[0], skip_special_tokens=True)

        df["translated_text"] = df[text_column_name].apply(_translate_text)

        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "dataset_traduzido_hf.csv")
        df.to_csv(out_path, index=False, encoding="utf-8")

        translations_log = [
            {
                "index": i,
                "original": row[text_column_name],
                "translated": row["translated_text"],
                "preserved_terms": self.extract_sensitive_terms(row[text_column_name])
            }
            for i, row in df.iterrows()
        ]

        self.generate_report(translations_log, output_dir, "Hugging Face Transformers")
        self.logger.info("Tradução concluída. Arquivo salvo em %s", out_path)
        return df

    # -------------------------
    # Relatório
    # -------------------------
    def generate_report(self, translations_log: List[Dict], output_dir: str, method: str):
        report_path = os.path.join(output_dir, "relatorio_traducao.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"RELATÓRIO DE TRADUÇÃO ({method})\n")
            f.write("=" * 60 + "\n\n")

            f.write("AMOSTRAS DE TRADUÇÃO (até 20 exemplos):\n")
            f.write("-" * 60 + "\n")
            for i, log in enumerate(translations_log[:20]):
                f.write(f"Exemplo {i + 1}:\n")
                f.write(f"ORIGINAL: {log['original']}\n")
                f.write(f"TRADUZIDO: {log['translated']}\n")
                f.write(f"TERMOS PRESERVADOS: {log['preserved_terms']}\n")
                f.write("-" * 60 + "\n\n")

            total_terms = sum(len(log['preserved_terms']) for log in translations_log)
            f.write("\nRESUMO:\n")
            f.write(f"Registros traduzidos: {len(translations_log)}\n")
            f.write(f"Termos sensíveis preservados: {total_terms}\n")

        self.logger.info("Relatório salvo em %s", report_path)


# -------------------------
# Execução
# -------------------------
def main():
    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    INPUT_CSV = "../raw/hate_speech/datasets/hate_speech_offensive_language/archive/labeled_data.csv"
    OUTPUT_DIR = "./hate_speech_translated"

    translator = DatasetTranslator(API_KEY)

    # Método 1 — DeepSeek API
    # translator.translate_dataset(INPUT_CSV, OUTPUT_DIR, sample_size=20)

    # Método 2 — Hugging Face
    translator.translate_dataset_with_transformers(
        input_path=INPUT_CSV,
        output_dir=OUTPUT_DIR + "_hf",
        text_column_name="tweet",
        sample_size=20
    )


if __name__ == "__main__":
    main()
