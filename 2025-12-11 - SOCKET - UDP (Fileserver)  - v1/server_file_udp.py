# Importando as bibliotecas necessárias
import socket, os

# Importando o arquivo de constantes
import constantes

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
   
   while True:
      try:
         # Recebendo solicitações do cliente
         byteMensagem, tuplaCliente = sockServer.recvfrom(constantes.BUFFER_SIZE)
         strMensagemCliente = byteMensagem.decode(constantes.CODE_PAGE).lower().strip()       
      except socket.timeout:
         continue
      else:
         # Exibindo quando um novo cliente se conecta
         if strMensagemCliente.startswith(chr(175)): 
            print(f'NOVA CONEXÃO.....: Cliente {tuplaCliente[0]} se conectou...')
            continue

         # Exibindo quando um cliente se desconecta
         if strMensagemCliente == 'sair':      
            print(f'FIM DA CONEXÃO...: Cliente {tuplaCliente[0]} se desconectou...')             
            continue

         # Abrindo o arquivo para a enviar ao cliente
         strNomeArquivo = strMensagemCliente
         print(f'{tuplaCliente} solicitou o arquivo: {strNomeArquivo}... ', end=' ')
         try:
            arqEnvio = open(f'{constantes.DIR_IMG_SERVER}\\{strNomeArquivo}', 'rb')
         except FileNotFoundError:
            print('ERRO: Arquivo não encontrado')
            strMensagemErro = 'ERRO: Arquivo não encontrado.'.encode(constantes.CODE_PAGE)
            sockServer.sendto(b'ERRO', tuplaCliente)
            sockServer.sendto(strMensagemErro, tuplaCliente)
            continue
         except Exception as strErro:
            print(f'ERRO: {strErro}')
            strMensagemErro = f'ERRO: {strErro}'.encode(constantes.CODE_PAGE)
            sockServer.sendto(b'ERRO', tuplaCliente)
            sockServer.sendto(strMensagemErro, tuplaCliente)
            continue
         else:
            # Obtendo o tamanho do arquivo
            intTamanhoArquivo = os.path.getsize(f'{constantes.DIR_IMG_SERVER}\\{strNomeArquivo}')
            intBytesEnviados  = 0
            # Lendo o conteúdo do arquivo para enviar ao cliente
            print(f'Enviando arquivo..')
            while intBytesEnviados < intTamanhoArquivo:
               fileData = arqEnvio.read(constantes.BUFFER_SIZE)
               sockServer.sendto(fileData, tuplaCliente)
               intBytesEnviados += len(fileData)

         # Enviando a mensagem de EOF (End Of File) para o cliente        
         print(f'Arquivo {strNomeArquivo} enviado com sucesso para {tuplaCliente}!')
         sockServer.sendto(b'EOF', tuplaCliente)
         
         # Fechando o arquivo
         arqEnvio.close()

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