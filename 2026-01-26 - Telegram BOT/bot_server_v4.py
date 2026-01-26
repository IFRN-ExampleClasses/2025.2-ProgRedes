import os, sys, requests, platform, json

'''
    Deve ser criado um arquivo com o nome token_bot.py
    e dentro criar a "constante" API_TOKEN e
    atribuir o valor do token informado pelo Bot Father
'''

from token_bot import *

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
            # Atualizando o ID para a última atualização processada
            if jsonRetorno["result"][-1]["update_id"] >= intIDUltimaAtualizacao:
               intIDUltimaAtualizacao = jsonRetorno["result"][-1]["update_id"]

            # Ignorando se não for uma mensagem 
            if 'message' not in atualizacao: continue

            # Obtendo os dados da última atualização
            intIDUltimaAtualizacao = jsonRetorno["result"][-1]["update_id"]
            strMensagem            = jsonRetorno["result"][-1]["message"]["text"]
            intIDChat              = jsonRetorno["result"][-1]["message"]["chat"]["id"]

            # Adicionando à fila de atualizações
            lstFilaAtualizacoes.append((intIDChat, strMensagem, intIDUltimaAtualizacao))

            # Exibindo a última mensagem recebida
            print(f'Mensagem recebida {intIDUltimaAtualizacao} do chat {intIDChat}: {strMensagem}')

         # Processando a fila de atualizações -> Enviando respostas
         for (intIDChat, strMensagem, intIDUltimaAtualizacao) in lstFilaAtualizacoes:
            # Envia a mensagem de retorno
            strMensagemDevolvida = f'Você enviou a mensagem:\n"{strMensagem.upper()}"'
            dictRetorno          = {'chat_id':intIDChat, 'text':strMensagemDevolvida}
            reqURL = requests.post(strURLSendMessage, data=dictRetorno) 
except KeyboardInterrupt:
   sys.exit('\n\nEncerrando o BOT Telegram...\n')
except Exception as e:
   sys.exit(f'\n\nERRO: {e}\n')  