import sys

import funcoes

try:
   strIP = input('\nDigite um endereço IP (Formato IPv4): ')
except KeyboardInterrupt:
   sys.exit('\nAVISO: Programa interrompido pelo usuário...\n')
except Exception as erro:
   sys.exit(f'\nERRO INESPERADO: {erro}...\n')
else:
   # Obtendo os octetos do endereço IP
   lstOctetos = strIP.split('.')

   # Validando o formato do IP
   if len(lstOctetos) != 4:
      sys.exit('\nERRO: Formato de IP inválido. Deve conter 4 octetos...\n')

   for octeto in lstOctetos:
      if not octeto.isdigit() or not (0 <= int(octeto) <= 255):
         sys.exit('\nERRO: Cada octeto deve ser um número entre 0 e 255...\n')

   # Exibindo a lista de octetos do IP
   print(lstOctetos)  

   # Convertendo cada octeto para binário
   lstBinarios_1 = [funcoes.dec2bin(int(octeto)) for octeto in lstOctetos]
   lstBinarios_2 = [bin(int(octeto)) for octeto in lstOctetos]

   print(lstBinarios_1)
   print(lstBinarios_2)

