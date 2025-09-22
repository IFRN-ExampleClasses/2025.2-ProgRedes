# ----------------------------------------------------------------------
def dec2bin(numero: int) -> str:
   """Converte um número decimal para binário, retornando uma string
   com o valor binário completo em bytes (8 bits).

   Args:
      numero (int): Número decimal a ser convertido.

   Returns:
      str: Representação binária do número em bytes.
   """
   if not isinstance(numero, int):
      raise TypeError('\nERRO: O valor deve ser um número inteiro...\n')
   
   if numero < 0:
      raise ValueError('\nERRO: Número deve ser não negativo...\n')

   # Converter para binário e remover o prefixo '0b'
   binRetorno = bin(numero)[2:]  

   if len(binRetorno) % 8 != 0:
      # Calcular quantos zeros são necessários para completar o byte
      intZeros = 8 - len(binRetorno) % 8

      # Adicionar os zeros à esquerda
      binRetorno = '0b' + ('0' * intZeros) + binRetorno

   return binRetorno
# ----------------------------------------------------------------------

