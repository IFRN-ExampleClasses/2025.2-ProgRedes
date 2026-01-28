# Threads - Versão 0.1: Sem Join (Não-Bloqueante)
# Neste exemplo, a thread principal (Main) dispara os pilotos e 
# encerra sua execução IMEDIATAMENTE, enquanto os pilotos continuam correndo sozinhos.
import threading
import time

# ----------------------------------------------------------------------
# Constantes Globais
VOLTAS_POR_CORRIDA = 3

PILOTOS = [
   {"nome": "Lewis Hamilton",   "velocidade": 2},
   {"nome": "Sebastian Vettel", "velocidade": 4},
   {"nome": "Max Verstappen",   "velocidade": 1}
]

# ----------------------------------------------------------------------
# Função que será executada em paralelo
def carroF1(nomePiloto: str, velocidadePiloto: int) -> None:
   intVoltas = 0
   while intVoltas < VOLTAS_POR_CORRIDA:
      # O time.sleep aqui pausa APENAS esta thread específica.
      # As outras threads (outros carros) continuam rodando.
      time.sleep(1 / velocidadePiloto)
      intVoltas += 1
      print(f"{nomePiloto}: {time.ctime(time.time())} .... {intVoltas}")
   
   exibirVolta(f"\n{nomePiloto} concluiu a prova!!!\n")

# ----------------------------------------------------------------------
def exibirVolta(mensagem: str) -> None:
   print(mensagem)

# ----------------------------------------------------------------------
# Programa Principal
try:
   print("\n>>> Iniciando a corrida (Versão 0.1 - Sem Join) <<<\n")

   # Iterando sobre a lista de pilotos
   for piloto in PILOTOS:
      # Cria a thread configurando a função alvo e os argumentos
      t = threading.Thread(
         target=carroF1, 
         args=(piloto["nome"], piloto["velocidade"])
      )
      
      # Inicia a thread. O Python "agenda" a execução e segue para a próxima linha
      # IMEDIATAMENTE, sem esperar o carro terminar a volta.
      t.start()

   # Como não usamos .join(), o programa principal chega nesta linha
   # milissegundos após disparar as ordens de largada.
   print("\nA corrida terminou!!! (Mas os carros ainda estão correndo...)\n")

except Exception as erro:
   print(f"\nERRO: nao foi possivel iniciar a corrida. Detalhes: {erro}\n")