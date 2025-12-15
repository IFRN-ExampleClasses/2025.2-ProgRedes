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
         # Recebendo solicitações do cliente (fragmentos)
         byteFragmento, tuplaCliente = sockServer.recvfrom(constantes.BUFFER_SIZE)        
      except socket.timeout:
         continue
      else: 
        # Abrindo o arquivo para a enviar ao cliente
        strNomeArquivo = byteFragmento.decode(constantes.CODE_PAGE)
        print (f'Recebi pedido para o arquivo: {strNomeArquivo}')
        try:
           arqEnvio = open (f'{constantes.DIR_IMG_SERVER}\\{strNomeArquivo}', 'rb')
        except FileNotFoundError:
           print (f'Arquivo não encontrado: {strNomeArquivo}\n')
           strMensagemErro = 'ERRO: Arquivo não encontrado.'.encode(constantes.CODE_PAGE)
           sockServer.sendto(strMensagemErro, tuplaCliente)
           continue
        except Exception as strErro:
           print (f'Erro ao abrir o arquivo: {strErro}\n')
           strMensagemErro = f'ERRO: {strErro}'.encode(constantes.CODE_PAGE)
           sockServer.sendto(strMensagemErro, tuplaCliente)
           continue
        else:
           # Lendo o conteúdo do arquivo para enviar ao cliente
           print (f'Enviando arquivo: {strNomeArquivo}')
           sockServer.sendto(b'OK', tuplaCliente)
           fileData = arqEnvio.read(4096)
           sockServer.sendto(fileData, tuplaCliente)

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