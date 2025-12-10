import socket, os, math, struct

import constantes

# ------------------------------------------------------------------------------------------
# Função que retorna o nome do Host (AGORA COM TRATAMENTO DE ERRO)
def obterNomeHost(strIPHost:str) -> str:
   try:
      # Tenta obter o nome do host
      strNomeCompleto = socket.gethostbyaddr(strIPHost)[0]
      # Retorna apenas a primeira parte do nome em maiúsculas
      return strNomeCompleto.split('.')[0].upper()
   except socket.error:
      # Se falhar (host not found), retorna um nome baseado no IP
      return f'IP_{strIPHost.replace(".", "_")}'
   except Exception:
      # Tratamento genérico
      return f'IP_{strIPHost}'

# ------------------------------------------------------------------------------------------
# Função que exibe mensagem de erro para o cliente
def erroComando() -> str:
   strMensagemErro  = '\nCOMANDO INVÁLIDO...\n'
   strMensagemErro += '\\? para ajuda...\n' 
   return strMensagemErro

# ------------------------------------------------------------------------------------------
# Função que exibe texto de ajuda para o cliente
def ajudaServidor() -> str:
   strTextoAjuda  = '\nAJUDA DO SERVIDOR:\n'
   strTextoAjuda += '\\? -> Ajuda\n'
   strTextoAjuda += '\\f -> Lista os arquivos do servidor\n'
   strTextoAjuda += '\\d:<NOME_ARQUIVO> -> Download do arquivo\n'
   strTextoAjuda += 'sair -> Encerra o cliente\n\n'
   return strTextoAjuda

# ------------------------------------------------------------------------------------------
# Função que retorna a lista de arquivos para o cliente
def listarArquivos() -> str:
   strListaArquivos  = '\nARQUIVOS NO SERVIDOR:\n'
   strListaArquivos += '-'*80 + '\n'
   for strNomeArquivo in os.listdir(constantes.DIR_IMG_SERVER):
      # Uso de os.path.join para garantir portabilidade
      strNomeCompletoArquivo = os.path.join(constantes.DIR_IMG_SERVER, strNomeArquivo)
      if os.path.isfile(strNomeCompletoArquivo):
         strListaArquivos += f'{strNomeArquivo:<50} -> {os.path.getsize(strNomeCompletoArquivo)} bytes\n'
         strListaArquivos += '-'*80 + '\n'
   return strListaArquivos

# ------------------------------------------------------------------------------------------
# Função Geradora universal que fragmenta dados binários (bytes) para envio UDP
def fragmentarDados(byteDados: bytes):
   '''Divide dados binários em fragmentos com cabeçalho de controle binário para envio UDP.'''
   
   byteMensagem = byteDados 
   
   # Calcula o número total de fragmentos
   intTotalFragmentos = math.ceil(len(byteMensagem) / constantes.PAYLOAD_SIZE)
   
   # Itera sobre os fragmentos
   for i in range(intTotalFragmentos):
      # Calculando os índices de início e fim
      intInicio = i * constantes.PAYLOAD_SIZE
      intFim    = min((i + 1) * constantes.PAYLOAD_SIZE, len(byteMensagem))
      
      # Extraindo o payload (carga útil) do fragmento
      bytePayload = byteMensagem[intInicio:intFim]
      
      # Implementando o STRUCT
      # Formato '<II': Little-endian ('<'), 
      # seguido de dois inteiros sem sinal (I) de 4 bytes cada. Total: 8 bytes.
      byteCabecalho = struct.pack('<II', int(intTotalFragmentos), int(i + 1))
      
      # Concatenando cabeçalho (8 bytes) e payload
      yield byteCabecalho + bytePayload

# ------------------------------------------------------------------------------------------
# Função auxiliar para calcular o total de fragmentos para um arquivo inteiro
def calcularTotalFragmentosArquivo(tamanho_arquivo: int) -> int:
   '''Calcula o número total de fragmentos que um arquivo geraria.'''
   
   if tamanho_arquivo == 0: return 0
   
   return math.ceil(tamanho_arquivo / constantes.PAYLOAD_SIZE)

# ------------------------------------------------------------------------------------------