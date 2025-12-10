# Importando as bibliotecas necessárias
import os, socket

# --------------------------------------------------------------------------------
# Definindo o IP do servidor para os clientes
HOST_IP_SERVER  = socket.gethostbyname(socket.gethostname())

# Obtendo o IP do cliente
HOST_IP_CLIENT  = socket.gethostbyname(socket.gethostname())

# Definindo a porta
HOST_PORT       = 50000           

# Definindo a tupla do servidor
TUPLA_SERVER    = (HOST_IP_SERVER, HOST_PORT)
TUPLA_CLIENTE   = (HOST_IP_CLIENT, HOST_PORT)

# Definindo a página de codificação de caracteres
CODE_PAGE       = 'utf-8'    

# Definindo o tamanho do buffer
BUFFER_SIZE     = 512

# Definindo o tamanho máximo da carga útil (payload), reservando 15 bytes para o cabeçalho:
# 'total:num:' (ex: 003:001:)
PAYLOAD_SIZE    = BUFFER_SIZE - 8

# Definindo o tempo de timeout do socket em segundos
TIMEOUT_SOCKET  = 2.0

# Definindo o tamanho do CHUNK de leitura - Definido em 64 KB para leitura do disco.
CHUNK_SIZE = 65536

# Definindo os diretórios de arquivos de imagens no servidor e cliente
DIR_IMG_SERVER  = os.path.dirname(__file__) + '\\server_files'
DIR_IMG_CLIENT  = os.path.dirname(__file__) + '\\client_files'

# Comandos válidos no servidor
COMANDOS_SERVER = [ '\\?', '\\f', '\\d']
# --------------------------------------------------------------------------------