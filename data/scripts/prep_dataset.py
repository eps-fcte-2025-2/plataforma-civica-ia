"""
Script de preparação de datasets.

Funcionalidades:
- Limpeza simples de texto (remoção de HTML, normalização de acentuação, lowercase)
- Tokenização simples (split por whitespace)
- Geração de splits train/val/test com seed fixo
- Leitura de CSVs em data/raw e escrita em data/processed

Uso (CLI):
    python data/scripts/prep_dataset.py --input data/raw/sample_raw.csv --output-dir data/processed --seed 42

"""
from __future__ import annotations

import argparse
import csv
import html
import os
import re
import unicodedata
from typing import List, Tuple

import pandas as pd


RE_COLUMNS = ["id", "texto_original", "texto_limpo", "label", "origem"]


def clean_text(text: str) -> str:
    """Remove HTML, normaliza acentuação, converte para lowercase e colapsa espaços."""
    if text is None:
        return ""
    # Unescape HTML entities
    text = html.unescape(text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Normalize unicode (decompose accents)
    text = unicodedata.normalize("NFKD", text)
    # Remove combining diacritics
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    # Lowercase
    text = text.lower()
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def simple_tokenize(text: str) -> List[str]:
    """Tokenização simples por whitespace."""
    if not text:
        return []
    return text.split()


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Garante o schema comum e produz colunas padronizadas.

    Schema alvo: id, texto_original, texto_limpo, label, origem
    """
    # Encontrar coluna de texto original em variantes comuns
    text_col_candidates = [c for c in df.columns if c.lower() in ("text", "texto", "conteudo", "content")]
    if text_col_candidates:
        text_col = text_col_candidates[0]
    elif "texto_original" in df.columns:
        text_col = "texto_original"
    else:
        # fallback: primeira coluna não numérica
        non_numeric = [c for c in df.columns if df[c].dtype == object]
        text_col = non_numeric[0] if non_numeric else df.columns[0]

    # id
    if "id" not in df.columns:
        df = df.copy()
        df["id"] = range(1, len(df) + 1)

    # label
    label_col = None
    for cand in ("label", "labels", "target"):
        if cand in df.columns:
            label_col = cand
            break

    # origem
    origem_col = None
    for cand in ("origem", "source", "dataset"):
        if cand in df.columns:
            origem_col = cand
            break

    result = pd.DataFrame()
    result["id"] = df["id"].astype(str)
    result["texto_original"] = df[text_col].astype(str)
    result["texto_limpo"] = result["texto_original"].apply(clean_text)
    result["label"] = df[label_col].astype(str) if label_col else None
    result["origem"] = df[origem_col].astype(str) if origem_col else None

    return result[RE_COLUMNS]


def split_dataframe(df: pd.DataFrame, seed: int = 42, ratios: Tuple[float, float, float] = (0.7, 0.15, 0.15)) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split em train/val/test com seed fixo e mantendo ordem aleatória consistente."""
    if abs(sum(ratios) - 1.0) > 1e-8:
        raise ValueError("ratios must sum to 1.0")
    df_shuffled = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    n = len(df_shuffled)
    n_train = int(n * ratios[0])
    n_val = int(n * ratios[1])
    train = df_shuffled.iloc[:n_train]
    val = df_shuffled.iloc[n_train:n_train + n_val]
    test = df_shuffled.iloc[n_train + n_val:]
    return train, val, test


def process_file(input_path: str, output_dir: str, seed: int = 42) -> None:
    try:
        os.makedirs(output_dir, exist_ok=True)
        df = pd.read_csv(input_path)
        processed = prepare_dataframe(df)
        
        # salvar processed full
        full_path = os.path.join(output_dir, "processed.csv")
        processed.to_csv(full_path, index=False, quoting=csv.QUOTE_MINIMAL)

        # gerar splits
        train, val, test = split_dataframe(processed, seed=seed)
        train.to_csv(os.path.join(output_dir, "train.csv"), index=False, quoting=csv.QUOTE_MINIMAL)
        val.to_csv(os.path.join(output_dir, "val.csv"), index=False, quoting=csv.QUOTE_MINIMAL)
        test.to_csv(os.path.join(output_dir, "test.csv"), index=False, quoting=csv.QUOTE_MINIMAL)

        # log
        log_path = os.path.join(output_dir, "process_log.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"input_file: {input_path}\n")
            f.write(f"n_total: {len(processed)}\n")
            f.write(f"n_train: {len(train)}\n")
            f.write(f"n_val: {len(val)}\n")
            f.write(f"n_test: {len(test)}\n")
            f.write(f"seed: {seed}\n")
    
    except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError) as e:
        raise ValueError(f"Erro ao processar arquivo {input_path}: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado no processamento: {str(e)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="CSV de entrada em data/raw")
    parser.add_argument("--output-dir", default="data/processed", help="Diretório de saída")
    parser.add_argument("--seed", type=int, default=42, help="Seed para splits")
    args = parser.parse_args()
    process_file(args.input, args.output_dir, seed=args.seed)


if __name__ == "__main__":
    main()
