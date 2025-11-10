import os
import json
from docling.document_converter import DocumentConverter
from chonkie import RecursiveChunker

# pastas
PASTA_CONTRATOS = "contratos"
PASTA_SAIDA_MD = "markdown_output"
PASTA_CHUNKS = "neo4j_chunks"

# cria pastas se não existirem
os.makedirs(PASTA_SAIDA_MD, exist_ok=True)
os.makedirs(PASTA_CHUNKS, exist_ok=True)

# inicializa chunker
chunker = RecursiveChunker()

# função para processar um contrato
def processar_contrato(caminho_arquivo):
    nome_base, _ = os.path.splitext(os.path.basename(caminho_arquivo))
    print(f"\nProcessando contrato: {nome_base}")

    # converte PDF/DOCX para Markdown via Docling
    converter = DocumentConverter()
    documento = converter.convert(caminho_arquivo).document
    markdown = documento.export_to_markdown()

    # salva Markdown
    caminho_md = os.path.join(PASTA_SAIDA_MD, f"{nome_base}.md")
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Markdown salvo em: {caminho_md}")

    # chunking com RecursiveChunker
    chunks = chunker(markdown)
    print(f"Contrato chunked em {len(chunks)} pedaços.")

    # monta JSON pronto para Neo4j
    dados = {
        "documento": nome_base,
        "chunks": [
            {"id": f"{nome_base}_{i+1}", "texto": chunk.text, "tokens": chunk.token_count}
            for i, chunk in enumerate(chunks)
        ]
    }

    # salva JSON
    caminho_json = os.path.join(PASTA_CHUNKS, f"{nome_base}.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"Chunks JSON salvo em: {caminho_json}")

    return chunks

# menu principal
def main():
    arquivos = [f for f in os.listdir(PASTA_CONTRATOS) if f.lower().endswith((".pdf", ".docx"))]
    if not arquivos:
        print(f"Nenhum contrato encontrado na pasta '{PASTA_CONTRATOS}'.")
        return

    while True:
        print("\nContratos disponíveis:")
        for i, nome in enumerate(arquivos, start=1):
            print(f"[{i}] {nome}")
        print("[0] Sair")

        try:
            escolha = int(input("\nDigite o número do contrato para processar: "))
        except ValueError:
            print("Entrada inválida. Digite um número.")
            continue

        if escolha == 0:
            print("Encerrando o programa. Até logo!")
            break

        if not (1 <= escolha <= len(arquivos)):
            print("Opção inválida.")
            continue

        caminho_arquivo = os.path.join(PASTA_CONTRATOS, arquivos[escolha - 1])
        try:
            chunks = processar_contrato(caminho_arquivo)
            print("="*50)
            input("Processo concluído. Pressione Enter para continuar...")
        except Exception as e:
            print(f"Erro durante a conversão: {e}")
            input("Pressione Enter para voltar ao menu...")

# ponto de entrada
if __name__ == "__main__":
    main()
