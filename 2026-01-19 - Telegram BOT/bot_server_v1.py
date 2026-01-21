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
# -1 indica que nenhuma mensagem foi recebida ainda
intIDUltimaMensagem = -1

# Loop infinito -> Modo Passivo
while True:
   # Obtém as mensagens
   reqURL = requests.get(strURL + '/getUpdates')

   # Verifica se a requisição não foi bem sucedida
   if not reqURL.status_code == 200:
      sys.exit(f'\nERRO: Erro ao acessar a URL\nCÓDIGO DE RETORNO: {reqURL.status_code}')

   # Verifica se não há mensagens
   if reqURL.json()['result'] == []: continue

   # Converte a resposta para JSON
   jsonRetorno = reqURL.text

   # Obtém o ID da última mensagem da Requisição
   intIDMensagemAtual = jsonRetorno['result'][-1]['message']['message_id']

   # Verifica se o ID da última mensagem é igual ao ID da mensagem atual
   # Se for igual, volta o loop para o início (ignora a mensagem)
   if intIDMensagemAtual == intIDUltimaMensagem: continue
      
   # Atualiza o ID da última mensagem
   intIDUltimaMensagem = intIDMensagemAtual
   
   # Exibe as mensagens recebidas
   print(f'{jsonRetorno}')
   print('-'*100+'\n')