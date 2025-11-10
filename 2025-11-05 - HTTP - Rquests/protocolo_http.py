import requests, sys, os

# Obtendo o diretório atual
strDirAtual = os.path.dirname(__file__)

# Definindo a URL para fazer a requisição
strURL = 'http://www.tribunadonorte.com.br'

# Definindo os cabeçalhos HTTP
dicHeaders = { 'User-Agent': 'MeuAppPython/1.0' }

try:
   # Fazendo a requisição GET
   response = requests.get(strURL, headers=dicHeaders)
except requests.exceptions.ConnectTimeout:
   sys.exit(f'\nERRO: A conexão demorou demais (Timeout). O servidor pode estar offline ou lento...\n')
except requests.exceptions.RequestException as e:
   sys.exit(f'\nERRO: Ocorreu um erro ao fazer a requisição: {e}\n')
except Exception as e:
   sys.exit(f'\nERRO: {e}\n')
else:
   # ----------------------------------------------------------------------
   # Exibindo o código de status HTTP
   print(f'\nCódigo de status HTTP ....: {response.status_code}')
   print(f'Descrição do status HTTP .: {response.reason}\n')

   # Exibindo os cabeçalhos de resposta
   print('Cabeçalhos de resposta HTTP:')
   print(response.headers)

   # ----------------------------------------------------------------------
   # Exibindo o tipo de conteúdo
   strContentType = response.headers.get('Content-Type', '')
   print(f'Tipo de conteúdo ..........: {strContentType}')  
   
   # ----------------------------------------------------------------------
   # Exibindo o conteúdo da resposta
   print('\nConteúdo da resposta HTTP:')
   print(f'{response.content[:500]}\n... (restante do conteúdo omitido)')
   
   # Salvando a resposta um arquivo
   arqSaida = open(f'{strDirAtual}\\resposta.bin', 'wb')
   arqSaida.write(response.content)
   arqSaida.close()

   # ----------------------------------------------------------------------
   # Exibindo informações adicionais
   print('\nInformações adicionais da resposta:')
   print(f'URL final da requisição .: {response.url}')
   print(f'Tamanho do conteúdo .....: {len(response.content)} bytes')