# Dados

Decisões tomadas para o pipeline de pré-processamento:

- Schema comum (arquivo CSV processado):
  - `id` (string): identificador único da instância
  - `texto_original` (string): o texto original extraído do dataset bruto
  - `texto_limpo` (string): texto após limpeza (remoção de HTML, normalização de acentuação, lowercase)
  - `label` (string|None): rótulo/target quando disponível
  - `origem` (string|None): fonte ou nome do dataset quando disponível

- Splits: `train.csv`, `val.csv`, `test.csv` com proporções padrão 70/15/15 e seed fixo (default=42).
- Logs de execução são gravados em `process_log.txt` dentro do diretório de saída.

Usage básico:

```bash
python data/scripts/prep_dataset.py --input data/raw/sample_raw.csv --output-dir data/processed --seed 42
```
