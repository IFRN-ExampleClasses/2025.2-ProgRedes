import os, sys, requests, platform

'''
    Deve ser criado um arquivo com o nome token_bot.py
    e dentro criar a "constante" API_TOKEN e
    atribuir o valor do token informado pelo Bot Father
'''

from token_bot import *

strURL = f'https://api.telegram.org/bot{API_TOKEN}'

# Limpa a tela
os.system('cls' if platform.system() == 'Windows' else 'clear')

# Mensagem inicial
print('\nBOT TELEGRAM - Aguardando mensagens...')
print('---------------------------------------\n')

# Inicializa a variável de controle do ID da última mensagem
intContador = 1

# Loop infinito -> Modo Passivo
while True:
   # Obtém as mensagens
   reqURL = requests.get(strURL + '/getUpdates')

   # Verifica se a requisição não foi bem sucedida
   if not reqURL.status_code == 200:
      sys.exit('\nERRO: Erro ao acessar a URL\nCÓDIGO DE RETORNO: ' + str(reqURL.status_code))

   # Verifica se não há mensagens
   if reqURL.json()['result'] == []: continue

   # Converte a resposta para JSON
   jsonRetorno = reqURL.json()

   # Obtém a mensagem
   strMensagem = jsonRetorno['result'][-1]['message']['text']

   # Exibe a mensagem
   print('REQUISIÇÃO Nº: ' + str(intContador))
   print(f'{strMensagem}')
   print('-'*100+'\n')
   intContador += 1