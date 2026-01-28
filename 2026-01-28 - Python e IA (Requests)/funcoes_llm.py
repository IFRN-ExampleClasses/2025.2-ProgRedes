import requests
import tokens_llm

# ----------------------------------------------------------------------
def obterResultados (data: dict) -> str:
   try: 
      strResposta = data["choices"][0]["message"]["content"].strip()
   except Exception as e:
      print ("Erro na resposta do modelo ", e)
      strResposta = ""
   else:
      return strResposta
         

# ----------------------------------------------------------------------
def solicitarServico (servico: str, prompt: str) -> str:
   try:
      tokens_llm.DICT_HEADERS["Authorization"]          = f'Bearer {tokens_llm.DICT_SERVICES[servico]["token"]}'
      tokens_llm.DICT_PAYLOAD["model"]                  = tokens_llm.DICT_SERVICES[servico]["model"]
      tokens_llm.DICT_PAYLOAD["messages"][1]["content"] = prompt

      reqEnvio = requests.post("https://"+ 
                               tokens_llm.DICT_SERVICES[servico]["host"]+
                               tokens_llm.DICT_SERVICES[servico]["endpoint"], 
                               headers=tokens_llm.DICT_HEADERS, 
                               json=tokens_llm.DICT_PAYLOAD)
      
      reqEnvio.raise_for_status()
      data = reqEnvio.json()
      return obterResultados(data)
   except Exception as e:
      return f"\nERRO: {e}..."


# ----------------------------------------------------------------------
def selecionarServico() -> str:
   for id, strServico in enumerate(tokens_llm.DICT_SERVICES):
      print (f"{id+1} - {strServico}")

   try:
      intServico = int(input("Informe o nº do serviço LLM: "))
      strServico = tuple(tokens_llm.DICT_SERVICES.items())[intServico-1][0]
   except ValueError:
      strServico = "gemini"
      print (f"ERRO: LLM inválida. Usando a LLM default: {strServico}")

   return strServico
# ----------------------------------------------------------------------

