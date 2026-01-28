# Threads - Versão 0.2: Execução Assíncrona com Sincronização (Join)
# Neste modelo, o programa dispara tarefas em segundo plano e 
# aguarda todas terminarem antes de encerrar o programa.
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
# Função que será executada em paralelo (Target da Thread)
def carroF1(nomePiloto: str, velocidadePiloto: int) -> None:
   intVoltas = 0
   while intVoltas < VOLTAS_POR_CORRIDA:
      # Pausa APENAS esta thread.
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
   print("\n>>> Iniciando a corrida (Modo Threads com Join) <<<\n")
   
   # Lista para manter o controle das threads criadas
   listaDeThreads = []

   # 1. Fase de Criação e Disparo
   for piloto in PILOTOS:
      t = threading.Thread(
         target=carroF1, 
         args=(piloto["nome"], piloto["velocidade"])
      )
      
      # O método .start() inicia a execução paralela
      t.start()
      
      # Guardamos a referência da thread na lista para usar depois
      listaDeThreads.append(t)

   # 2. Fase de Sincronização (Barreira)
   # Se não fizermos isso, o "print" final sairia antes da corrida acabar.
   for threadDoPiloto in listaDeThreads:
      # O método .join() bloqueia o programa principal AQUI até que
      # a thread específica termine sua tarefa.
      threadDoPiloto.join()

   # Como usamos o join() acima, esta mensagem só aparece quando 
   # TODOS os pilotos (threads) tiverem terminado.
   print("\nA corrida terminou!!!\n")

except Exception as erro:
   print(f"\nERRO: nao foi possivel iniciar a corrida. Detalhes: {erro}\n")