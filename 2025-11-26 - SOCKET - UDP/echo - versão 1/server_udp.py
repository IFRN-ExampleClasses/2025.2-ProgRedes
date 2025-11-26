import socket

# ----------------------------------------------------------------------
HOST_IP_SERVER  = ''              # Definindo o IP do servidor
HOST_PORT       = 50000           # Definindo a porta

BUFFER_SIZE     = 10              # Tamanho do buffer
CODE_PAGE       = 'utf-8'         # Definindo a página de 
                                  # codificação de caracteres
# ----------------------------------------------------------------------

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta
sockServer.bind( (HOST_IP_SERVER, HOST_PORT) ) 

# Definindo um timeout (tempo de vida) para o socket
sockServer.settimeout(0.5)

print('\nRecebendo Mensagens...')
print('Pressione CTRL+C para sair do servidor...\n')
print('-'*100 + '\n')

try:
   while True:
      try:
         # Recebendo os dados do cliente
         byteMensagem, tuplaCliente = sockServer.recvfrom(BUFFER_SIZE)
         intTamanhoMensagem = int(byteMensagem.decode(CODE_PAGE))
         if intTamanhoMensagem > BUFFER_SIZE: BUFFER_SIZE = intTamanhoMensagem
         byteMensagem, tuplaCliente = sockServer.recvfrom(BUFFER_SIZE)
      except socket.timeout:
         continue
      else:
         # Obtendo o nome (HOST) do cliente
         strNomeHost = socket.gethostbyaddr(tuplaCliente[0])[0].split('.')[0].upper()

         # Imprimindo a mensagem recebida convertendo de bytes para string
         strMensagem = byteMensagem.decode(CODE_PAGE)
         print(f'{tuplaCliente} -> {strNomeHost}: {strMensagem}')

         # Devolvendo uma mensagem ao cliente
         sockServer.sendto(strMensagem[::-1].encode(CODE_PAGE), tuplaCliente)

except KeyboardInterrupt:
   print('\nAVISO: Foi Pressionado CTRL+C...\nSaindo do Servidor...\n\n')
finally:
   # Fechando o socket
   sockServer.close()
   print('Servidor finalizado com sucesso...\n\n')