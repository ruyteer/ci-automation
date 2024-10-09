from flask import Flask, render_template, request, send_from_directory, send_file
import os
from functions.get_req import get_data_from_req
from functions.generate_ci import preencher_modelo_word
from functions.generate_ci import preencher_modelo_compras
from functions.get_emails import ler_emails
import zipfile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.pdf'):
            pdf_path = os.path.join("uploads", uploaded_file.filename)
            uploaded_file.save(pdf_path)
            data = get_data_from_req(pdf_path)
            return render_template("index.html", data=data, pdf_filename=uploaded_file.filename)
    return render_template("index.html", data=None, pdf_filename=None)


@app.route("/compras", methods=["GET", "POST"])
def compras():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.pdf'):
            pdf_path = os.path.join("uploads", uploaded_file.filename)
            uploaded_file.save(pdf_path)
            data = get_data_from_req(pdf_path)
            return render_template("compras.html", data=data, pdf_filename=uploaded_file.filename)
    return render_template("compras.html", data=None, pdf_filename=None)

@app.route("/emails", methods=["GET"])
def emails():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Ler emails quando a página inicial for carregada
    emails = ler_emails()
    print(emails)
    
    return render_template("emails.html", emails=emails)

@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/gerar_ci_compras', methods=["POST"])
def gerar_ci_compras():
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
        'name_file': request.form['name_file'],
        'empresa': request.form['empresa'],
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

    name_file = f"{data['name_file']}.docx"
    word_output_path = os.path.join("uploads", name_file)

    # Preencher o modelo Word e converter para PDF
    preencher_modelo_compras(data, word_output_path)

    # Retornar o arquivo ZIP para o usuário baixar
    return send_file(word_output_path, as_attachment=True)

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
        'name_file': request.form['name_file'],
        'empresa': request.form['empresa'],
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

    name_file = f"{data['name_file']}.docx"
    word_output_path = os.path.join("uploads", name_file)

    # Preencher o modelo Word e converter para PDF
    preencher_modelo_word(data, word_output_path)

    # Retornar o arquivo ZIP para o usuário baixar
    return send_file(word_output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001, debug=True)

