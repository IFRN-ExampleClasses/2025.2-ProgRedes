import os, sys, requests, platform

'''
    Deve ser criado um arquivo com o nome token_bot.py
    e dentro criar a "constante" API_TOKEN e
    atribuir o valor do token informado pelo Bot Father
'''

from token_bot import *

# Definine as URLs 
strURLBase        = f'https://api.telegram.org/bot{API_TOKEN}'
strURLGetUpdates  = f'{strURLBase}/getUpdates'
strURLSendMessage = f'{strURLBase}/sendMessage'

# Limpa a tela
os.system('cls' if platform.system() == 'Windows' else 'clear')

# Mensagem inicial
print('\nBOT TELEGRAM - Aguardando mensagens...')
print('---------------------------------------\n')

# Inicializa a variável de controle do ID da última mensagem
intIDUltimaMensagem = 0

# Loop infinito -> Modo Passivo
while True:
   # Obtém as mensagens
   reqURL = requests.get(strURLGetUpdates)

   # Verifica se a requisição de recebimento não foi bem sucedida
   if not reqURL.status_code == 200:
      sys.exit('\nERRO: Erro ao obter mensagem...\nCÓDIGO DE RETORNO: ' + str(reqURL.status_code))

   # COnverte a resposta para JSON
   jsonRetorno   = reqURL.json()

   # Obtém o ID da última mensagem
   intIDMensagem = jsonRetorno['result'][-1]['message']['message_id']

   # Verifica se a última mensagem é a mesma
   if intIDMensagem == intIDUltimaMensagem: continue

   # Obtém o comando e o ID do chat
   strComando    = jsonRetorno['result'][-1]['message']['text']
   intIDChat     = jsonRetorno['result'][-1]['message']['chat']['id']
   
   # Atualiza o ID da última mensagem
   intIDUltimaMensagem = intIDMensagem

   # Verifica o comando
   if strComando == '/?':
      strMensagemRetorno = f'BOT: Texto de Ajuda...\nUsuário:{intIDChat}'
   elif strComando == '/start':
      strMensagemRetorno = f'BOT: Bem vindo ao BOT...\nUsuário:{intIDChat}'
   else:
      strMensagemRetorno = f'BOT: Comando não reconhecido...\nUsuário:{intIDChat}'

   # Envia a mensagem de retorno
   dictDados = {'chat_id':intIDChat, 'text':strMensagemRetorno}
   reqURL = requests.post(strURLSendMessage, data=dictDados) 

   # Verifica se a requisição de envio não foi bem sucedida
   if not reqURL.status_code == 200:
      sys.exit('\nERRO: Erro ao enviar mensagem...\nCÓDIGO DE RETORNO: ' + str(reqURL.status_code))
