# Importando a biblioteca SOCKET
import socket

# ----------------------------------------------------------------------
HOST_IP_SERVER  = ''              # Definindo o IP do servidor
HOST_PORT       = 50000           # Definindo a porta
CODE_PAGE       = 'utf-8'         # Definindo a página de 
                                  # codificação de caracteres
BUFFER_SIZE     = 512             # Tamanho do buffer
# ----------------------------------------------------------------------

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta
sockServer.bind((HOST_IP_SERVER, HOST_PORT)) 

# Definindo um timeout de 0.5 segundos para o socket
sockServer.settimeout(0.5)

print('\nRecebendo Mensagens...')
print('Pressione CTRL+C para encerrar o servidor...\n')
print('-' * 100 + '\n')

try:
    while True:
        try:
            # Recebendo os dados do cliente
            byteMensagem, tuplaCliente = sockServer.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            continue
        else:
            # Obtendo o nome (HOST) do Cliente
            strNomeHost = socket.gethostbyaddr(tuplaCliente[0])[0]
            strNomeHost = strNomeHost.split('.')[0].upper()
            # Imprimindo a mensagem recebida convertendo de bytes para string
            print(f'{tuplaCliente} -> {strNomeHost}: {byteMensagem.decode(CODE_PAGE)}')

except KeyboardInterrupt:
    print('\n\nAVISO: Interrupção detectada (CTRL + C). Encerrando servidor...')

finally:
    # Fechando o socket
    sockServer.close()
    print('Servidor finalizado com sucesso.')
