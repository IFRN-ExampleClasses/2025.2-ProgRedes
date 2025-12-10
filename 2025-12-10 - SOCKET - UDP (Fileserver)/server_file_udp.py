# Importando as bibliotecas necessárias
import math
import os
import socket, os
import struct # Necessário para cabeçalhos binários

# Importando o arquivo de constantes e funções
import constantes, funcoes

# Limpando a tela do terminal
os.system('cls') if os.name == 'nt' else os.system('clear')

try:
   # Criando um socket (IPv4 / UDP)
   sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   # Ligando o socket do servidor à porta
   sockServer.bind(('', constantes.HOST_PORT))

   # Definindo um timeout para o socket.
   sockServer.settimeout(constantes.TIMEOUT_SOCKET)

   # Mensagem de início do servidor
   print('\n' + '-'*100)
   print('SERVIDOR UDP Inicializado - Recebendo Comandos...')
   print('Pressione CTRL+C para sair do servidor...\n')
   print(f'IP/Porta do Servidor.:{constantes.TUPLA_SERVER}')
   print('-'*100 + '\n')
   
   # Variável para armazenar fragmentos de um cliente específico
   # Estrutura: {('IP', PORTA): {'total': int, 'fragmentos': {num: payload}}}
   clientes_fragmentando = dict()
   
   # Loop principal do servidor
   while True:
      try:
         # Recebendo solicitações do cliente (fragmentos)
         byteFragmento, tuplaCliente = sockServer.recvfrom(constantes.BUFFER_SIZE)        
      except socket.timeout:
         continue
      else:
         # ----------------------------------------------------------------
         # LÓGICA DE MONTAGEM E EXTRAÇÃO DA MENSAGEM DO CLIENTE
         
         # 1. Extrai cabeçalho (8 bytes) e payload
         byteCabecalho = byteFragmento[:8]
         
         # Descompactando STRUCT do cabeçalho
         intTotalFragmentos, intNumFragmento = struct.unpack('<II', byteCabecalho)

         bytePayload = byteFragmento[8:]
         
         # 2. Inicializa ou atualiza o estado de fragmentação para este cliente
         if tuplaCliente not in clientes_fragmentando:
            clientes_fragmentando[tuplaCliente] = {'total': intTotalFragmentos, 'fragmentos': {}}
            
         clientes_fragmentando[tuplaCliente]['fragmentos'][intNumFragmento] = bytePayload
         
         # 3. Verifica se todos os fragmentos chegaram
         if len(clientes_fragmentando[tuplaCliente]['fragmentos']) == intTotalFragmentos:
            
            # Montagem final da mensagem
            listPayloads = [clientes_fragmentando[tuplaCliente]['fragmentos'][i] 
                            for i in sorted(clientes_fragmentando[tuplaCliente]['fragmentos'])]
            byteMensagemCompleta = b''.join(listPayloads)
            
            # Decodifica, limpa e normaliza a mensagem (lowercase/strip)
            strMensagemCliente = byteMensagemCompleta.decode(constantes.CODE_PAGE).lower().strip()
            
            # Limpa o estado do cliente após a montagem
            del clientes_fragmentando[tuplaCliente] 
         else:
            # Continua esperando por mais fragmentos
            continue 
         
         # ----------------------------------------------------------------
         
         # Obtendo o nome do Host cliente (com tratamento de erro)
         strNomeHostCliente = funcoes.obterNomeHost(tuplaCliente[0])

         # Inicializando variáveis de resposta
         boolRetornoCliente      = True # Controla se o servidor deve responder ao cliente
         strMensagemResposta     = ''   # Resposta de texto (erro, ajuda, FILE_START)
         strCaminhoArquivoEnviar = None # Caminho do arquivo a ser enviado (se houver)

         # Exibindo quando um novo cliente se conecta
         if strMensagemCliente.startswith(chr(175).lower()): 
           strMensagemLog = f'Cliente {tuplaCliente[0]} ({strNomeHostCliente}) se conectou agora...'
           print(f'NOVA CONEXÃO.....: {strMensagemLog}')
           boolRetornoCliente = False             
         # Exibindo quando um cliente se desconecta
         elif strMensagemCliente == 'sair':      
           strMensagemLog = f'Cliente {tuplaCliente[0]} ({strNomeHostCliente}) se desconectou...'
           print(f'FIM DA CONEXÃO...: {strMensagemLog}')             
           boolRetornoCliente = False             
         elif strMensagemCliente.startswith('\\d:'):
            strNomeArquivo = strMensagemCliente[3:].strip()
            strCaminhoCompletoArquivo = os.path.join(constantes.DIR_IMG_SERVER, strNomeArquivo)
            strMensagemLog = f'Cliente {tuplaCliente[0]} ({strNomeHostCliente}) solicitou o download de "{strNomeArquivo}"'            
            # Arquivo não encontrado - Mensagem de erro
            if not os.path.exists(strCaminhoCompletoArquivo) or not os.path.isfile(strCaminhoCompletoArquivo):
               strMensagemResposta = f'ERRO: Arquivo "{strNomeArquivo}" nao encontrado ou inacessivel no servidor.'
            else:
               intTamanhoArquivo           = os.path.getsize(strCaminhoCompletoArquivo)
               intTotalFragmentosEsperados = funcoes.calcularTotalFragmentosArquivo(intTamanhoArquivo)              
               # Mensagem de controle (texto) com o nome e o total de fragmentos
               strMensagemResposta = f'FILE_START:{strNomeArquivo}:{intTotalFragmentosEsperados}' 
               strCaminhoArquivoEnviar = strCaminhoCompletoArquivo # Armazena o caminho para leitura posterior         
         elif strMensagemCliente == '\\?':
           strMensagemLog             = f'Cliente {tuplaCliente[0]} ({strNomeHostCliente}) enviou \\?...'
           strMensagemResposta        = funcoes.ajudaServidor()
         elif strMensagemCliente == '\\f':
           strMensagemLog             = f'Cliente {tuplaCliente[0]} ({strNomeHostCliente}) enviou \\f...'
           strMensagemResposta        = funcoes.listarArquivos()
         # ----------------------------------------------------------------
         # FALLBACK: Comando Inválido (Checa se não foi pego acima)
         elif strMensagemCliente not in [c.lower() for c in constantes.COMANDOS_SERVER]: 
           strMensagemLog             = f'Cliente {tuplaCliente[0]} ({strNomeHostCliente}) enviou -> {strMensagemCliente[:30]}...'
           strMensagemResposta        = funcoes.erroComando() 

         # Enviando a resposta do comando ao cliente (Fragmentação via Gerador)
         if boolRetornoCliente:
            # Exibindo a mensagem recebida no servidor -> LOG
            print(f'COMANDO RECEBIDO.: {strMensagemLog}')
           
            # 1. Enviando a mensagem de controle/texto (sempre presente)
            byteDadosResposta = strMensagemResposta.encode(constantes.CODE_PAGE)
            
            print(f'STATUS: Enviando controle/resposta de {len(byteDadosResposta)} bytes.')
            for byteFragmento in funcoes.fragmentarDados(byteDadosResposta):
               sockServer.sendto(byteFragmento, tuplaCliente)
            
            # 2. Eviando o arquivo em CHUNKS (se houver / sem estourar memória)
            if strCaminhoArquivoEnviar:
               print(f'STATUS: Iniciando envio do arquivo ({intTamanhoArquivo} bytes) em chunks...')
               try:
                  with open(strCaminhoArquivoEnviar, 'rb') as f:                      
                     while True:
                        # Lendo um CHUNCK
                        byteChunk = f.read(constantes.CHUNK_SIZE)
                        if not byteChunk:break 
                        
                        # Fragmenta o chunk lido e envia todos os fragmentos do chunk
                        # NOTA: O gerador funcoes.fragmentarDados calculará o total do CHUNK,
                        # mas o cliente só precisa saber o total do ARQUIVO para o progresso.
                        # No nosso protocolo atual, o cliente usará o total dos fragmentos
                        # para remontar cada chunk, o que funciona.
                          
                        for byteFragmento in funcoes.fragmentarDados(byteChunk):
                           sockServer.sendto(byteFragmento, tuplaCliente)
                             
                        print(f'STATUS: Transferencia binaria de {intTamanhoArquivo} bytes finalizada.')
               except Exception as e:
                  print(f'ERRO CRÍTICO AO LER E ENVIAR ARQUIVO: {e}')
                  # Neste ponto, o cliente pode ter recebido dados parciais.
                  # Um sistema robusto enviaria um comando de ABORT.

except KeyboardInterrupt:
   print('\nAVISO.........: Foi Pressionado CTRL+C...\nSaindo do Servidor...\n\n')
except socket.error as strErro:
   print(f'\nERRO DE SOCKET: {strErro}\n\n')
except Exception as strErro:
   print(f'\nERRO GENÉRICO..: {strErro}\n\n')
finally:
   # Fechando o Socket
   sockServer.close()
   print('Servidor finalizado com Sucesso...\n\n')