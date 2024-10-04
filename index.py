from flask import Flask, render_template, request, send_from_directory
import os
from PyPDF2 import PdfReader
import re
from docx import Document
from docxtpl import DocxTemplate

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

    return data

@app.route("/", methods=["GET", "POST"])
def home():
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

@app.route('/gerar_ci', methods=["POST"])
def gerar_ci():
    # Pegar os dados do formulário
    data = {
        'codigo_requisicao': request.form['codigo_requisicao'],
        'solicitante': request.form['solicitante'],
        'local_entrega': request.form['local_entrega'],
        'justificativa': request.form['justificativa'],
        'valor_total': request.form['valor_total'],
        'motivo': request.form['motivo'],
        'cod_arq': request.form['cod_arq'],
        'date': request.form['data'],
        'itens': []
    }

    # Pegar os itens do formulário
    quantidades = request.form.getlist('quantidade[]')
    descricoes = request.form.getlist('descricao[]')
    precos = request.form.getlist('preco[]')

    

    for i in range(len(quantidades)):
        item = {
            'quantidade': quantidades[i],
            'descricao': descricoes[i],
            'preco': precos[i]
        }
        data['itens'].append(item)

    # Preencher o modelo Word
    word_output_path = os.path.join("uploads", "CI_preenchida.docx")
    preencher_modelo_word(data, word_output_path)

    # Retornar o arquivo Word preenchido para o usuário baixar
    return send_from_directory('uploads', "CI_preenchida.docx", as_attachment=True)


def preencher_modelo_word(data, word_output_path):
    doc = DocxTemplate("modelo_ci.docx")

    context = {
        'COD_ARQ': data['cod_arq'],
        'DATA': data['date'],
        'CODIGO': data['codigo_requisicao'],
        'SOLICITANTE': data['solicitante'],
        'LOCAL_ENTREGA': data['local_entrega'],
        'VALOR_TOTAL': data['valor_total'],
        'JUSTIFICATIVA': data['justificativa'],
        'ITENS': [f'{item['quantidade']} {item['descricao']} {item['preco']}' for item in data['itens']]
    }

    # Renderiza o template
    doc.render(context)

    # Salva o documento preenchido
    doc.save(word_output_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)