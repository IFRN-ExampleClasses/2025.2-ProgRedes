import sys

import funcoes


try:
   intValor = int(input('\nDigite um número inteiro: '))
except ValueError:
   sys.exit('\nERRO: Valor inválido. Por favor, insira um número inteiro...\n')
except KeyboardInterrupt:
   sys.exit('\nAVISO: Programa interrompido pelo usuário...\n')
except Exception as erro:
   sys.exit(f'\nERRO INESPERADO: {erro}...\n')
else:
   if intValor < 0:
      sys.exit('\nERRO: Por favor, insira um número inteiro não negativo...\n')

   binValor = funcoes.dec2bin(intValor)

   # Exibir a saída
   print(f'\n{intValor} em Binário....: {binValor}\n')