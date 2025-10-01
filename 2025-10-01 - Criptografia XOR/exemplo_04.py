# Operações bit a bit (bitwise) com strings em Python
import os

strTexto_1 = 'Programação'
strTexto_2 = 'desenvolver'

print(f'Texto 1................: {strTexto_1}')
print(f'Texto 2................: {strTexto_2}')

intPosicao      = 0
strResultadoAND = ''
strResultadoOR  = ''
strResultadoXOR = ''

while intPosicao < len(strTexto_1):
   # Operação AND bit a bit
   andResultado = ord(strTexto_1[intPosicao]) & ord(strTexto_2[intPosicao]) 
   strResultadoAND += chr(andResultado)

   # Operação OR bit a bit
   orResultado = ord(strTexto_1[intPosicao]) | ord(strTexto_2[intPosicao]) 
   strResultadoOR += chr(orResultado)

   # Operação XOR bit a bit
   xorResultado = ord(strTexto_1[intPosicao]) ^ ord(strTexto_2[intPosicao])
   strResultadoXOR += chr(xorResultado)

   # Incrementa a posição
   intPosicao += 1

# Exibe os resultados
print(f'Texto_1 & Texto_2......: {strResultadoAND} -> {len(strResultadoAND)} caracteres')
print(f'Texto_1 | Texto_2......: {strResultadoOR} -> {len(strResultadoOR)} caracteres')
print(f'Texto_1 ^ Texto_2......: {strResultadoXOR} -> {len(strResultadoXOR)} caracteres')

# Escrevendo em um arquivo
strDir = os.path.dirname(__file__)
strArquivo = os.path.join(strDir, 'resultado_operacoes.txt')
arqSaida   = open(strArquivo, 'w', encoding='utf-8')
arqSaida.write('Resultados das operações bit a bit (bitwise) com strings\n\n')
arqSaida.write(f'Texto 1................: {strTexto_1}\n')
arqSaida.write(f'Texto 2................: {strTexto_2}\n\n\n')
arqSaida.write(f'Texto_1 & Texto_2......: {strResultadoAND}\n')
arqSaida.write(f'Texto_1 | Texto_2......: {strResultadoOR}\n')
arqSaida.write(f'Texto_1 ^ Texto_2......: {strResultadoXOR}\n')
arqSaida.close()
