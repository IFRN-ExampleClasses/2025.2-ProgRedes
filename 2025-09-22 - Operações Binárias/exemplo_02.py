import sys

try:
   intValor = int(input('\nDigite um número inteiro: '))
except ValueError:
   sys.exit('Valor inválido. Por favor, insira um número inteiro.')
except KeyboardInterrupt:
   sys.exit('\nPrograma interrompido pelo usuário.')
except Exception as erro:
   sys.exit(f'Erro inesperado: {erro}')
else:
   if intValor < 0:
      sys.exit('Por favor, insira um número inteiro não negativo.')

   # Calcular quantos bits são necessários para representar o número
   intQtBits = intValor.bit_length()

   # Converter para binário e remover o prefixo '0b'
   binValor = bin(intValor)[2:]  

   if len(binValor) % 8 != 0:
      # Calcular quantos zeros são necessários para completar o byte
      intZeros = 8 - len(binValor) % 8

      # Adicionar os zeros à esquerda
      binValor = ('0' * intZeros) + binValor

   # Exibir a saída
   print(f'\n{intValor} em Binário....: 0b{binValor}\n')