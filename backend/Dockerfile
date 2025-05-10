FROM python:alpine

# diretório
WORKDIR /app

#pra ver se o pystest funciona
ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY src/requirements.txt .

#instalar ddependencias
RUN pip install --no-cache-dir -r requirements.txt

#copiar aplicação
COPY src/ .

#copiar testes
COPY tests/ ./tests/

#porta do flask
EXPOSE 5000

#rodar aplicação
CMD ["python", "app.py"]
