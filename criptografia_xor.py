'''
   Programa que criptografa uma frase através da operação binária XOR 
   utilizando a chave fornecida pelo usuário.

   Case a chave seja menor que a frase, a chave será repetida até o tamanho 
   da frase.

      Exemplo:
      Frase: "Olá, tudo bem?"
      Chave: "chave"
      Frase criptografada: ","
'''
import os

# ----------------------------------------------------------------------
# Obtendo o diretório do script
strDir = os.path.dirname(__file__)

# ----------------------------------------------------------------------
# Definindo o nome dos arquivos de saída
strArquivoSaida1 = os.path.join(strDir, 'frase_criptografada.txt')
strArquivoSaida2 = os.path.join(strDir, 'frase_descriptografada.txt')

# ----------------------------------------------------------------------
# Entrada de dados
strFrase = input('Digite a frase: ')
strChave = input('Digite a chave: ')

# ----------------------------------------------------------------------
# Repetir a chave até o tamanho da frase
strChaveRepetida = ''
for i in range(len(strFrase)):
   strChaveRepetida += strChave[i % len(strChave)]

# ----------------------------------------------------------------------
# Criptografar com XOR diretamente
strFraseCriptografada = ''
for i in range(len(strFrase)):
   intXOR = ord(strFrase[i]) ^ ord(strChaveRepetida[i])
   strFraseCriptografada += chr(intXOR)
print(f'Frase Criptografada...: {strFraseCriptografada}')

with open(strArquivoSaida1, 'w', encoding='utf-8') as arqOutput:
   arqOutput.write(strFraseCriptografada)

# ----------------------------------------------------------------------
# Descriptografar com XOR novamente
strFraseDescriptografada = ''
for i in range(len(strFraseCriptografada)):
   intXOR = ord(strFraseCriptografada[i]) ^ ord(strChaveRepetida[i])
   strFraseDescriptografada += chr(intXOR)
print(f'Frase Descriptografada...: {strFraseDescriptografada}')

with open(strArquivoSaida2, 'w', encoding='utf-8') as arqOutput:
   arqOutput.write(strFraseDescriptografada)
