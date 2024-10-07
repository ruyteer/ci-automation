from flask import Flask, render_template, request, send_from_directory, send_file
import os
from functions.get_req import get_data_from_req
from functions.generate_ci import preencher_modelo_word
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
        'name_file': request.form['name_file'],
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
    pdf_filename = preencher_modelo_word(data, word_output_path)

    if not pdf_filename:
        return "Erro ao gerar o arquivo PDF", 500

    # Criar o arquivo ZIP contendo o Word e o PDF
    zip_filename = f"{data['name_file']}.zip"
    zip_path = os.path.join("uploads", zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(word_output_path, os.path.basename(word_output_path))
        zipf.write(os.path.join("uploads", pdf_filename), pdf_filename)

    # Retornar o arquivo ZIP para o usuário baixar
    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
