import subprocess
import re
import os

def convert_to_pdf(folder, source, timeout=None):
    # Caminho completo do arquivo de origem
    source_path = os.path.join(folder, source)
    
    # Checar se o arquivo de origem existe
    if not os.path.exists(source_path):
        print(f"Arquivo {source_path} não encontrado!")
        return None

    # Argumentos para a conversão com o LibreOffice
    args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', folder, source_path]
    
    try:
        # Executa o comando de conversão
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        output = process.stdout.decode()

        # Verifica a saída do processo para encontrar o nome do arquivo gerado
        match = re.search(r'-> (.*?) using filter', output)
        if match:
            # Extrair o nome do arquivo PDF gerado
            pdf_filename = os.path.basename(match.group(1))
            print(f"PDF gerado com sucesso: {pdf_filename}")
            return pdf_filename
        else:
            print(f"Falha na conversão para PDF: {output}")
            return None
    except subprocess.TimeoutExpired:
        print("Tempo limite de conversão excedido!")
        return None
