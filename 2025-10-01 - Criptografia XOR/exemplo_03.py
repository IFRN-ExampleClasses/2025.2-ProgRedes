# Operações bit a bit (bitwise) com strings em Python
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