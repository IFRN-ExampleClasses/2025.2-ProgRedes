import os, socket

# --------------------------------------------------------------------------------
# Definindo o IP do servidor para os clientes
HOST_IP_SERVER = socket.gethostbyname(socket.gethostname())    

# Definindo a porta
HOST_PORT      = 50000           

# Definindo a tupla do servidor
TUPLA_SERVER   = (HOST_IP_SERVER, HOST_PORT)

# Definindo a página de codificação de caracteres
CODE_PAGE      = 'utf-8'    

# Definindo o tamanho do buffer
BUFFER_SIZE    = 512

# Definindo os diretórios de arquivos de imagens no servidor
DIR_IMG_SERVER = os.path.dirname(__file__) + '\\server_files\\'
# --------------------------------------------------------------------------------