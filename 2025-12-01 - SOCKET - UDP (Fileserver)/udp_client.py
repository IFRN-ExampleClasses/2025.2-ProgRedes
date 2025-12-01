# Importando a biblioteca SOCKET
import socket

import constantes

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('\n\nPara sair digite SAIR...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite a mensagem: ')

   # Saindo do Cliente quando digitar SAIR
   if strMensagem.lower().strip() == 'sair': break

   # Enviando a mensagem ao servidor      
   sockClient.sendto(strMensagem.encode(constantes.CODE_PAGE), constantes.TUPLA_SERVER)

   # Recebendo resposta do servidor
   bytesMensagemRetorno, tuplaCliente = sockClient.recvfrom(constantes.BUFFER_SIZE)
   intTamanhoMensagem = int(bytesMensagemRetorno.decode(constantes.CODE_PAGE))
   if intTamanhoMensagem > constantes.BUFFER_SIZE: constantes.BUFFER_SIZE = intTamanhoMensagem

   bytesMensagemRetorno, tuplaOrigem = sockClient.recvfrom(constantes.BUFFER_SIZE)
   strNomeHost = socket.gethostbyaddr(tuplaOrigem[0])[0].split('.')[0].upper()
   print(f'{tuplaOrigem} -> {strNomeHost}: {bytesMensagemRetorno.decode(constantes.CODE_PAGE)}')

# Fechando o socket
sockClient.close()
