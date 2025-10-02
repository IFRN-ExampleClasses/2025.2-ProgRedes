'''
   Este script demonstra como as operações bit a bit (bitwise) podem ser 
   aplicadas a caracteres (strings).
   
   Para que isso funcione, os caracteres precisam ser convertidos em seus 
   valores numéricos correspondentes da tabela ASCII. As operações são feitas 
   nesses números, e o resultado pode ser convertido de volta para um caractere.

   - Ao executar este script, a saída será:

      Texto 1................: P -> ASCII =  80 -> 01010000
      Texto 2................: d -> ASCII = 100 -> 01100100
      ------------------------------------------------------------
      strTexto_1 & strTexto_2: ASCII =  64 -> "@" -> 01000000
      strTexto_1 | strTexto_2: ASCII = 116 -> "t" -> 01110100
      strTexto_1 ^ strTexto_2: ASCII =  52 -> "4" -> 00110100
'''

# ----------------------------------------------------------------------
# Inicialização das Variáveis de Entrada
strTexto_1 = 'P'
strTexto_2 = 'd'

# ----------------------------------------------------------------------
# Antes de operar, vamos visualizar os caracteres e seus equivalentes numéricos.
# A função `ord()` é usada para obter o código numérico (ASCII) de um caractere.
# Assim como no exemplo anterior, formatamos a saída para mostrar o valor decimal
# e sua representação binária de 8 bits.
print(f'Texto 1................: {strTexto_1} -> ASCII = {ord(strTexto_1):>3} -> {ord(strTexto_1):08b}')
print(f'Texto 2................: {strTexto_2} -> ASCII = {ord(strTexto_2):>3} -> {ord(strTexto_2):08b}')
print("-" * 60) # Imprime uma linha para separar as seções

# ----------------------------------------------------------------------
# Realizando as Operações Bitwise
# As operações bit a bit são realizadas nos valores ASCII dos caracteres,
# que foram obtidos usando a função `ord()`.

# Operação AND (&): O bit resultante é 1 se ambos os bits correspondentes forem 1.
andResultado = ord(strTexto_1) & ord(strTexto_2)
# 'P' (80) -> 01010000
# 'd' (100)-> 01100100
#             ---------
# Resultado-> 01000000 (64)

# Operação OR (|): O bit resultante é 1 se pelo menos um dos bits correspondentes for 1.
orResultado  = ord(strTexto_1) | ord(strTexto_2)
# 'P' (80) -> 01010000
# 'd' (100)-> 01100100
#             ---------
# Resultado-> 01110100 (116)

# Operação XOR (^): O bit resultante é 1 se os bits correspondentes forem diferentes.
xorResultado = ord(strTexto_1) ^ ord(strTexto_2)
# 'P' (80) -> 01010000
# 'd' (100)-> 01100100
#             ---------
# Resultado-> 00110100 (52)


# ----------------------------------------------------------------------
# Exibição dos Resultados
# Agora, vamos imprimir os resultados das operações.
# Usamos a função `chr()` para converter o código ASCII resultante de volta para um caractere.
# É importante notar que o resultado nem sempre será um caractere visível ou imprimível.
print(f'strTexto_1 & strTexto_2: ASCII = {andResultado:>3} -> "{chr(andResultado)}" -> {(andResultado):08b}')
print(f'strTexto_1 | strTexto_2: ASCII = {orResultado:>3} -> "{chr(orResultado)}" -> {(orResultado):08b}')
print(f'strTexto_1 ^ strTexto_2: ASCII = {xorResultado:>3} -> "{chr(xorResultado)}" -> {(xorResultado):08b}')