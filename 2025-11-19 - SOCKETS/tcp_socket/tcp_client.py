# Importando a biblioteca SOCKET
import socket


# ----------------------------------------------------------------------
HOST_IP_SERVER = 'COLOQUE_IP_DO_SERVIDOR' # Definindo o IP do servidor
HOST_PORT      = 50000                    # Definindo a porta
CODE_PAGE      = 'utf-8'                  # Definindo a página de 
                                          # codificação de caracteres
# ----------------------------------------------------------------------

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_STREAM -> TCP)
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando ao servidor
sockTCP.connect((HOST_IP_SERVER, HOST_PORT))

print('\n\nPara sair digite EXIT...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite a mensagem: ')

   # Saindo do Cliente quando digitar SAIR
   if strMensagem.lower().strip() == 'sair': break

   # Convertendo a mensagem em bytes
   bytesMensagem = strMensagem.encode(CODE_PAGE) 

   # Enviando a mensagem ao servidor      
   sockTCP.send(bytesMensagem)

# Fechando o socket
sockTCP.close()
