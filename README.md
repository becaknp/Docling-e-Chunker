# Docling-e-Chunker
# Processador de Contratos

Um script simples para converter contratos PDF/DOCX em Markdown e quebrar em pedaços (chunks).

## O que faz?

- Pega contratos da pasta `contratos/`
- Converte para Markdown (vai para `markdown_output/`)
- Quebra em chunks menores (vai para `neo4j_chunks/`)
- Gera JSON pronto para usar no Neo4j

## Como usar?

1. Instale as bibliotecas:
```bash
pip install docling
pip install chonkie
