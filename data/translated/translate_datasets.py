import pandas as pd
import requests
import json
import os
import time
from typing import List, Dict
import re

class DatasetTranslator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Termos sensíveis que devem ser preservados (podem ser expandidos)
        self.sensitive_terms = {
            'RT', 'FBI', 'CIA', 'GDPR', 'LGPD', 'CPF', 'CNPJ', 'OAB', 'STF', 'STJ',
            'MP', 'DEA', 'INTERPOL', 'UEFA', 'FIFA', 'CBF', 'COB', 'TSE', 'PIX'
        }
        
    def create_translation_prompt(self, text: str) -> str:
        """Cria prompt para tradução preservando termos sensíveis"""
        
        prompt_template = f"""
        TRADUZA o seguinte texto para português brasileiro PRESERVANDO termos sensíveis.

        REGRAS CRÍTICAS:
        1. PRESERVE todos os termos jurídicos, siglas, nomes próprios e termos técnicos NO ORIGINAL
        2. Preserve a estrutura e formato do texto
        3. Adapte apenas a linguagem natural para português brasileiro
        4. Mantenha palavrões e termos ofensivos equivalentes no contexto brasileiro

        TERMOS SENSÍVEIS PARA PRESERVAR (NÃO TRADUZIR):
        {', '.join(self.sensitive_terms)}

        TEXTO PARA TRADUZIR: "{text}"

        APENAS RETORNE A TRADUÇÃO, SEM EXPLICAÇÕES.
        TRADUÇÃO:
        """
        
        return prompt_template
    
    def extract_sensitive_terms(self, text: str) -> List[str]:
        """Extrai termos sensíveis do texto"""
        found_terms = []
        words = re.findall(r'\b[A-Z]{2,}\b', text)  # Siglas em maiúsculas
        for word in words:
            if word in self.sensitive_terms:
                found_terms.append(word)
        return found_terms
    
    def translate_text(self, text: str, max_retries: int = 3) -> str:
        """Traduz texto usando API do DeepSeek"""
        
        if pd.isna(text) or text == "":
            return text
            
        for attempt in range(max_retries):
            try:
                prompt = self.create_translation_prompt(text)
                
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 1000
                }
                
                response = requests.post(
                    self.api_url, 
                    headers=self.headers, 
                    json=payload, 
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    translated_text = result['choices'][0]['message']['content'].strip()
                    
                    # Verifica se termos sensíveis foram preservados
                    original_terms = self.extract_sensitive_terms(text)
                    preserved_terms = self.extract_sensitive_terms(translated_text)
                    
                    if set(original_terms) != set(preserved_terms):
                        print(f"Aviso: Alguns termos podem não ter sido preservados: {original_terms}")
                    
                    return translated_text
                    
                else:
                    print(f"Erro API: {response.status_code} - {response.text}")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"Erro na tentativa {attempt + 1}: {str(e)}")
                time.sleep(2)
                
        return text  # Retorna original se falhar
    
    def translate_dataset(self, input_path: str, output_dir: str, sample_size: int = None):
        """Traduz dataset completo"""
        
        # Carregar dataset
        df = pd.read_csv(input_path)
        
        if sample_size:
            df = df.head(sample_size)
        
        print(f"Iniciando tradução de {len(df)} registros...")
        
        # Criar coluna traduzida
        df['tweet_pt'] = ""
        translations_log = []
        
        for idx, row in df.iterrows():
            original_text = row['tweet']
            
            print(f"Traduzindo registro {idx + 1}/{len(df)}")
            translated_text = self.translate_text(original_text)
            
            df.at[idx, 'tweet_pt'] = translated_text
            
            # Log para relatório
            translations_log.append({
                'index': idx,
                'original': original_text,
                'translated': translated_text,
                'preserved_terms': self.extract_sensitive_terms(original_text)
            })
            
            time.sleep(0.5)  # Rate limiting
            
        # Salvar dataset traduzido
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'dataset_traduzido.csv')
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        # Gerar relatório
        self.generate_report(translations_log, output_dir)
        
        return df, translations_log
    
    def generate_report(self, translations_log: List[Dict], output_dir: str):
        """Gera relatório de tradução"""
        
        report_path = os.path.join(output_dir, 'relatorio_traducao.txt')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE TRADUÇÃO - PLATAFORMA CÍVICA DIGITAL\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("EXEMPLOS DE TRADUÇÃO (ANTES/DEPOIS):\n")
            f.write("-" * 40 + "\n\n")
            
            for i, log in enumerate(translations_log[:20]):  # Primeiros 20 exemplos
                f.write(f"Exemplo {i + 1}:\n")
                f.write(f"ORIGINAL: {log['original']}\n")
                f.write(f"TRADUZIDO: {log['translated']}\n")
                f.write(f"TERMOS PRESERVADOS: {log['preserved_terms']}\n")
                f.write("-" * 40 + "\n\n")
            
            # Estatísticas
            total_terms = sum(len(log['preserved_terms']) for log in translations_log)
            f.write(f"RESUMO ESTATÍSTICO:\n")
            f.write(f"Total de registros traduzidos: {len(translations_log)}\n")
            f.write(f"Total de termos sensíveis preservados: {total_terms}\n")

def main():
    # Configuração
    API_KEY = ""  # Substitua pela sua API key
    INPUT_CSV = "../raw/hate_speech/datasets/hate_speech_offensive_language/archive/labeled_data.csv"
    OUTPUT_DIR = "./hate_speech_translated"
    
    # Inicializar tradutor
    translator = DatasetTranslator(API_KEY)
    
    # Traduzir dataset (usar sample_size=None para dataset completo)
    df_translated, log = translator.translate_dataset(
        input_path=INPUT_CSV,
        output_dir=OUTPUT_DIR,
        sample_size=20  # Apenas para teste - remover para produção
    )
    
    print("Tradução concluída!")
    print(f"Dataset salvo em: {OUTPUT_DIR}/dataset_traduzido.csv")
    print(f"Relatório salvo em: {OUTPUT_DIR}/relatorio_traducao.txt")

if __name__ == "__main__":
    main()