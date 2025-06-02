# 1. Use uma imagem base oficial do Python
FROM python:3.9-slim

# 2. Defina o diretório de trabalho dentro do contêiner
WORKDIR /app_mini

# 3. Variáveis de ambiente para otimizar o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Copie o arquivo de dependências primeiro para otimizar o cache de camadas
COPY requirements.txt .

# 5. Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copie todo o código da aplicação (a pasta 'app' e o 'run.py')
# Certifique-se que a estrutura de pastas no COPY está correta
COPY ./app ./app  # Copia a pasta 'app' local para a pasta 'app' dentro de /app_mini
COPY run.py .     # Copia o run.py local para a raiz de /app_mini

# 7. Defina o comando para executar sua aplicação usando Gunicorn
#    $PORT é fornecido pelo Cloud Run. 'run:app' refere-se ao objeto 'app' no arquivo 'run.py'.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 "run:app"