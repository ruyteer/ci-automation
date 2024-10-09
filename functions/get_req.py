import re
from PyPDF2 import PdfReader

def get_data_from_req(pdf_path):
    reader = PdfReader(pdf_path)
    data = {
        'codigo_requisicao': '',
        'solicitante': '',
        'local_entrega': '',
        'justificativa': '',
        'valor_total': '',
        'itens': []
    }

    for page in reader.pages:
        text = page.extract_text()
        if text:
            text = text.replace('\n', ' ').strip()

        
            codigo_match = re.search(r'REQDF[-\s]*(\d+)', text)
            if codigo_match:
                data['codigo_requisicao'] = f"REQDF-{codigo_match.group(1).strip()}"
            else:
                po_codigo_match = re.search(r'PODF[-\s]*(\d+)', text)
                if po_codigo_match:
                    data['codigo_requisicao'] = f"PODF-{po_codigo_match.group(1).strip()}"


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
