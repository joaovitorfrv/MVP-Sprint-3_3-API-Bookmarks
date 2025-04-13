FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Criar diretório para o banco de dados SQLite
RUN mkdir -p database

EXPOSE 5003

CMD ["python", "app.py"]
