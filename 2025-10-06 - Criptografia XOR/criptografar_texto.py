# Operações bit a bit (bitwise) com strings em Python
import os

strFrase = input('\nInforme o texto a ser criptografado: ')

strChave = input('\nInforme a chave de criptografia....: ')[:len(strFrase)].strip()

print(f'Texto p/ criptografar.: {strFrase}')
print(f'Chave de criptografia.: {strChave}')

intPosicao       = 0
strCriptografado = ''

for intPosicao in range(len(strFrase)):
   # Pega o caractere da chave, repetindo-a se for menor que o texto
   # O operador de módulo (%) garante que o índice sempre esteja dentro dos limites da chave
   charChave = strChave[intPosicao % len(strChave)]   

   xorResultado     = ord(strFrase[intPosicao]) ^ ord(charChave)
   strCriptografado += chr(xorResultado)

# Escrevendo em um arquivo
try:
   strDir     = os.path.dirname(__file__)
   strArquivo = os.path.join(strDir, 'texto_criptografado.txt')
   arqSaida   = open(strArquivo, 'w', encoding='utf-8')
   arqSaida.write(f'{strCriptografado}\n')
   arqSaida.close()
   print(f'Arquivo salvo em: {strArquivo}\n')
except Exception as e:
   print(f'ERRO: Ocorreu um erro ao salvar o arquivo -> {e}\n')
