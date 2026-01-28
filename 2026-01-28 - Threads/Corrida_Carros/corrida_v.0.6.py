# Threads - Versão 0.6: Solução Correta com Lock (Granularidade Fina)
# OBJETIVO: 
# 1. Mostrar variáveis globais compartilhadas (quem chega primeiro).
# 2. Manter a explicação visual da concorrência (comentários da v0.4/0.5).
# 3. Tentar resolver a Race Condition usando um Lock (bloqueio).
# 4. [AJUSTE v0.6] Demonstrar o conceito de "Granularidade Fina":
#    Reduzir o escopo do bloqueio para recuperar o paralelismo perdido na v0.5.
import threading
import time

# ----------------------------------------------------------------------
# Constantes e Variáveis Globais
VOLTAS_POR_CORRIDA = 5

# Variável que armazenará o nome do vencedor.
# É iniciada como None para indicar que ninguém ganhou ainda.
# Como é uma variável GLOBAL, todas as threads podem lê-la e alterá-la.
strVencedor = None

# [NOVO NA v0.5] Criando o objeto de bloqueio (Lock)
# Ele funciona como uma chave única: só quem tem a chave executa o código.
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
   # Nesta versão 0.6, deixamos o código seguir livre para o loop abaixo.
   
   intVoltas = 0
   while intVoltas < VOLTAS_POR_CORRIDA:
      # time.sleep pausa a execução deste bloco. 
      # Como o Lock não está ativo aqui, todas as threads dormem e 
      # acordam simultaneamente (Concorrência Real restaurada).
      time.sleep(1 / velocidadePiloto)
      
      intVoltas += 1
      
      # ----------------------------------------------------------------
      # EXPLICAÇÃO DA SAÍDA "MISTURADA" (Ex: S01.L01.S02.M01...):
      # 1. Concorrência: O terminal é um recurso único compartilhado. 
      #    As 3 threads escrevem nele assim que acordam, sem fila.
      # 2. Velocidade: As velocidades agora são muito próximas, gerando
      #    uma alternância quase caótica no terminal.
      # 3. Formatação: O parâmetro end=' -> ' impede que o print pule 
      #    para a próxima linha, "grudando" a saída de todos os carros.
      # ----------------------------------------------------------------
      # [NOTA DA v0.6]: Diferente da v0.5 (que era sequencial), aqui a 
      # saída VOLTA A SER MISTURADA e caótica, pois removemos o Lock
      # de antes do loop. Os carros estão correndo juntos novamente!
      print(f'Piloto: {nomePiloto} / Volta: {intVoltas:02d}', end=' -> ')
   
   # [AJUSTE v0.6 - INÍCIO DO BLOQUEIO (Granularidade Fina)]
   # Movemos o acquire para cá. Protegemos APENAS a linha de chegada e
   # o acesso à variável global. O resto da corrida foi livre.
   lck.acquire()

   # Ao sair do loop, usamos a função padrão para anunciar o término.
   exibirVolta(f"\n{nomePiloto} concluiu a prova!!!\n")
   
   # -------------------------------------------------------------------
   # ÁREA DE PERIGO: CONDIÇÃO DE CORRIDA (RACE CONDITION)
   # O código abaixo ilustra onde o erro pode acontecer.
   # Cenário Hipotético de Falha (M1 a M5):
   #
   # [M1] Lewis chega, testa (strVencedor is None?) -> Verdadeiro.
   # [M2] O Sistema Operacional PAUSA Lewis (perde CPU) antes de gravar.
   #      Sebastian ganha a CPU.
   # [M3] Sebastian testa (strVencedor is None?) -> Verdadeiro (Lewis não gravou!).
   #      Sebastian ainda está correndo ou acabou de chegar.
   # [M4] Lewis ganha a CPU de volta e faz: strVencedor = 'Lewis Hamilton'.
   # [M5] Sebastian ganha a CPU de volta e faz: strVencedor = 'Sebastian Vettel'.
   #
   # RESULTADO: Lewis chegou primeiro, mas Sebastian sobrescreveu a variável.
   # -------------------------------------------------------------------
   
   # [NOTA DA v0.5/v0.6]: Este bloco está SEGURO.
   # Mesmo que dois carros cheguem aqui ao mesmo tempo, o Lock garante
   # que apenas um entre no 'if' por vez.
   if strVencedor is None:
      strVencedor = nomePiloto

   # [AJUSTE v0.6 - FIM DO BLOQUEIO (release)]
   # Liberamos a chave imediatamente após o uso crítico.
   lck.release()

# ----------------------------------------------------------------------
# Função auxiliar para imprimir mensagens (Mantida igual às versões anteriores)
def exibirVolta(mensagem: str) -> None:
   print(mensagem)

# ----------------------------------------------------------------------
# Programa Principal
try:
   print("\n>>> Iniciando a corrida (Versão 0.6 - Granularidade Fina) <<<\n")
   
   # Reinicia o vencedor (segurança caso rode múltiplas vezes)
   strVencedor = None
   
   listaDeThreads = list()

   # 1. Fase de Criação e Disparo
   # Iteramos a lista PILOTOS como no arquivo anterior.
   for piloto in PILOTOS:
      # Criação do objeto Thread:
      # target: define qual função vai rodar em paralelo.
      # args: tupla com os argumentos que a função 'carroF1' precisa receber.
      t = threading.Thread(
         target=carroF1, 
         args=(piloto["nome"], piloto["velocidade"])
      )
      
      # O método .start() diz ao sistema operacional: 
      # "Comece a executar essa função agora".
      t.start()
      
      # Guardamos a referência da thread na lista para usar no join()
      listaDeThreads.append(t)

   # 2. Fase de Sincronização (Barreira)
   # O programa principal precisa esperar todos terminarem para anunciar o pódio.
   for threadDoPiloto in listaDeThreads:
      # O método .join() bloqueia o programa principal AQUI até que
      # a thread específica termine sua tarefa.
      threadDoPiloto.join()

   print("\nA corrida terminou!!!\n")
   
   # Exibe o valor que foi gravado na variável global.
   # Agora temos: Corrida Paralela (rápida) + Resultado Correto (seguro).
   print(f"\nA prova terminou .... {strVencedor} VENCEEEUUUU!!!\n")

except Exception as erro:
   print(f"\nERRO: nao foi possivel iniciar a corrida. Detalhes: {erro}\n")