import os, sys, requests, platform, json

'''
    Deve ser criado um arquivo com o nome token_bot.py
    e dentro criar a "constante" API_TOKEN e
    atribuir o valor do token informado pelo Bot Father
'''

from token_bot import *
from funcoes_bot import *

strURLBase        = f'https://api.telegram.org/bot{API_TOKEN}'
strURLGetUpdates  = f'{strURLBase}/getUpdates'
strURLSendMessage = f'{strURLBase}/sendMessage'

# Limpando a tela
os.system('cls' if platform.system() == 'Windows' else 'clear')

# Mensagem inicial
print('\nBOT TELEGRAM - Aguardando mensagens...')
print('Pressione Ctrl+C para encerrar o BOT')
print('---------------------------------------\n')

# Inicializando o ID da última atualização
intIDUltimaAtualizacao = 0

# Try principal -> Captura de exceções gerais / encerramento do BOT
try:
   # Loop infinito -> Modo Passivo
   while True:
      # Try secundário -> Captura de timeout na requisição
      try:
         # Obtendo as atualizações a partir do ID da última atualização
         reqURL = requests.get(strURLGetUpdates,  
                               params={'offset': intIDUltimaAtualizacao + 1, 'timeout': 20},
                              timeout=25)
      # Timeout -> Continua o loop
      except requests.Timeout:
         continue
      else:
         # Verificando se a requisição não foi bem sucedida
         if not reqURL.status_code == 200:
            sys.exit('\nERRO: Erro ao acessar a URL\nCÓDIGO DE RETORNO: ' + str(reqURL.status_code))

         # Convertendo o dicionário JSON de retorno (') para um objeto JSON Nativo (")
         jsonRetorno = json.loads(reqURL.text)

         # Verifica se o resultado está vazio -> Retorna ao início do loop
         if jsonRetorno["result"] == []: continue

         # Processando cada atualização recebida
         lstFilaAtualizacoes = list()
         for atualizacao in jsonRetorno["result"]:
            # Ignorando se não for uma mensagem 
            if 'message' not in atualizacao: continue

            # Atualizando o ID para a última atualização processada
            intIDUltimaAtualizacao = atualizacao["update_id"]

            # Obtendo os dados da última atualização
            strMensagem            = atualizacao["message"]["text"]
            intIDChat              = atualizacao["message"]["chat"]["id"]

            # Adicionando à fila de atualizações
            lstFilaAtualizacoes.append((intIDChat, strMensagem, intIDUltimaAtualizacao))

            # Exibindo a última mensagem recebida
            print(f'Mensagem recebida {intIDUltimaAtualizacao} do chat {intIDChat}: {strMensagem}')

         # Processando a fila de atualizações -> Enviando respostas
         for (intIDChat, strMensagem, intIDUltimaAtualizacao) in lstFilaAtualizacoes:
            if strMensagem == '/start':
               strMensagemDevolvida = startBot()
            elif strMensagem == '/?':
               strMensagemDevolvida = ajudaBot()
            elif strMensagem.startswith('/fatorial:'):
               try:
                  lstArgs = strMensagem.split(':')
                  if len(lstArgs) > 2:
                     raise Exception("ERRO: comando /fatorial requer apenas um argumento...")
                  else:
                     strMensagemDevolvida = fatorialBot(lstArgs[1])
               except Exception as strErro:
                  strMensagemDevolvida = strErro
            elif strMensagem.startswith('/fibonacci:'):
               try:
                  lstArgs = strMensagem.split(':')
                  if len(lstArgs) > 2:
                     raise Exception("ERRO: comando /fibonacci requer apenas um argumento...")
                  else: 
                     strMensagemDevolvida = fibonacciBot(lstArgs[1])
               except Exception as strErro:
                  strMensagemDevolvida = strErro   
            else:
               strMensagemDevolvida = "COMANDO NÃO RECONHECIDO.\n\nEnvie /? para obter ajuda sobre os comandos disponíveis."
            
            # Envia a mensagem de retorno
            dictRetorno = {'chat_id':intIDChat, 'text':strMensagemDevolvida}
            reqURL = requests.post(strURLSendMessage, data=dictRetorno) 
except KeyboardInterrupt:
   sys.exit('\n\nEncerrando o BOT Telegram...\n')
except Exception as e:
   sys.exit(f'\n\nERRO: {e}\n')  