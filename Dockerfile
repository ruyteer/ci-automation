# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos e o código-fonte
COPY requirements.txt .
COPY index.py .
COPY modelo_ci.docx .
COPY modelo_compras.docx .
COPY templates/ templates/
COPY static/ static/
COPY uploads/ uploads
COPY functions/ functions

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Flask usará
EXPOSE 3434

# Comando para iniciar a aplicação
CMD ["python", "index.py"]
