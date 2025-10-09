# Datasets de Spam

Este diretório contém datasets públicos utilizados para treinar um classificador inicial de denúncias em apostas esportivas para a plataforma Apita Cidadão. Tendo como objetivo inicial filtrar denúncias que não se encaixam no padrão pretendido, sejam eslas spam ou denuncias falsas, esse treinamento inicial tem o objetivo de classificar essas denúncias antes de enviar para o banco de dados.

## Tabela de Datasets Catalogados

| Nome                               | Link                                                                                                   | Formato | Idioma                | Licença          | Tipo        | Tamanho                         |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------ | ------- | --------------------- | ---------------- | ----------- | ------------------------------- |
| SMS Spam Collection                | [UCI](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection)                                     | TXT/CSV | EN (traduzível p/ PT) | Research         | SMS         | 5.574 mensagens                 |
| Enron Spam Dataset                 | [CMU](https://www.cs.cmu.edu/~enron/)                                                                  | TXT     | EN                    | Research         | E-mails     | ~500.000 e-mails                |
| Spambase                           | [UCI](https://archive.ics.uci.edu/dataset/94/spambase)                                                 | CSV     | EN                    | CC BY 4.0        | E-mails     | 4.601 instâncias / 58 atributos |
| YouTube Spam Collection            | [UCI](https://archive.ics.uci.edu/dataset/380/youtube+spam+collection)                                 | CSV     | EN                    | Research         | Comentários | 1.956 comentários               |
| Hate Speech and Offensive Language | [Kaggle](https://www.kaggle.com/datasets/mfaaris/hate-speech-and-offensive-language-dataset)           | CSV     | EN                    | Varia            | Tweets      | ~25.000 tweets                  |
| Brazilian Portuguese Hate Speech   | [Hugging Face](https://www.kaggle.com/datasets/hrmello/brazilian-portuguese-hatespeech-dataset/data)                | CSV     | PT-BR                 | Varia            | Tweets      | ~6.900 tweets                   |
| Spam-Email-Classifier-DataSet      | [GitHub](https://github.com/zrz1996/Spam-Email-Classifier-DataSet)                                     | TXT     | EN                    | Não especificada | E-mails     | 1.378 arquivos de texto         |
| SMS PHISHING DATASET               | [Mendeley](https://data.mendeley.com/datasets/f45bkkt8pr/1/files/edb361de-918d-469f-9106-e84823830665) | CSV     | EN                    | CC BY 4.0        | E-mails     | 5.972 instâncias / 5 atributos  |
| LIAR-PLUS                          | [Github](https://github.com/Tariq60/LIAR-PLUS/)                                                        | TSV     | EN                    | CC0 1.0          | E-mails     | ~12.800 / 15 atributos          |

## Seleção de Candidatos

- **SMS Spam Collection** → ideal para spam/propaganda em mensagens curtas.
- **Enron Spam Dataset** → cobre fraude/golpes em e-mails reais corporativos.
- **Spambase** → cobre padrões estatísticos de e-mails (features numéricas).
- **YouTube Spam Collection** → excelente para spam em comentários de redes sociais.
- **Hate Speech and Offensive Language** → focado em identificar conteúdo tóxico, ofensivo e de ódio em textos curtos.
- **Brazilian Portuguese Hate Speech** → essencial para treinar o modelo com as nuances do discurso de ódio em português do Brasil.
- **Spam-Email-Classifier-DataSet** → e-mails para classificação de spam/ham tradicional.
- **SMS PHISHING DATASET** → focado em mensagens de texto (SMS) com tentativas de phishing.
- **LIAR-PLUS** → focado em frases curtas com "níveis de falsidade".

## Estrutura

- `/data/raw/sms_spam/` → SMS Spam Collection
- `/data/raw/enron_spam/` → Enron E-mails
- `/data/raw/spambase/` → Spambase Dataset
- `/data/raw/youtube_spam/` → Youtube Spam Dataset
- `/data/raw/hate_speech/` → Hate Speech Dataset
- `/data/raw/brazilian_hate_speech/` → Brazilian Hate Speech Dataset
- `/data/raw/Spam-Email-Classifier-DataSet/` → Spam-Email-Classifier-DataSet
- `/data/raw/SMS_PHISHING_DATASET/` → SMS_PHISHING_DATASET
- `/data/raw/LIAR-PLUS/` → LIAR-PLUS

---

## Histórico de Versão

| Data       | Versão | Descrição                               | Autor                                                    | Revisor                                                  |
| ---------- | ------ | --------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| 2025-09-30 | 1.0    | Criação inicial do catálogo de datasets | [Gabriel Campello Marques](https://github.com/G16C)      | [Rafael Ferreira Lenadro](https://github.com/RafaelCLG0) |
| 2025-09-30 | 1.1    | Adição de mais datasets                 | [Geovanna Maciel](https://github.com/manuziny)           | [Matheus Henrique](https://github.com/mathonaut)         |
| 2025-09-30 | 1.2    | Adição de datasets                      | [Rafael Ferreira Lenadro](https://github.com/RafaelCLG0) | [Gabriel Campello Marques](https://github.com/G16C)      |
| 2025-09-30 | 1.3    | Adição do dataset LIAR-PLUS             | [Matheus Henrique](https://github.com/mathonaut)         | [Gabriel Campello Marques](https://github.com/G16C)      |
