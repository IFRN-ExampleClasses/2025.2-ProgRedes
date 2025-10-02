'''
   Este script realiza as mesmas operações bit a bit (bitwise) do exemplo anterior, 
   processando duas strings caractere por caractere.

   A novidade aqui é que, além de exibir os resultados no console, o script também 
   salva esses resultados em um arquivo de texto chamado 'resultado_operacoes.txt'.
'''
# ----------------------------------------------------------------------
# Importamos o módulo 'os', que fornece funções para interagir com o sistema
# operacional. Usaremos ele para manipular caminhos de arquivos de forma segura.
import os

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


# ----------------------------------------------------------------------
# Escrita dos Resultados em um Arquivo

# 1. Montando o caminho do arquivo de saída
# os.path.dirname(__file__) obtém o caminho da pasta onde este script está salvo.
strDir = os.path.dirname(__file__)

# os.path.join() junta o caminho da pasta com o nome do arquivo. É a forma mais
# segura de criar caminhos, pois funciona em qualquer sistema operacional (Windows, Linux, Mac).
strArquivo = os.path.join(strDir, 'resultado_operacoes.txt')

# 2. Abrindo o arquivo para escrita
# A função open() abre um arquivo.
# 'w' é o modo de "escrita" (write). Ele cria o arquivo se não existir ou apaga
# todo o conteúdo de um arquivo existente para escrever do zero.
# 'encoding="utf-8"' garante que caracteres especiais (como acentos) sejam salvos corretamente.
arqSaida = open(strArquivo, 'w', encoding='utf-8')

# 3. Escrevendo os dados no arquivo
# O método .write() escreve o texto fornecido dentro do arquivo.
# Usamos '\n' para indicar uma quebra de linha (para pular para a próxima linha).
arqSaida.write('Resultados das operações bit a bit (bitwise) com strings\n\n')
arqSaida.write(f'Texto 1................: {strTexto_1}\n')
arqSaida.write(f'Texto 2................: {strTexto_2}\n\n\n')
arqSaida.write(f'Texto_1 & Texto_2......: {strResultadoAND}\n')
arqSaida.write(f'Texto_1 | Texto_2......: {strResultadoOR}\n')
arqSaida.write(f'Texto_1 ^ Texto_2......: {strResultadoXOR}\n')

# 4. Fechando o arquivo
# É uma prática essencial fechar o arquivo com .close() após terminar de usá-lo.
# Isso garante que todas as informações sejam salvas no disco e libera o arquivo.
arqSaida.close()