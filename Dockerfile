# Usa uma imagem base Python oficial leve
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta em que a aplicação Flask será executada
EXPOSE 5000

# Define a variável de ambiente para a chave da API LeakCheck
# ATENÇÃO: Substitua "SUA_CHAVE_LEAKCHECK_AQUI" pela sua chave real da API LeakCheck.
# Para ambientes de produção, é ALTAMENTE RECOMENDADO passar esta chave via variáveis de ambiente do Docker.
ENV LEAKCHECK_API_KEY="SUA_CHAVE_LEAKCHECK_AQUI"

# Comando para executar a aplicação Flask quando o contêiner for iniciado
# Usa Gunicorn para um servidor de produção mais robusto (instale com pip install gunicorn)
# Se não quiser usar Gunicorn, pode usar: CMD ["python", "app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
