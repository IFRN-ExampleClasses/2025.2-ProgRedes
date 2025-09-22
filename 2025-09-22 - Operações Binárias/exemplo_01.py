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
   # Imprimir o valor binário do número inteiro
   print(f'\n{intValor} em Binário....: {bin(intValor)}')

   # Imprimir o valor hexadecimal do número inteiro
   print(f'{intValor} em Hexadecimal: {hex(intValor)}')  

   # Imprimir o valor octal do número inteiro
   print(f'{intValor} em Octal......: {oct(intValor)}\n')