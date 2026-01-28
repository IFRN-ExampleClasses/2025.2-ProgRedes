# Threads - Versão 0.0: Execução Síncrona (Sequencial)
# Neste modelo, uma tarefa deve terminar completamente para a próxima começar.
import time

# ----------------------------------------------------------------------
# Constantes Globais
# Define quantas voltas cada piloto deve dar para completar a prova.
VOLTAS_POR_CORRIDA = 3

# Lista de dicionários contendo os dados dos pilotos.
PILOTOS = [
   {"nome": "Lewis Hamilton",   "velocidade": 2},
   {"nome": "Sebastian Vettel", "velocidade": 4},
   {"nome": "Max Verstappen",   "velocidade": 1}
]

# ----------------------------------------------------------------------
# Função que simula o comportamento de um carro de F1 na pista.
def carroF1(nomePiloto: str, velocidadePiloto: int) -> None:
   intVoltas = 0
   
   # Loop que simula as voltas da corrida
   while intVoltas < VOLTAS_POR_CORRIDA:
      # time.sleep pausa a execução deste bloco. 
      # Como estamos no modo sequencial, TODO o programa congela aqui.
      time.sleep(1 / velocidadePiloto)
      
      intVoltas += 1
      print(f"{nomePiloto}: {time.ctime(time.time())} .... {intVoltas}")
   
   # Ao sair do loop, o piloto terminou.
   exibirVolta(f"\n{nomePiloto} concluiu a prova!!!\n")

# ----------------------------------------------------------------------
# Função auxiliar para imprimir mensagens
def exibirVolta(mensagem: str) -> None:
   print(mensagem)

# ----------------------------------------------------------------------
# Programa Principal (Main)
try:
   print("\n>>> Iniciando a corrida (Modo Sequencial) <<<\n")
   
   # Itera sobre a lista de pilotos
   for piloto in PILOTOS:
      # CHAMADA BLOQUEANTE:
      # O programa entra na função carroF1 e só sai de lá quando
      # o piloto atual terminar todas as suas voltas.
      # O próximo piloto da lista terá que esperar sua vez.
      carroF1(piloto["nome"], piloto["velocidade"])

   # Esta mensagem só será exibida após o ÚLTIMO piloto terminar.
   print("\nA corrida terminou!!!\n")
   
   print("\nQuem foi o vencedor? (Neste modelo, vence quem correu primeiro...)\n")

except Exception as erro:
   print(f"\nERRO: nao foi possivel iniciar a corrida. Detalhes: {erro}\n")