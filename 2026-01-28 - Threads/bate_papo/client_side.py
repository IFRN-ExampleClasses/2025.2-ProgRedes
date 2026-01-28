import socket, threading

# ------------------------------------------------------------
# Configurações globais
DEBUG  = True
ENDIAN = 'big'

# ------------------------------------------------------------
# Função que trata as mensagens recebidas do servidor
def trataServidor(con):
   # Variável global de controle
   global boolContinua
   # Define timeout para evitar bloqueio na recepção
   con.settimeout(1)
   # Loop de recebimento de mensagens
   while boolContinua:
      try:
         # Recebe tamanho da mensagem
         tam = con.recv(4) 
         # Verifica se conexão foi encerrada
         if tam == b'' or msg == b'':
            boolContinua = False
            con.close()
            break
         # Recebe a mensagem completa
         msg = con.recv(int.from_bytes(tam, ENDIAN))
         # Exibe a mensagem recebida
         print(f"\n{msg.decode()}")
         # Reexibe o prompt de entrada
         print("Digite uma mensagem: ")
      except Exception:
         None
            

# ------------------------------------------------------------
# Programa principal - Cliente

# Parâmetros de conexão
SERVER = 'localhost'
PORT   = 12345

# Cria socket e conecta ao servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))

# Inicia thread para tratar mensagens do servidor
boolContinua = True
threading.Thread(target=trataServidor, args=(sock,)).start()

# Loop principal para envio de mensagens ao servidor
while boolContinua:
   try:
      # Lê mensagem do usuário
      strMensagem = input("Digite uma mensagem: ")
      # Verifica se deve enviar a mensagem
      if strMensagem != '' and boolContinua: 
         msg = strMensagem.encode()
         sock.send(len(msg).to_bytes(4, ENDIAN))   
         sock.send(msg) 
   except KeyboardInterrupt:
      print("Cliente encerrado!")
      boolContinua = False         