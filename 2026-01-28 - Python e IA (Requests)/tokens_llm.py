'''
   Obter os tokens e configurações para os LLMs utilizados

   GEMINI:
      https://aistudio.google.com/

   DEEPSEEK:
      https://api-docs.deepseek.com/

   OPENAI:
      https://openai.com/pt-BR/api/
'''

# ----------------------------------------------------------------------
# Tokens de acesso para os LLMs
GEMINI_TOKEN   = "INFORME TOKEN GEMINI AQUI"
DEEPSEEK_TOKEN = "INFORME TOKEN DEEPSEEK AQUI"
OPENAI_TOKEN   = "INFORME TOKEN OPENAI AQUI"

# ----------------------------------------------------------------------
# Configurações dos serviços LLM
# Para mais detalhes, veja a documentação de cada LLM

# Dicionário com as configurações dos serviços LLM
# Cada serviço inclui o modelo, host, endpoint e token de acesso
DICT_SERVICES = { 
   "gemini"   : { "model" : "gemini-2.5-flash",  # ou gemini-1.5-pro, etc.
                  "host": "generativelanguage.googleapis.com",
                  "endpoint" : "/v1beta/openai/chat/completions",
                  "token": GEMINI_TOKEN  },

   "deepseek" : { "model" : "deepseek-chat",  # ou "deepseek-coder" se preferir 
                  "host" : "api.deepseek.com", 
                  "endpoint" : "/v1/chat/completions",
                  "token": DEEPSEEK_TOKEN  },

   "openai"   : { "model" : "gpt-3.5-turbo",   # Ou "gpt-4", "gpt-4o", etc.
                  "host" : "api.openai.com",
                  "endpoint" : "/v1/chat/completions",
                  "token": OPENAI_TOKEN  }
}

# Headers padrão para as requisições -> Podem variar conforme a LLM
# São utilizadas para autenticação e definição do tipo de conteúdo
DICT_HEADERS = {
   "Authorization": "",
   "Content-Type": "application/json"
}

# Payload padrão para as requisições -> Podem variar conforme a LLM
# Payloads são os dados enviados na requisição
# Incluem o modelo, mensagens, temperatura, etc.
DICT_PAYLOAD =  {
   "model" : "", 
   "messages"   : [ 
         {  "role": "system", "content": "Você é um assistente."},
         {"role": "user", "content": ""} ],
         "temperature": 0.7,
         "max_tokens" : 10000
}