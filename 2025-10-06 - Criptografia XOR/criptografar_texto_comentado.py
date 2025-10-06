'''
   Este script demonstra uma aplicação prática das operações bit a bit:
   a criptografia de texto usando o operador XOR (^).

   A cifra XOR é simétrica, o que significa que o mesmo algoritmo (e a mesma chave)
   que criptografa o texto também o descriptografa.
'''
import os


# ----------------------------------------------------------------------
# Pede ao usuário que forneça o texto a ser criptografado.
strFrase = input('\nInforme o texto a ser criptografado: ')

# Pede ao usuário uma chave de criptografia.
# [:len(strFrase)] -> Limita o tamanho da chave para não ser maior que o texto.
# .strip() -> Remove espaços em branco do início e do fim da chave.
strChave = input('\nInforme a chave de criptografia....: ')[:len(strFrase)].strip()

print(f'\nTexto p/ criptografar.: {strFrase}')
print(f'Chave de criptografia.: {strChave}')
print("-" * 50)


# ----------------------------------------------------------------------
intPosicao       = 0
strCriptografado = ''

for intPosicao in range(len(strFrase)):
   '''
      Lógica da Chave Repetida (Repeating Key XOR)
         - Se a chave for mais curta que o texto, ela será repetida.
         - O operador de módulo (%) faz a mágica aqui: ele "reseta" o índice da chave
           de volta para 0 quando ele atinge o final.
      Exemplo: Se a chave tem 5 caracteres e estamos na posição 7 do texto,
               7 % 5 = 2. Então, usaremos o caractere da chave na posição 2.
   '''
   charChave = strChave[intPosicao % len(strChave)]   

   '''
      Operação XOR
         1. Pega o caractere da frase e o caractere correspondente da chave.
         2. Converte ambos para seus valores ASCII com `ord()`.
         3. Aplica a operação XOR (^).
         4. Converte o resultado numérico de volta para um caractere com `chr()`.
   '''
   xorResultado     = ord(strFrase[intPosicao]) ^ ord(charChave)
   strCriptografado += chr(xorResultado)


# ----------------------------------------------------------------------
'''
   Salvando o Resultado em Arquivo ===
      - O bloco 'try...except' é usado para tratamento de erros.
      - Ele tenta executar o código no bloco 'try'. Se um erro ocorrer (ex: falta de
        permissão para criar o arquivo), o programa não trava, mas executa o bloco 'except'.
'''
try:
   strDir     = os.path.dirname(__file__)
   strArquivo = os.path.join(strDir, 'texto_criptografado.txt')
   
   # Abre o arquivo em modo de escrita ('w')
   arqSaida   = open(strArquivo, 'w', encoding='utf-8')
   # Escreve a string criptografada no arquivo
   arqSaida.write(f'{strCriptografado}\n')
   # Fecha o arquivo para garantir que tudo seja salvo
   arqSaida.close()
   
   print(f'Texto criptografado com sucesso!')
   print(f'Arquivo salvo em: {strArquivo}\n')
except Exception as e:
   # Se qualquer erro (Exception) ocorrer, ele será capturado na variável 'e'
   # e uma mensagem de erro amigável será exibida.
   print(f'ERRO: Ocorreu um erro ao salvar o arquivo -> {e}\n')