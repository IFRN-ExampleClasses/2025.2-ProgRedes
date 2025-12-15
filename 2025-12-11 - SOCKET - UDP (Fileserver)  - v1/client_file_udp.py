# Importando as bibliotecas necessárias
import socket, os

# Importando o arquivo de constantes
import constantes

# Limpando a tela do terminal
os.system('cls') if os.name == 'nt' else os.system('clear')

try:
   # Criando o socket
   sockClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   
   # Definindo o timeout para o socket do cliente
   sockClient.settimeout(constantes.TIMEOUT_SOCKET)

   # Enviando uma 'sinalização' de que um cliente se conectou ao servidor (FRAGMENTADO)
   strMensagemEntrada = f'{chr(175)} {constantes.HOST_IP_CLIENT}'
   byteMensagemEntrada = strMensagemEntrada.encode(constantes.CODE_PAGE)

   # Mensagem inicial do cliente
   print('\n' + '-'*100)
   print('CLIENTE UDP Inicializado - Enviando Comandos...')
   print('Digite SAIR para sair do cliente...\n')
   print(f'IP/Porta do Cliente.:{constantes.TUPLA_CLIENTE}')
   print('-'*100 + '\n')

   # Loop principal do cliente
   while True:
      strNomeArquivo = input('Digite o arquivo para receber: ').lower().strip()

      # Se teclar ENTER sem digitar nada, ignora
      if not strNomeArquivo: continue

      if strNomeArquivo == 'sair': break

      # Dizendo ao servidor que deseja receber um arquivo
      byteMensagem = strNomeArquivo.encode(constantes.CODE_PAGE)

      # Enviando a mensagem ao servidor
      sockClient.sendto(byteMensagem, constantes.TUPLA_SERVER)

      # Preparando para receber o arquivo
      objArquivoRecebimento = open(f'{constantes.DIR_IMG_CLIENT}\\{strNomeArquivo}', 'wb')
      print(f'\nRecebendo o arquivo "{strNomeArquivo}" do Servidor...')

      while True:
         # Recebendo os dados do servidor
         byteDados, tuplaServidor = sockClient.recvfrom(constantes.BUFFER_SIZE)
    
         # Se a mensagem recebida for 'EOF', significa que o arquivo terminou
         if byteDados == b'EOF':
            print(f'Arquivo "{strNomeArquivo}" recebido com sucesso!\n')
            objArquivoRecebimento.close()
            break
    
         # Escrevendo os dados recebidos no arquivo
         objArquivoRecebimento.write(byteDados)

      # Fechando o arquivo após o recebimento
      objArquivoRecebimento.close()
except KeyboardInterrupt:
   print('\nAVISO.........: Foi Pressionado CTRL+C...\nSaindo do Cliente...\n\n')
except socket.error as strErro:
   print(f'\nERRO DE SOCKET: {strErro}\n\n')
except Exception as strErro:
   print(f'\nERRO GENÉRICO..: {strErro}\n\n')
finally:
   sockClient.close()
   print('Cliente finalizado com Sucesso...\n\n')


















#-------------------------------


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    strNomeArq = input('Nome do arquivo a fazer download: ')
    sock.sendto(strNomeArq.encode('utf-8'), (SERVER, PORT))

    data, addr = sock.recvfrom(4096)

    fd = open (strNomeArq, 'wb')
    fd.write (data)
    fd.close()

sock.close()