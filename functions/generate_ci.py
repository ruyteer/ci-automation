from docxtpl import DocxTemplate
import aspose.words as aw
import pypandoc
from functions.helpers.convert_pdf import convert_to_pdf
import os

from docx import Document


def preencher_modelo_word(data, word_output_path):
    # Carregar o template
    doc = DocxTemplate("modelo_ci.docx")

    # Definir o contexto
    context = {
        'COD_ARQ': data['cod_arq'],
        'DATA': data['date'],
        'CODIGO': data['codigo_requisicao'],
        'SOLICITANTE': data['solicitante'],
        'LOCAL_ENTREGA': data['local_entrega'],
        'VALOR_TOTAL': data['valor_total'],
        'JUSTIFICATIVA': data['justificativa'],
        'MOTIVO': data['motivo'],
        'EMPRESA': data['empresa'],
        'ITENS': []
    }

    # Preencher itens
    for item in data['itens']:
        formatted_item = f"{item['quantidade']} | {item['descricao']} | R$ {item['preco']}"
        context['ITENS'].append(formatted_item)

    # Renderiza o template Word
    doc.render(context)

    # Salva o documento Word preenchido
    doc.save(word_output_path)

    # Extrair o nome do arquivo Word
    # word_filename = os.path.basename(word_output_path)

    # Converte o arquivo Word para PDF
    # pdf_filename = convert_to_pdf(folder="uploads", source=word_filename, timeout=15)

   

def preencher_modelo_compras(data, word_output_path):
    # Carregar o template
    doc = DocxTemplate("modelo_compras.docx")

    # Definir o contexto
    context = {
        'COD_ARQ': data['cod_arq'],
        'DATA': data['date'],
        'CODIGO': data['codigo_requisicao'],
        'SOLICITANTE': data['solicitante'],
        'LOCAL_ENTREGA': data['local_entrega'],
        'VALOR_TOTAL': data['valor_total'],
        'JUSTIFICATIVA': data['justificativa'],
        'MOTIVO': data['motivo'],
        'EMPRESA': data['empresa'],
        'ITENS': []
    }

    # Preencher itens
    for item in data['itens']:
        formatted_item = f"{item['quantidade']} | {item['descricao']} | R$ {item['preco']}"
        context['ITENS'].append(formatted_item)

    # Renderiza o template Word
    doc.render(context)

    # Salva o documento Word preenchido
    doc.save(word_output_path)

    # Extrair o nome do arquivo Word
    # word_filename = os.path.basename(word_output_path)

    # Converte o arquivo Word para PDF
    # pdf_filename = convert_to_pdf(folder="uploads", source=word_filename, timeout=15)
