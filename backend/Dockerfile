FROM python:alpine

# diretório
WORKDIR /app

#pra ver se o pystest funciona
ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY src/requirements.txt .

#instalar ddependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY tests/ ./tests/

#porta do flask
EXPOSE 5000

#rodar aplicação
CMD echo "INFO: Executando testes antes de iniciar a aplicação..." && \
    pytest tests/ && \
    echo "INFO: Testes concluídos. Iniciando aplicação Flask..." && \
    exec python app.py

