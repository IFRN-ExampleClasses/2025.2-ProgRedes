# Threads - Versão 0.7: Checagem em Tempo Real (Lock dentro do Loop)
# OBJETIVO: 
# 1. Mostrar variáveis globais compartilhadas (quem chega primeiro).
# 2. Manter a explicação visual da concorrência (comentários da v0.4/0.5/0.6).
# 3. [AJUSTE v0.6] Demonstrar o conceito de "Granularidade Fina" (bloquear pouco).
# 4. [AJUSTE v0.7] Mudar a estratégia de verificação do vencedor:
#    Em vez de verificar após o fim da corrida, verificamos a cada volta
#    se aquela foi a volta final e se já temos um vencedor.
import threading
import time

# ----------------------------------------------------------------------
# Constantes e Variáveis Globais
VOLTAS_POR_CORRIDA = 5

# Variável que armazenará o nome do vencedor.
strVencedor = None

# Criando o objeto de bloqueio (Lock)
lck = threading.Lock()

# Ajuste das velocidades para serem muito próximas (milésimos de segundo),
# forçando uma disputa acirrada pela variável 'strVencedor'.
PILOTOS = [
   {"nome": "Lewis Hamilton",   "velocidade": 2.00001},
   {"nome": "Sebastian Vettel", "velocidade": 2.00002},
   {"nome": "Max Verstappen",   "velocidade": 2.000025}
]

# ----------------------------------------------------------------------
# Função executada em paralelo (Target da Thread)
def carroF1(nomePiloto: str, velocidadePiloto: int) -> None:
   # A palavra-chave 'global' permite que esta função altere
   # a variável 'strVencedor' que foi definida fora do escopo da função.
   global strVencedor
   
   # [NOVO NA v0.5] Print para indicar que a thread começou
   print(f'{nomePiloto} largou...')

   # [AJUSTE v0.6 - LOCK REMOVIDO DAQUI]
   # Na versão 0.5, fazíamos lck.acquire() AQUI.
   # ISSO CAUSAVA UM PROBLEMA GRAVE: O carro bloqueava a pista inteira
   # para si mesmo (fila indiana), matando o paralelismo.
   # Nesta versão, deixamos o código seguir livre para o loop abaixo.
   
   intVoltas = 0
   while intVoltas < VOLTAS_POR_CORRIDA:
      # time.sleep pausa a execução deste bloco. 
      # Como o Lock não está ativo aqui, todas as threads dormem e 
      # acordam simultaneamente (Concorrência Real restaurada).
      time.sleep(1 / velocidadePiloto)
      
      # [AJUSTE v0.7 - INÍCIO DO BLOQUEIO (Dentro do Loop)]
      # Diferente da v0.6 (que travava só no final), agora travamos
      # a cada volta para atualizar o contador e verificar o estado com segurança.
      lck.acquire()
      
      # O incremento agora é uma operação atômica/protegida
      intVoltas += 1
      
      # -------------------------------------------------------------------
      # ÁREA DE PERIGO: CONDIÇÃO DE CORRIDA (RACE CONDITION)
      # O código abaixo ilustra onde o erro poderia acontecer se não houvesse Lock.
      # Cenário Hipotético de Falha (M1 a M5):
      #
      # [M1] Lewis chega, testa (strVencedor is None?) -> Verdadeiro.
      # [M2] O Sistema Operacional PAUSA Lewis (perde CPU) antes de gravar.
      #      Sebastian ganha a CPU.
      # [M3] Sebastian testa (strVencedor is None?) -> Verdadeiro (Lewis não gravou!).
      # [M4] Lewis ganha a CPU de volta e faz: strVencedor = 'Lewis Hamilton'.
      # [M5] Sebastian ganha a CPU de volta e faz: strVencedor = 'Sebastian Vettel'.
      # -------------------------------------------------------------------
      
      # [AJUSTE v0.7]: A verificação agora é instantânea (na volta exata).
      # Este bloco está SEGURO pois estamos dentro do lck.acquire().
      if intVoltas == VOLTAS_POR_CORRIDA and strVencedor is None:
         strVencedor = nomePiloto

      # [AJUSTE v0.7 - FIM DO BLOQUEIO]
      # Liberamos a chave rapidamente para outras threads poderem processar suas voltas.
      lck.release()
      
      # ----------------------------------------------------------------
      # EXPLICAÇÃO DA SAÍDA "MISTURADA" (Ex: S01.L01.S02.M01...):
      # 1. Concorrência: O terminal é um recurso único compartilhado. 
      # 2. Velocidade: As velocidades agora são muito próximas.
      # 3. Formatação: O parâmetro end=' -> ' "gruda" a saída.
      # ----------------------------------------------------------------
      # [NOTA DA v0.6/v0.7]: O print continua FORA do lock.
      # Isso garante que a "briga" visual pelo terminal continue acontecendo
      # de forma misturada e caótica (paralelismo real).
      print(f'Piloto: {nomePiloto} / Volta: {intVoltas:02d}', end=' -> ')
   
   # Ao sair do loop, usamos a função padrão para anunciar o término.
   exibirVolta(f"\n{nomePiloto} concluiu a prova!!!\n")

# ----------------------------------------------------------------------
# Função auxiliar para imprimir mensagens (Mantida igual às versões anteriores)
def exibirVolta(mensagem: str) -> None:
   print(mensagem)

# ----------------------------------------------------------------------
# Programa Principal
try:
   print("\n>>> Iniciando a corrida (Versão 0.7 - Checagem Real-Time) <<<\n")
   
   # Reinicia o vencedor (segurança caso rode múltiplas vezes)
   strVencedor = None
   
   listaDeThreads = list()

   # 1. Fase de Criação e Disparo
   for piloto in PILOTOS:
      t = threading.Thread(
         target=carroF1, 
         args=(piloto["nome"], piloto["velocidade"])
      )
      t.start()
      listaDeThreads.append(t)

   # 2. Fase de Sincronização (Barreira)
   for threadDoPiloto in listaDeThreads:
      threadDoPiloto.join()

   print("\nA corrida terminou!!!\n")
   
   # Exibe o valor que foi gravado na variável global.
   # Agora temos: Corrida Paralela + Checagem Instantânea + Resultado Correto.
   print(f"\nA prova terminou .... {strVencedor} VENCEEEUUUU!!!\n")

except Exception as erro:
   print(f"\nERRO: nao foi possivel iniciar a corrida. Detalhes: {erro}\n")