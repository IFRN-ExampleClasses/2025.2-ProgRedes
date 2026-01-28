import requests
import tokens_llm  # Módulo externo (fictício/local) que contém configurações, tokens e dicionários de estrutura

# ----------------------------------------------------------------------
def obterResultados(data: dict) -> str:
    """
    Processa o JSON retornado pela API da LLM para extrair apenas o texto da resposta.
    
    Args:
        data (dict): O dicionário JSON completo retornado pela API.
        
    Returns:
        str: O texto da resposta gerada ou None em caso de erro (implícito).
    """
    try: 
        # Tenta acessar a estrutura padrão de resposta (comum em APIs estilo OpenAI).
        # Caminho: choices -> item 0 -> message -> content
        strResposta = data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # Captura erros caso a estrutura do JSON seja diferente do esperado (ex: erro de API)
        print("Erro na resposta do modelo ", e)
        strResposta = ""
        # Nota: Se cair aqui, a função retorna None (comportamento padrão do Python sem return explícito)
    else:
        # O bloco 'else' no try/except é executado apenas se NÃO houver exceção.
        return strResposta
          

# ----------------------------------------------------------------------
def solicitarServico(servico: str, prompt: str) -> str:
    """
    Prepara e envia a requisição HTTP POST para a API da LLM selecionada.
    
    Args:
        servico (str): A chave/nome do serviço (ex: 'gpt-4', 'gemini') para buscar configs.
        prompt (str): O texto de entrada do usuário.
        
    Returns:
        str: A resposta da LLM processada ou uma mensagem de erro formatada.
    """
    try:
        # 1. Configuração Dinâmica dos Headers e Payload
        # Atualiza o token de autenticação no dicionário de headers global importado
        tokens_llm.DICT_HEADERS["Authorization"] = f'Bearer {tokens_llm.DICT_SERVICES[servico]["token"]}'
        
        # Define qual modelo (engine) será usado no payload
        tokens_llm.DICT_PAYLOAD["model"] = tokens_llm.DICT_SERVICES[servico]["model"]
        
        # Injeta o prompt do usuário na estrutura de mensagens. 
        # O índice [1] sugere que o índice [0] já está ocupado (provavelmente um 'system prompt').
        tokens_llm.DICT_PAYLOAD["messages"][1]["content"] = prompt

        # 2. Construção da URL e Envio da Requisição
        # Concatena protocolo, host e endpoint para formar a URL completa
        url_completa = "https://" + \
                       tokens_llm.DICT_SERVICES[servico]["host"] + \
                       tokens_llm.DICT_SERVICES[servico]["endpoint"]

        reqEnvio = requests.post(
            url_completa, 
            headers=tokens_llm.DICT_HEADERS, 
            json=tokens_llm.DICT_PAYLOAD
        )
      
        # 3. Verificação e Processamento
        # Levanta uma exceção (HTTPError) se o status code for 4xx ou 5xx
        reqEnvio.raise_for_status()
        
        # Converte a resposta bruta para dicionário Python
        data = reqEnvio.json()
        
        # Chama a função auxiliar para extrair o texto limpo
        return obterResultados(data)
        
    except Exception as e:
        # Retorna uma string formatada em caso de falha de conexão ou parsing
        return f"\nERRO: {e}..."


# ----------------------------------------------------------------------
def selecionarServico() -> str:
    """
    Exibe um menu no console para o usuário escolher qual LLM utilizar.
    
    Returns:
        str: A chave (key) do serviço selecionado no dicionário de configurações.
    """
    # Itera sobre as chaves do dicionário de serviços para criar o menu
    for id, strServico in enumerate(tokens_llm.DICT_SERVICES):
        print(f"{id+1} - {strServico}")

    try:
        # Captura a escolha do usuário
        intServico = int(input("Informe o nº do serviço LLM: "))
        
        # Converte o dicionário em uma lista de tuplas para acessar pelo índice numérico.
        # [intServico-1] pega a tupla correta, [0] pega a chave (nome do serviço).
        strServico = tuple(tokens_llm.DICT_SERVICES.items())[intServico-1][0]
        
    except ValueError:
        # Tratamento se o usuário digitar algo que não seja número
        strServico = "gemini"
        print(f"ERRO: LLM inválida. Usando a LLM default: {strServico}")
        # Nota: Este bloco não captura IndexError (se o usuário digitar um número fora da lista)

    return strServico
# ----------------------------------------------------------------------