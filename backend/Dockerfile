FROM python:alpine

# diretório
WORKDIR /app

COPY src/requirements.txt .

#instalar ddependencias
RUN pip install --no-cache-dir -r requirements.txt

#copiar aplicação
COPY src/ .

#porta do flask
EXPOSE 5000

#rodar aplicação
CMD ["python", "app.py"]
