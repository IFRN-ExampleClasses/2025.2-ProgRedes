'''
   Este script demonstra as operações bit a bit (bitwise) básicas em Python.
   As operações bitwise atuam diretamente nos bits (0s e 1s) dos números.
   Para entender melhor, vamos visualizar os números em suas formas binárias.


   - Ao executar este script, a saída será:

      Valor 1................: 195 -> 11000011 (Binário)
      Valor 2................:  89 -> 01011001 (Binário)

      --- Operações Bitwise ---
      intValor_1 & intValor_2:  65 -> 01000001 (Resultado de AND)
      intValor_1 | intValor_2: 219 -> 11011011 (Resultado de OR)
      intValor_1 ^ intValor_2: 154 -> 10011010 (Resultado de XOR)
'''

# ----------------------------------------------------------------------
# Inicialização das Variáveis
intValor_1 = 195
intValor_2 = 89

# ----------------------------------------------------------------------
# As linhas abaixo imprimem os valores originais em formato decimal e binário.
# A formatação `:>3` alinha o número decimal à direita em um espaço de 3 caracteres.
# A formatação `:08b` converte o número para binário e o preenche com zeros
# à esquerda até que tenha 8 dígitos, facilitando a comparação visual.
print(f'Valor 1................: {intValor_1:>3} -> {intValor_1:08b} (Binário)')
print(f'Valor 2................: {intValor_2:>3} -> {intValor_2:08b} (Binário)')

# Adiciona uma linha em branco para melhor organização da saída.
print('\n--- Operações Bitwise ---')

# ----------------------------------------------------------------------
# Operador AND (&)
# O operador AND bit a bit compara cada par de bits correspondentes (um de cada número).
# O bit resultante será 1 SOMENTE SE ambos os bits comparados forem 1.
# Exemplo:
#   11000011  (195)
# & 01011001  (89)
#   --------
#   01000001  (65)
print(f'intValor_1 & intValor_2: {intValor_1 & intValor_2:>3} -> {(intValor_1 & intValor_2):08b} (Resultado de AND)')

# ----------------------------------------------------------------------
# Operador OR (|)
# O operador OR bit a bit compara cada par de bits correspondentes.
# O bit resultante será 1 SE PELO MENOS UM dos bits comparados for 1.
# Exemplo:
#   11000011  (195)
# | 01011001  (89)
#   --------
#   11011011  (219)
print(f'intValor_1 | intValor_2: {intValor_1 | intValor_2:>3} -> {(intValor_1 | intValor_2):08b} (Resultado de OR)')

# ----------------------------------------------------------------------
# Operador XOR (^)
# O operador XOR (OU Exclusivo) bit a bit compara cada par de bits correspondentes.
# O bit resultante será 1 SOMENTE SE os bits comparados forem DIFERENTES um do outro.
# Exemplo:
#   11000011  (195)
# ^ 01011001  (89)
#   --------
#   10011010  (154)
print(f'intValor_1 ^ intValor_2: {intValor_1 ^ intValor_2:>3} -> {(intValor_1 ^ intValor_2):08b} (Resultado de XOR)')