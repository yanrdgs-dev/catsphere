# Use uma imagem base do Python
FROM python:3.9-slim

# Instale gcc
RUN apt-get update && apt-get install -y gcc

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Crie o diretório para os arquivos JSON
RUN mkdir -p /app/controllers/db

# Copie o restante do código da aplicação para o contêiner
COPY . .

# Exponha a porta que a aplicação irá rodar
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["python", "route.py"]
