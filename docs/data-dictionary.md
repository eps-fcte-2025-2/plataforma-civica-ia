# Dicionário de Dados

Este documento descreve as entidades, atributos, tipos de dados e relacionamentos do sistema.

## Entidades

![Diagrama Entidade-Relacionamento](https://github.com/eps-fcte-2025-2/plataforma-civica-ia/blob/docs/8-Add-Dicionario-Dados/docs/diagramas/diagrama-entidade-relacionamento.png)

### Denuncia (Denúncia)

Entidade principal que representa uma denúncia de manipulação.

| Atributo | Tipo | Descrição | Restrições | Valores Possíveis |
|----------|------|-----------|------------|-------------------|
| id | UUID | Identificador único da denúncia | Chave primária, Gerado automaticamente | - |
| tipoDenuncia | Enum | Tipo da denúncia | Obrigatório | PARTIDA_ESPECIFICA, ESQUEMA_DE_MANIPULACAO |
| descricao | String | Descrição detalhada da denúncia | Obrigatório | - |
| comoSoube | Enum | Como o denunciante tomou conhecimento | Opcional | VITIMA, TERCEIROS, INTERNET, PRESENCIAL, OBSERVACAO, OUTROS |
| pontualOuDisseminado | Enum | Indica se é um caso isolado ou disseminado | Obrigatório, Valor padrão: PONTUAL | PONTUAL, DISSEMINADO |
| frequencia | Enum | Frequência dos eventos relatados | Obrigatório, Valor padrão: ISOLADO | ISOLADO, FREQUENTE |
| dataDenuncia | DateTime | Data e hora do registro da denúncia | Obrigatório, Gerado automaticamente | - |
| status | Enum | Status atual da denúncia | Obrigatório, Valor padrão: PENDENTE | PENDENTE, EM_ANALISE, APROVADA, REJEITADA, ARQUIVADA |
| observacoes | String | Observações adicionais | Opcional | - |
| municipio | String | Município onde ocorreu o fato | Obrigatório | - |
| uf | String | Unidade federativa onde ocorreu o fato | Obrigatório | - |

**Relacionamentos:**
- 1:N com `Partida` (uma denúncia pode ter várias partidas)
- 1:N com `Clube` (uma denúncia pode envolver vários clubes)
- 1:N com `Pessoa` (uma denúncia pode envolver várias pessoas)
- 1:N com `DenunciaFoco` (uma denúncia pode ter vários focos de manipulação)
- 1:N com `Evidencia` (uma denúncia pode ter várias evidências)

### Partida

Representa uma partida específica relacionada a uma denúncia.

| Atributo | Tipo | Descrição | Restrições | Valores Possíveis |
|----------|------|-----------|------------|-------------------|
| id | UUID | Identificador único da partida | Chave primária, Gerado automaticamente | - |
| torneio | String | Nome do torneio/campeonato | Obrigatório | - |
| dataPartida | DateTime | Data e hora da partida | Obrigatório | - |
| localPartida | String | Local onde a partida foi realizada | Obrigatório | - |
| timeA | String | Nome do primeiro time | Opcional | - |
| timeB | String | Nome do segundo time | Opcional | - |
| observacoes | String | Observações sobre a partida | Opcional | - |
| municipio | String | Município onde ocorreu a partida | Obrigatório | - |
| uf | String | Unidade federativa onde ocorreu a partida | Obrigatório | - |
| denunciaId | UUID | ID da denúncia relacionada | Chave estrangeira | - |

**Relacionamentos:**
- N:1 com `Denuncia` (uma partida pertence a uma denúncia)

### Pessoa

Representa uma pessoa envolvida em uma denúncia.

| Atributo | Tipo | Descrição | Restrições | Valores Possíveis |
|----------|------|-----------|------------|-------------------|
| id | UUID | Identificador único da pessoa | Chave primária, Gerado automaticamente | - |
| nomePessoa | String | Nome da pessoa | Obrigatório | - |
| funcaoPessoa | String | Função/cargo da pessoa | Obrigatório | - |
| denunciaId | UUID | ID da denúncia relacionada | Chave estrangeira, Opcional | - |

**Relacionamentos:**
- N:1 com `Denuncia` (uma pessoa pode estar envolvida em uma denúncia)

### Clube

Representa um clube envolvido em uma denúncia.

| Atributo | Tipo | Descrição | Restrições | Valores Possíveis |
|----------|------|-----------|------------|-------------------|
| id | UUID | Identificador único do clube | Chave primária, Gerado automaticamente | - |
| nomeClube | String | Nome do clube | Obrigatório | - |
| denunciaId | UUID | ID da denúncia relacionada | Chave estrangeira, Opcional | - |

**Relacionamentos:**
- N:1 com `Denuncia` (um clube pode estar envolvido em uma denúncia)

### DenunciaFoco (Foco da Denúncia)

Representa o foco da manipulação em uma denúncia.

| Atributo | Tipo | Descrição | Restrições | Valores Possíveis |
|----------|------|-----------|------------|-------------------|
| id | UUID | Identificador único do foco | Chave primária, Gerado automaticamente | - |
| denunciaId | UUID | ID da denúncia relacionada | Chave estrangeira | - |
| foco | Enum | Tipo do foco da manipulação | Obrigatório | ATLETAS_DIRIGENTES_COMISSAO, APOSTADORES, JUIZES |

**Relacionamentos:**
- N:1 com `Denuncia` (um foco pertence a uma denúncia)
- Restrição única: combinação de `denunciaId` e `foco` deve ser única

### Evidencia (Evidência)

Representa uma evidência anexada a uma denúncia.

| Atributo | Tipo | Descrição | Restrições | Valores Possíveis |
|----------|------|-----------|------------|-------------------|
| id | UUID | Identificador único da evidência | Chave primária, Gerado automaticamente | - |
| nomeOriginal | String | Nome original do arquivo | Obrigatório | - |
| nomeArquivo | String | Nome do arquivo no storage | Obrigatório | - |
| caminhoArquivo | String | Caminho completo do arquivo no storage | Obrigatório | - |
| tamanhoBytes | Int | Tamanho do arquivo em bytes | Obrigatório | - |
| mimeType | String | Tipo MIME do arquivo | Obrigatório | - |
| tipo | Enum | Tipo da evidência | Obrigatório | DOCUMENTO, IMAGEM, VIDEO, AUDIO, OUTRO |
| descricao | String | Descrição da evidência | Opcional | - |
| dataUpload | DateTime | Data e hora do upload | Obrigatório, Gerado automaticamente | - |
| denunciaId | UUID | ID da denúncia relacionada | Chave estrangeira | - |

**Relacionamentos:**
- N:1 com `Denuncia` (uma evidência pertence a uma denúncia)

## Histórico de Versão

| Data | Versão | Descrição | Autor | Revisor |
| ---- | ------ | --------- | ----- | ------- |
| 2025-10-22 | 1.0 | Versão inicial do dicionário de dados com mapeamento de entidades | [Ana Luiza Hoffmann Ferreira](https://github.com/AnHoff) | [Pedro Lucas](https://github.com/AlefMemTav)  |
