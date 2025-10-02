'''
   Este script expande a ideia anterior para aplicar operações bit a bit (bitwise) 
   entre duas strings de texto completas.

   A lógica é processar as strings caractere por caractere, em paralelo.

   Para que este código funcione corretamente, as duas strings de entrada devem 
   ter exatamente o mesmo comprimento.

   - Ao executar este script, a saída será:

      Texto 1................: Programação
      Texto 2................: desenvolver
      ------------------------------------------------------------
      Texto_1 & Texto_2......: @dos`c`a`go -> 11 caracteres
      Texto_1 | Texto_2......: uswooumuçao -> 11 caracteres
      Texto_1 ^ Texto_2......: 4sezwm}mÊ -> 11 caracteres

      
   - Note que os resultados das operações bit a bit podem incluir caracteres
     não imprimíveis ou especiais, dependendo dos valores ASCII resultantes.
'''

# ----------------------------------------------------------------------
# Inicialização das Variáveis de Entrada
strTexto_1 = 'Programação'
strTexto_2 = 'desenvolver'

print(f'Texto 1................: {strTexto_1}')
print(f'Texto 2................: {strTexto_2}')
print("-" * 60) # Imprime uma linha para separar as seções

# ----------------------------------------------------------------------
# Inicialização das Variáveis de Controle e Resultado
intPosicao      = 0
strResultadoAND = ''
strResultadoOR  = ''
strResultadoXOR = ''

# ----------------------------------------------------------------------
# Loop de Processamento
# O laço 'while' continuará executando enquanto a posição atual (intPosicao)
# for menor que o comprimento da primeira string.
while intPosicao < len(strTexto_1):
   # Dentro do loop, a cada iteração, trabalhamos com um par de caracteres:
   # um de strTexto_1 e um de strTexto_2, ambos na mesma 'intPosicao'.

   # --- Operação AND bit a bit ---
   # 1. Pegamos o caractere de cada texto na posição atual (ex: strTexto_1[0] e strTexto_2[0]).
   # 2. Convertemos ambos para seus valores ASCII usando `ord()`.
   # 3. Realizamos a operação AND (&) entre os dois números ASCII.
   # 4. O resultado numérico é convertido de volta para um caractere com `chr()`.
   # 5. O novo caractere é adicionado (concatenado) ao final da string de resultado AND.
   andResultado = ord(strTexto_1[intPosicao]) & ord(strTexto_2[intPosicao])
   strResultadoAND += chr(andResultado)

   # --- Operação OR bit a bit ---
   # O processo é o mesmo, mas agora usando o operador OR (|).
   orResultado = ord(strTexto_1[intPosicao]) | ord(strTexto_2[intPosicao])
   strResultadoOR += chr(orResultado)

   # --- Operação XOR bit a bit ---
   # O processo é o mesmo, mas agora usando o operador XOR (^).
   xorResultado = ord(strTexto_1[intPosicao]) ^ ord(strTexto_2[intPosicao])
   strResultadoXOR += chr(xorResultado)

   # --- Incremento do Contador ---
   # É FUNDAMENTAL incrementar a posição para que, na próxima iteração do loop,
   # peguemos o próximo par de caracteres. Se esquecermos esta linha, teremos um loop infinito.
   intPosicao += 1

# ----------------------------------------------------------------------
# Exibição dos Resultados Finais
# Após o loop terminar, as strings de resultado foram completamente montadas.
# Agora, exibimos cada uma delas e seu comprimento total.
print(f'Texto_1 & Texto_2......: {strResultadoAND} -> {len(strResultadoAND)} caracteres')
print(f'Texto_1 | Texto_2......: {strResultadoOR} -> {len(strResultadoOR)} caracteres')
print(f'Texto_1 ^ Texto_2......: {strResultadoXOR} -> {len(strResultadoXOR)} caracteres')