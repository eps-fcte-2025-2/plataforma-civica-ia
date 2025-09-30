import os
import pandas as pd

from data.scripts.prep_dataset import clean_text, simple_tokenize, prepare_dataframe, split_dataframe


def test_clean_text():
    s = "<p>Olá &amp; bem-vindo! ação.</p>"
    cleaned = clean_text(s)
    assert "olá" in cleaned or "ola" in cleaned
    assert "<" not in cleaned


def test_simple_tokenize():
    tokens = simple_tokenize("uma frase simples")
    assert tokens == ["uma", "frase", "simples"]


def test_prepare_dataframe_and_schema(tmp_path):
    df = pd.DataFrame({"text": ["Olá mundo", "Teste"], "label": ["a", "b"]})
    processed = prepare_dataframe(df)
    assert list(processed.columns) == ["id", "texto_original", "texto_limpo", "label", "origem"]
    assert len(processed) == 2


def test_split_dataframe():
    df = pd.DataFrame({"id": [1,2,3,4,5,6,7,8,9,10], "texto_original": ["a"]*10, "texto_limpo":["a"]*10, "label":["x"]*10, "origem":["s"]*10})
    train, val, test = split_dataframe(df, seed=123, ratios=(0.7,0.15,0.15))
    assert len(train) + len(val) + len(test) == 10
    # taxa aproximada
    assert len(train) == 7
