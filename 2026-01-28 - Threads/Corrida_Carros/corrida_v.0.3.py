# Threads - Versão 0.3: Controle de Estado Global e Explicação Visual
# OBJETIVO: 
# 1. Mostrar variáveis globais compartilhadas (quem chega primeiro).
# 2. Explicar visualmente a concorrência através do print misturado.
# 3. Manter a estrutura das versões anteriores (uso de exibirVolta).
# 4. Demonstrar o uso de .join() para sincronização final.
import threading
import time

# ----------------------------------------------------------------------
# Constantes e Variáveis Globais
VOLTAS_POR_CORRIDA = 5

# Variável que armazenará o nome do vencedor.
# É iniciada como None para indicar que ninguém ganhou ainda.
# Como é uma variável GLOBAL, todas as threads podem lê-la e alterá-la.
vencedor = None

PILOTOS = [
   {"nome": "Lewis Hamilton",   "velocidade": 2},
   {"nome": "Sebastian Vettel", "velocidade": 4},
   {"nome": "Max Verstappen",   "velocidade": 1}
]

# ----------------------------------------------------------------------
# Função executada em paralelo (Target da Thread)
def carroF1(nomePiloto: str, velocidadePiloto: int) -> None:
   # A palavra-chave 'global' permite que esta função altere
   # a variável 'strVencedor' que foi definida fora do escopo da função.
   global strVencedor
   
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
      # 2. Velocidade: Sebastian (vel 4) dorme apenas 0.25s. 
      #    Lewis (vel 2) dorme 0.50s. Por isso o 'S' aparece o dobro 
      #    de vezes que o 'L' no mesmo intervalo de tempo.
      # 3. Formatação: O parâmetro end=' -> ' impede que o print pule 
      #    para a próxima linha, "grudando" a saída de todos os carros.
      # ----------------------------------------------------------------
      print(f'Piloto: {nomePiloto} / Volta: {intVoltas:02d}', end=' -> ')
   
   # Ao sair do loop, usamos a função padrão para anunciar o término.
   exibirVolta(f"\n{nomePiloto} concluiu a prova!!!\n")
   
   # Lógica para definir o vencedor (Check-and-Set)
   # Verifica se a variável global ainda está vazia (None).
   # A primeira thread a chegar aqui encontrará None e gravará seu nome.
   # As próximas encontrarão o nome do primeiro e não farão nada.
   if strVencedor is None:
      strVencedor = nomePiloto

# ----------------------------------------------------------------------
# Função auxiliar para imprimir mensagens (Mantida igual às versões anteriores)
def exibirVolta(mensagem: str) -> None:
   print(mensagem)

# ----------------------------------------------------------------------
# Programa Principal
try:
   print("\nv>>> Iniciando a corrida (Versão 0.3 - Completa) <<<\n")
   
   # Reinicia o vencedor (segurança caso rode múltiplas vezes)
   strVencedor = None
   
   listaDeThreads = []

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
      # "Comece a executar essa função agora, mas não trave o meu código principal".
      # O Python agenda a execução e passa imediatamente para a próxima iteração do loop.
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
   
   # Exibe o valor que foi gravado na variável global pela thread mais rápida
   print(f"\nA prova terminou .... {strVencedor} VENCEEEUUUU!!!\n")

except Exception as erro:
   print(f"\nERRO: nao foi possivel iniciar a corrida. Detalhes: {erro}\n")