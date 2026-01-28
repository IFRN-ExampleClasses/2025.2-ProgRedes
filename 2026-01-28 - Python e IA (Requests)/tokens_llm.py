"""
    Módulo de Configuração de LLMs.
    
    Este arquivo armazena as credenciais (tokens), endpoints de API e estruturas 
    de dados (headers e payloads) necessárias para conectar com diferentes 
    provedores de Inteligência Artificial.

    Links úteis para obter as chaves de API:
    GEMINI:   https://aistudio.google.com/
    DEEPSEEK: https://api-docs.deepseek.com/
    OPENAI:   https://openai.com/pt-BR/api/
"""

# ----------------------------------------------------------------------
# Tokens de acesso para os LLMs
# NOTA DE SEGURANÇA: Em produção, nunca deixe chaves hardcoded (escritas diretamente no código).
# O ideal é usar variáveis de ambiente (os.getenv) ou arquivos .env.
GEMINI_TOKEN   = "INFORME TOKEN GEMINI AQUI"
DEEPSEEK_TOKEN = "INFORME TOKEN DEEPSEEK AQUI"
OPENAI_TOKEN   = "INFORME TOKEN OPENAI AQUI"

# ----------------------------------------------------------------------
# Configurações dos serviços LLM
# Este dicionário mapeia um "nome amigável" (ex: 'gemini') para suas configurações técnicas.

DICT_SERVICES = { 
    "gemini"   : { 
        "model" : "gemini-2.0-flash",  # Modelo específico (verifique a disponibilidade da versão 2.5 ou 1.5)
        "host": "generativelanguage.googleapis.com",
        
        # IMPORTANTE: Este endpoint é crucial. O Google oferece uma API compatível com OpenAI.
        # Ao usar '/v1beta/openai/...', o Gemini aceita o mesmo formato de JSON da OpenAI,
        # permitindo usar o mesmo código para ambos os serviços.
        "endpoint" : "/v1beta/openai/chat/completions",
        "token": GEMINI_TOKEN  
    },

    "deepseek" : { 
        "model" : "deepseek-chat",  # O modelo padrão de chat (V3). Use "deepseek-reasoner" para R1 (raciocínio).
        "host" : "api.deepseek.com", 
        "endpoint" : "/v1/chat/completions", # Padrão da indústria (OpenAI compatible)
        "token": DEEPSEEK_TOKEN  
    },

    "openai"   : { 
        "model" : "gpt-3.5-turbo",   # Modelo custo-benefício. Para maior inteligência, use "gpt-4o".
        "host" : "api.openai.com",
        "endpoint" : "/v1/chat/completions",
        "token": OPENAI_TOKEN  
    }
}

# ----------------------------------------------------------------------
# Headers (Cabeçalhos HTTP)
# Define como os dados são enviados e quem está enviando.
# A chave "Authorization" começa vazia e é preenchida dinamicamente no script principal
# antes de cada requisição (Bearer Token).
DICT_HEADERS = {
    "Authorization": "", 
    "Content-Type": "application/json" # Informa ao servidor que o corpo da mensagem é um JSON
}

# ----------------------------------------------------------------------
# Payload (Corpo da Requisição)
# Estrutura base do JSON que será enviado via POST.
# O script principal irá modificar os campos "model" e "messages" em tempo de execução.
DICT_PAYLOAD =  {
    "model" : "",  # Será preenchido com o modelo selecionado em DICT_SERVICES
    "messages" : [ 
         # Role 'system': Define a persona ou regras de comportamento da IA.
         {  "role": "system", "content": "Você é um assistente."},
         
         # Role 'user': Onde entrará o prompt digitado pelo usuário.
         {"role": "user", "content": ""} 
    ],
    
    # Parâmetros de controle de geração:
    "temperature": 0.7, # 0.0 = Mais focado/determinístico; 1.0 = Mais criativo/aleatório.
    "max_tokens" : 10000 # Limite máximo de tokens na resposta (entrada + saída ou apenas saída, depende da API).
}