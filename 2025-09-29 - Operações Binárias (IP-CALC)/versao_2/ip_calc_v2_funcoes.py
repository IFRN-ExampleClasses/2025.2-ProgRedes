import sys

# ----------------------------------------------------------------------
def validarIP(ip: str) -> bool | Exception:
   """
   Valida um endereço IPv4 no formato string 'A.B.C.D'.

      Args:
         ip (str): O endereço IP a ser validado.

      Returns:
         bool: True se o IP for válido ou uma Exception.
   """
   try:
      lstOctetos = ip.split('.')
      if len(lstOctetos) != 4: 
         raise ValueError('ERRO...: Endereço IPv4 inválido. Não possui 4 octetos')
      for octeto in lstOctetos:
         if not octeto.isdigit(): 
            raise ValueError(f'ERRO...: Endereço IPv4 inválido. Octeto \'{octeto}\' não é numérico')
         if not 0 <= int(octeto) <= 255: 
            raise ValueError(f'ERRO...: Endereço IPv4 inválido. Octeto \'{octeto}\' está fora do intervalo válido (0-255)')
   except Exception as excecao:
      raise excecao
   else:
      return True 


# ----------------------------------------------------------------------
def validarCIDR(cidr: int) -> bool | Exception:
   """
      Valida uma máscara de rede no formato CIDR.

      Args:
         cidr (int): O valor CIDR a ser validado (como inteiro).

      Returns:
         bool: True se o CIDR for válido ou uma Exception.
   """
   try:
      if not isinstance(cidr, int):
         raise TypeError('ERRO...: O CIDR deve ser um número inteiro.') 
      if not 0 <= cidr <= 32: 
         raise ValueError('ERRO...: O CIDR deve estar entre 0 e 32.')
   except Exception as excecao:
      raise excecao
   else:
      return True


# ----------------------------------------------------------------------
def classificarIP(ip: str) -> tuple:
   """
      Classifica um endereço IPv4, identificando sua classe e se pertence a
      um intervalo especial (privado, loopback, etc.).

      Args:
         ip (str): Um endereço IP válido.
   """
   lstOctetos = [int(o) for o in ip.split('.')]
    
   if lstOctetos[0] == 0:
      classe = 'Reservado (Rede Atual)'
      tipo   = 'Endereço Especial'
   elif lstOctetos[0] == 127:
      classe = 'Classe A (Endereço de Loopback)'
      tipo   = 'Endereço Especial'
   elif 1 <= lstOctetos[0] <= 126:
      classe = 'A'
      tipo   = 'Público' if lstOctetos[0] != 10 else 'Privado'
   elif 128 <= lstOctetos[0] <= 191:
      classe = 'B'
      tipo   = 'Público' if not (lstOctetos[0] == 172 and 16 <= lstOctetos[1] <= 31) else 'Privado'
   elif 192 <= lstOctetos[0] <= 223:
      classe = 'C'
      tipo   = 'Público' if not (lstOctetos[0] == 192 and lstOctetos[1] == 168) else 'Privado'
   elif 224 <= lstOctetos[0] <= 239:
      classe = 'D'
      tipo   = 'Reservado para Multicast'
   elif 240 <= lstOctetos[0] <= 255:
      classe = 'E'
      tipo   = 'Reservado para Uso Futuro/Experimental'
   else:
      classe = 'Desconhecida'
      tipo   = 'N/A' 

   return classe, tipo
