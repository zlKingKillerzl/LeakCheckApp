# Importa os módulos necessários do Flask
from flask import Flask, request, jsonify, send_from_directory
# Importa requests para fazer requisições HTTP para a API externa
import requests
# Importa Flask-CORS para lidar com políticas de Cross-Origin Resource Sharing
from flask_cors import CORS
# Importa o módulo os para interagir com o sistema operacional (variáveis de ambiente)
import os
# Importa load_dotenv para carregar variáveis de ambiente de um arquivo .env
from dotenv import load_dotenv
# Importa o Limit e Limiter para implementar limitação de taxa
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Carrega as variáveis de ambiente do arquivo .env
# Isso deve ser feito antes de acessar qualquer variável de ambiente
load_dotenv()

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# --- Configuração de Segurança e Desempenho ---

# Habilita CORS para todas as rotas. Em produção, considere restringir a origens específicas:
# CORS(app, resources={r"/api/*": {"origins": "https://seu-dominio.com"}})
CORS(app)

# Carrega a chave da API LeakCheck de uma variável de ambiente.
# É CRÍTICO para a segurança que esta chave NÃO seja hardcoded em produção.
# Para desenvolvimento local, defina LEAKCHECK_API_KEY no seu arquivo .env.
LEAKCHECK_API_KEY = os.getenv("LEAKCHECK_API_KEY")

# Verifica se a chave da API foi carregada. Se não, a aplicação não deve iniciar corretamente.
if not LEAKCHECK_API_KEY:
    print("ERRO CRÍTICO: A variável de ambiente LEAKCHECK_API_KEY não está definida.")
    print("Por favor, defina-a no seu ambiente ou em um arquivo .env.")
    # Em um ambiente de produção, você pode querer levantar uma exceção ou sair.
    # raise ValueError("LEAKCHECK_API_KEY não configurada.")

# Define a URL base da API original do LeakCheck
LEAKCHECK_BASE_URL = "https://leakcheck.io/api/v2/query/"

# Configura o Flask-Limiter para limitação de taxa
# Limita a 10 requisições por minuto por endereço IP remoto
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute", "1 per second"], # Limites padrão
    storage_uri="memory://", # Armazenamento em memória (simples, para um único processo)
    # Em produção, use um armazenamento persistente como Redis: storage_uri="redis://localhost:6379"
)

# --- Rotas da Aplicação ---

@app.route("/")
@limiter.exempt # Exclui a rota principal da limitação de taxa
def serve_index():
    """
    Serve o arquivo index.html quando a raiz do servidor é acessada.
    O arquivo index.html deve estar na mesma pasta que app.py (ou em 'templates' se configurado).
    """
    # Para uma aplicação Flask padrão, 'index.html' estaria em uma pasta 'templates'.
    # Como o seu index.html está no mesmo nível, usamos os.getcwd().
    return send_from_directory(os.getcwd(), 'index.html')

@app.route("/api/v2/query/<path:query_value>", methods=["GET"])
# Aplica a limitação de taxa para este endpoint
@limiter.limit("5 per minute") # Exemplo: 5 requisições por minuto para este endpoint específico
def proxy_leakcheck_query(query_value):
    """
    Função que atua como proxy seguro para a API LeakCheck.
    Recebe a consulta do frontend, adiciona a chave da API (do backend) e repassa para a API LeakCheck.
    Retorna a resposta da API LeakCheck para o frontend.
    """
    # Verifica novamente se a chave da API está configurada antes de fazer a requisição externa
    if not LEAKCHECK_API_KEY:
        return jsonify({"success": False, "error": "LeakCheck API key not configured on the server."}), 500

    # Validação básica de entrada para query_value
    if not query_value or len(query_value) < 3:
        return jsonify({"success": False, "error": "Query muito curta. Mínimo de 3 caracteres."}), 400
    
    # Obtém o tipo de consulta dos parâmetros da URL (ex: ?type=email)
    query_type = request.args.get("type", "auto")

    # Constrói a URL completa para a API original do LeakCheck
    leakcheck_url = f"{LEAKCHECK_BASE_URL}{query_value}"
    if query_type != "auto":
        # Adiciona o tipo de consulta como parâmetro URL
        leakcheck_url += f"?type={query_type}"

    # Define os cabeçalhos para a requisição à API original do LeakCheck
    headers = {
        "Accept": "application/json",
        "X-API-Key": LEAKCHECK_API_KEY # A chave da API é adicionada aqui, segura no backend
    }

    try:
        # Faz a requisição GET para a API original do LeakCheck
        response = requests.get(leakcheck_url, headers=headers, timeout=10) # Adicionado timeout
        response.raise_for_status() # Levanta um HTTPError para respostas de erro (4xx ou 5xx)
        
        # Retorna a resposta JSON da API LeakCheck e o código de status original
        return jsonify(response.json()), response.status_code
    
    except requests.exceptions.HTTPError as e:
        # Captura e repassa erros HTTP da API LeakCheck (ex: 400, 401, 403, 429)
        print(f"Erro HTTP da API LeakCheck: {e.response.status_code} - {e.response.text}")
        try:
            # Tenta retornar o erro JSON da API LeakCheck, se disponível
            return jsonify(e.response.json()), e.response.status_code
        except ValueError:
            # Se a resposta não for JSON, retorna uma mensagem de erro genérica
            return jsonify({"success": False, "error": f"Erro da API LeakCheck: {e.response.status_code} - {e.response.text}"}), e.response.status_code
    except requests.exceptions.ConnectionError:
        # Captura erros de conexão (ex: API offline, problema de rede)
        print("Erro de conexão: Não foi possível conectar à API LeakCheck.")
        return jsonify({"success": False, "error": "Falha ao conectar à API LeakCheck. Verifique a conexão de rede."}), 503
    except requests.exceptions.Timeout:
        # Captura erros de tempo limite da requisição
        print("Erro de tempo limite: A requisição à API LeakCheck excedeu o tempo limite.")
        return jsonify({"success": False, "error": "A requisição à API LeakCheck excedeu o tempo limite."}), 504
    except requests.exceptions.RequestException as e:
        # Captura quaisquer outras exceções de requisição inesperadas
        print(f"Ocorreu um erro inesperado ao fazer a requisição: {e}")
        return jsonify({"success": False, "error": f"Ocorreu um erro inesperado: {e}"}), 500

# Ponto de entrada para a aplicação Flask
if __name__ == "__main__":
    # Em ambiente de produção, certifique-se de que debug=False.
    # Use um servidor WSGI como Gunicorn para produção (gunicorn app:app).
    app.run(debug=True, port=5000)
