FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

COPY src/requirements.txt .

#instalar dependências e pacotes
RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc python3-dev musl-dev

COPY src/ .
COPY tests/ ./tests/

#porta do flask
EXPOSE 5000

#rodar aplicação
 CMD echo "INFO: Executando testes antes de iniciar a aplicação..." && \
     pytest tests/ && \
     echo "INFO: Testes concluídos. Iniciando aplicação Flask..." && \
     exec python app.py


