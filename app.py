# Importa os módulos necessários do Flask e para fazer requisições HTTP
from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS # Importa Flask-CORS para lidar com políticas de CORS
import os # Importa o módulo os para lidar com caminhos de arquivo

# Cria uma instância da aplicação Flask
app = Flask(__name__)
# Habilita CORS para todas as rotas, permitindo que o frontend acesse esta API
CORS(app)

# --- Configuração da Chave da API LeakCheck ---
# ATENÇÃO: Substitua "SUA_CHAVE_LEAKCHECK_AQUI" pela sua chave real da API LeakCheck.
# Para ambientes de produção, é ALTAMENTE RECOMENDADO usar variáveis de ambiente.
LEAKCHECK_API_KEY = "SUA_CHAVE_LEAKCHECK_AQUI" # <-- Insira sua chave aqui!

# Define a URL base da API original do LeakCheck
LEAKCHECK_BASE_URL = "https://leakcheck.io/api/v2/query/"

# --- Nova Rota para servir o index.html ---
@app.route("/")
def serve_index():
    """
    Serve o arquivo index.html quando a raiz do servidor é acessada.
    O arquivo index.html deve estar no mesmo diretório que app.py.
    """
    print("Servindo index.html...")
    return send_from_directory(os.getcwd(), 'index.html')

# Define a rota para a nossa API proxy.
# Ela aceitará requisições GET para /api/v2/query/<query_value>
# O <path:query_value> permite que a consulta inclua barras (/)
@app.route("/api/v2/query/<path:query_value>", methods=["GET"])
def proxy_leakcheck_query(query_value):
    """
    Função que atua como proxy para a API LeakCheck.
    Recebe a consulta do frontend, usa a chave da API configurada no backend e repassa para a API LeakCheck.
    Retorna a resposta da API LeakCheck para o frontend.
    """
    # Verifica se a chave da API foi configurada corretamente
    if not LEAKCHECK_API_KEY or LEAKCHECK_API_KEY == "SUA_CHAVE_LEAKCHECK_AQUI":
        print("Erro: Chave da API LeakCheck não configurada corretamente em app.py.")
        return jsonify({"success": False, "error": "LeakCheck API key not properly configured on the server. Please update app.py"}), 500

    # Obtém o tipo de consulta dos parâmetros da URL (ex: ?type=email)
    # Se não for especificado, usa 'auto' como padrão
    query_type = request.args.get("type", "auto")

    # Constrói a URL completa para a API original do LeakCheck
    leakcheck_url = f"{LEAKCHECK_BASE_URL}{query_value}"
    if query_type != "auto":
        leakcheck_url += f"?type={query_type}"

    # Define os cabeçalhos para a requisição à API LeakCheck
    # Inclui 'Accept' para JSON e a chave da API (agora do backend)
    headers = {
        "Accept": "application/json",
        "X-API-Key": LEAKCHECK_API_KEY
    }

    try:
        # Faz a requisição GET para a API original do LeakCheck
        response = requests.get(leakcheck_url, headers=headers)
        # Levanta um HTTPError para respostas de erro (4xx ou 5xx)
        response.raise_for_status()
        
        # Retorna a resposta JSON da API LeakCheck e o código de status
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as e:
        # Captura erros HTTP (ex: 400, 401, 403, 429) da API LeakCheck
        print(f"Erro HTTP da API LeakCheck: {e.response.status_code} - {e.response.text}")
        try:
            # Tenta retornar o erro JSON da API LeakCheck, se disponível
            return jsonify(e.response.json()), e.response.status_code
        except ValueError:
            # Se a resposta não for JSON, retorna o texto bruto do erro
            return jsonify({"success": False, "error": f"LeakCheck API error: {e.response.status_code} - {e.response.text}"}), e.response.status_code
    except requests.exceptions.ConnectionError:
        # Captura erros de conexão (ex: API offline, problema de rede)
        print("Erro de conexão: Não foi possível conectar à API LeakCheck.")
        return jsonify({"success": False, "error": "Failed to connect to LeakCheck API. Check network connection."}), 503
    except requests.exceptions.Timeout:
        # Captura erros de tempo limite da requisição
        print("Erro de tempo limite: A requisição à API LeakCheck excedeu o tempo limite.")
        return jsonify({"success": False, "error": "LeakCheck API request timed out."}), 504
    except requests.exceptions.RequestException as e:
        # Captura quaisquer outras exceções de requisição
        print(f"Ocorreu um erro inesperado ao fazer a requisição: {e}")
        return jsonify({"success": False, "error": f"An unexpected error occurred: {e}"}), 500

# Ponto de entrada para a aplicação Flask
if __name__ == "__main__":
    # Executa a aplicação em modo de depuração (debug=True) na porta 5000.
    # Em um ambiente de produção, debug deve ser False.
    app.run(debug=True, port=5000)
