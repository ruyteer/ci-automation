from flask import Flask, render_template, request, send_from_directory
import os
from PyPDF2 import PdfReader
import re

app = Flask(__name__)

# Função para extrair dados do PDF
def extract_data_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    data = {
        'codigo_requisicao': None,
        'solicitante': None,
        'local_entrega': None,
        'justificativa': None,
        'valor_total': None,
        'itens': []
    }

    # Percorrer todas as páginas do PDF
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text = text.replace('\n', ' ').strip()

            codigo_match = re.search(r'REQDF[-\s]*(\d+)', text)
            if codigo_match:
                data['codigo_requisicao'] = f"REQDF-{codigo_match.group(1).strip()}"

            solicitante_match = re.search(r'Solicitante\s+([A-Z\s]+)\s+Fornecedor', text)
            if solicitante_match:
                data['solicitante'] = solicitante_match.group(1).strip()

            local_entrega_match = re.search(r'Local para Entrega\s+(.*?)\s+Telefone', text)
            if local_entrega_match:
                data['local_entrega'] = local_entrega_match.group(1).strip()

            justificativa_match = re.search(r'Justificativa\s+(.*?)(?=\s+Linhas)', text, re.DOTALL)
            if justificativa_match:
                justificativa = justificativa_match.group(1).replace('\n', ' ').strip()
                data['justificativa'] = ' '.join(justificativa.split())

            valor_total_match = re.search(r'Valor da Requisição\s+([\d.,]+)\s+BRL', text)
            if valor_total_match:
                data['valor_total'] = valor_total_match.group(1).strip()

            itens_match = re.search(r'Linhas(.*?)(?=Solicitante)', text, re.DOTALL)
            if itens_match:
                itens_text = itens_match.group(1).strip()
                item_lines = re.split(r'\s*(?=\d+\s+ES\.)', itens_text)

                header_to_remove = "LinhaItem Descrição Nomeda CategoriaQuantid adeUDM Preço Valor(BRL) Status"
                cleaned_item_lines = [item.replace(header_to_remove, '').strip() for item in item_lines if item]

                for item in cleaned_item_lines:
                    item = item.replace('\n', ' ').strip()
                    item = re.sub(r'(\d+)\s*(ES\.)', r'\1, \2', item)
                    item = re.sub(r'(?<=\d)\s+', r' ', item)
                    item = re.sub(r'\s+(PC|BRL)\s+', r' \1 ', item)
                    item = re.sub(r'\s+', ' ', item)
                    if item:
                        data['itens'].append(item.strip())

    return data

@app.route("/", methods=["GET", "POST"])
def home():
    # Cria o diretório 'uploads' se não existir
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.pdf'):
            pdf_path = os.path.join("uploads", uploaded_file.filename)
            uploaded_file.save(pdf_path)
            data = extract_data_from_pdf(pdf_path)
            return render_template("index.html", data=data, pdf_filename=uploaded_file.filename)
    return render_template("index.html", data=None, pdf_filename=None)

@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
