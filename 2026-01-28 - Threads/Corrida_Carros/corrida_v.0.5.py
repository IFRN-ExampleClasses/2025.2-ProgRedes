# Threads - Versão 0.5: Solução Drástica com Lock (Serialização)
# OBJETIVO: 
# 1. Mostrar variáveis globais compartilhadas (quem chega primeiro).
# 2. Manter a explicação visual da concorrência (comentários da v0.4).
# 3. Tentar resolver a Race Condition usando um Lock (bloqueio).
# 4. Mostrar o perigo de bloquear uma área muito grande (Granularidade Grossa).
# 5. O código deixa de ser concorrente na prática e vira sequencial.
import threading
import time

# ----------------------------------------------------------------------
# Constantes e Variáveis Globais
VOLTAS_POR_CORRIDA = 5

# Variável que armazenará o nome do vencedor.
# É iniciada como None para indicar que ninguém ganhou ainda.
# Como é uma variável GLOBAL, todas as threads podem lê-la e alterá-la.
vencedor = None

# [NOVO NA v0.5] Criando o objeto de bloqueio (Lock)
# Ele funciona como uma chave única: só quem tem a chave executa o código.
lck = threading.Lock()

# Ajuste das velocidades para serem muito próximas (milésimos de segundo),
# forçando uma disputa acirrada pela variável 'vencedor'.
PILOTOS = [
   {"nome": "Lewis Hamilton",   "velocidade": 2.002},
   {"nome": "Sebastian Vettel", "velocidade": 2.001},
   {"nome": "Max Verstappen",   "velocidade": 2.003}
]

# ----------------------------------------------------------------------
# Função executada em paralelo (Target da Thread)
def carroF1(nomePiloto: str, velocidadePiloto: int) -> None:
   # A palavra-chave 'global' permite que esta função altere
   # a variável 'strVencedor' que foi definida fora do escopo da função.
   global strVencedor
   
   # [NOVO NA v0.5] Print para indicar que a thread começou (antes do bloqueio)
   print(f'{nomePiloto} largou...')

   # [NOVO NA v0.5] INÍCIO DO BLOQUEIO (acquire)
   # A thread tenta pegar a chave. Se alguém já estiver usando (correndo), ela 
   # FICA PARADA AQUI esperando a chave ser liberada.
   # IMPACTO: Como colocamos isso ANTES do loop, transformamos a corrida
   # em uma fila indiana. Um carro só corre quando o outro acaba.
   lck.acquire()
   
   intVoltas = 0
   while intVoltas < VOLTAS_POR_CORRIDA:
      # time.sleep pausa a execução deste bloco. 
      # Como estamos usando Threads, apenas ESTA thread dorme.
      # As outras continuam rodando (Concorrência).
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
      # [NOTA DA v0.5]: Devido ao lck.acquire() acima, a saída NÃO será 
      # mais misturada. O efeito visual explicado acima foi "anulado"
      # pelo bloqueio total da função.
      print(f'Piloto: {nomePiloto} / Volta: {intVoltas:02d}', end=' -> ')
   
   # Ao sair do loop, usamos a função padrão para anunciar o término.
   exibirVolta(f"\n{nomePiloto} concluiu a prova!!!\n")
   
   # -------------------------------------------------------------------
   # ÁREA DE PERIGO: CONDIÇÃO DE CORRIDA (RACE CONDITION)
   # O código abaixo ilustra onde o erro pode acontecer.
   # Cenário Hipotético de Falha (M1 a M5):
   #
   # [M1] Lewis chega, testa (vencedor is None?) -> Verdadeiro.
   # [M2] O Sistema Operacional PAUSA Lewis (perde CPU) antes de gravar.
   #      Sebastian ganha a CPU.
   # [M3] Sebastian testa (vencedor is None?) -> Verdadeiro (Lewis não gravou!).
   #      Sebastian ainda está correndo ou acabou de chegar.
   # [M4] Lewis ganha a CPU de volta e faz: vencedor = 'Lewis Hamilton'.
   # [M5] Sebastian ganha a CPU de volta e faz: vencedor = 'Sebastian Vettel'.
   #
   # RESULTADO: Lewis chegou primeiro, mas Sebastian sobrescreveu a variável.
   # -------------------------------------------------------------------
   
   # [NOTA DA v0.5]: O bloco abaixo agora está "seguro" porque está dentro
   # da área protegida pelo Lock. Nenhuma outra thread pode entrar aqui
   # enquanto a chave não for liberada.
   if strVencedor is None:
      strVencedor = nomePiloto

   # [NOVO NA v0.5] FIM DO BLOQUEIO (release)
   # Devolve a chave. O próximo piloto que estava esperando no 'acquire'
   # agora acorda e pode finalmente começar suas voltas.
   lck.release()

# ----------------------------------------------------------------------
# Função auxiliar para imprimir mensagens (Mantida igual às versões anteriores)
def exibirVolta(mensagem: str) -> None:
   print(mensagem)

# ----------------------------------------------------------------------
# Programa Principal
try:
   print("\n>>> Iniciando a corrida (Versão 0.5 - Lock Global/Serializado) <<<\n")
   
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
   # Com o Lock, o vencedor será correto, mas a corrida foi "falsa" (um de cada vez).
   print(f"A prova terminou .... {strVencedor} VENCEEEUUUU!!!")
except Exception as erro:
   print(f"\nERRO: nao foi possivel iniciar a corrida. Detalhes: {erro}\n")