# Operações bit a bit (bitwise) com strings em Python
strTexto_1 = 'P'
strTexto_2 = 'd'

print(f'Texto 1................: {strTexto_1} -> ASCII = {ord(strTexto_1):>3} -> {ord(strTexto_1):08b}')
print(f'Texto 2................: {strTexto_2} -> ASCII = {ord(strTexto_2):>3} -> {ord(strTexto_2):08b}')

# Operação AND bit a bit
andResultado = ord(strTexto_1) & ord(strTexto_2) # Operação AND bit a bit
orResultado  = ord(strTexto_1) | ord(strTexto_2) # Operação OR bit a bit
xorResultado = ord(strTexto_1) ^ ord(strTexto_2) # Operação XOR bit a bit

print(f'strTexto_1 & strTexto_2: ACSII = {andResultado:>3} -> {chr(andResultado)} -> {(andResultado):08b}')
print(f'strTexto_1 | strTexto_2: ACSII = {orResultado:>3} -> {chr(orResultado)} -> {(orResultado):08b}')
print(f'strTexto_1 ^ strTexto_2: ACSII = {xorResultado:>3} -> {chr(xorResultado)} -> {(xorResultado):08b}')