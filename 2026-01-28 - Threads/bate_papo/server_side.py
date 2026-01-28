import socket, threading

# ------------------------------------------------------------
# Configurações globais
DEBUG  = True
ENDIAN = 'big'

# Cria lista global de clientes conectados
lstClientes = list()

# ------------------------------------------------------------
# Função que trata as mensagens de um cliente
def trataCliente(con, src):
   # Loop de recepção de mensagens
   while True:
      # Recebe tamanho e mensagem
      tam = con.recv(4)

      # Recebe a mensagem completa
      msg = con.recv(int.from_bytes(tam, ENDIAN))

      # Verifica se conexão foi encerrada
      if tam == b'' or msg == b'':
         con.close()
         lstClientes.remove((con,src))
         break

      # Exibe mensagem recebida (se em modo debug)
      if DEBUG: print (f"Recebido de {src}: {msg}!!!")

      # Reenvia a mensagem para os outros clientes
      for cli_con, _ in lstClientes:
         if cli_con != con:
            cli_con.send(tam)
            cli_con.send(msg)


# ------------------------------------------------------------
# Configurações do servidor
PORT= 12345

# Cria o socket do servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 12345))
sock.listen(1)

# Loop principal do servidor
while True:
   # Aceita novas conexões
   con, src = sock.accept()

   # Exibe mensagem de conexão aceita (se em modo debug)
   if DEBUG: print (f"Conexao aceita de {src}!!!")

   # Adiciona o cliente à lista e inicia a thread de tratamento
   lstClientes.append((con, src))
   threading.Thread(target=trataCliente, args=(con, src)).start()
    