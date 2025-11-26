# Importando a biblioteca SOCKET
import socket

# ----------------------------------------------------------------------
HOST_IP_SERVER = '10.25.1.9' # Definindo o IP do servidor
HOST_PORT      = 50000       # Definindo a porta
TUPLA_SERVER   = (HOST_IP_SERVER, HOST_PORT)


BUFFER_SIZE    = 10          # Tamanho do buffer
CODE_PAGE      = 'utf-8'     # Definindo a página de 
                             # codificação de caracteres
# ----------------------------------------------------------------------

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('\n\nPara sair digite SAIR...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite a mensagem: ')

   # Saindo do Cliente quando digitar SAIR
   if strMensagem.lower().strip() == 'sair': break

   # Enviando o tamanho da mensagem ao servidor
   bytesTamanhoMensagem = str(len(strMensagem)).encode(CODE_PAGE)
   sockClient.sendto(bytesTamanhoMensagem, TUPLA_SERVER)
   
   # Enviando a mensagem ao servidor      
   sockClient.sendto(strMensagem.encode(CODE_PAGE), TUPLA_SERVER)

   # Recebendo resposta do servidor
   bytesMensagemRetorno, tuplaCliente = sockClient.recvfrom(BUFFER_SIZE)
   intTamanhoMensagem = int(bytesMensagemRetorno.decode(CODE_PAGE))
   if intTamanhoMensagem > BUFFER_SIZE: BUFFER_SIZE = intTamanhoMensagem

   bytesMensagemRetorno, tuplaOrigem = sockClient.recvfrom(BUFFER_SIZE)
   strNomeHost = socket.gethostbyaddr(tuplaOrigem[0])[0].split('.')[0].upper()
   print(f'{tuplaOrigem} -> {strNomeHost}: {bytesMensagemRetorno.decode(CODE_PAGE)}')

# Fechando o socket
sockClient.close()
