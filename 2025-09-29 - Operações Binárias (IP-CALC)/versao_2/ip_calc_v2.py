'''
   Script para Cálculo de Faixa de Rede IPv4

   Este script realiza uma série de cálculos de rede com base em um endereço IPv4
   e uma máscara de sub-rede no formato CIDR. Ele foi projetado para ser
   educacional, demonstrando passo a passo como os cálculos são realizados
   em nível de bits.

   Variáveis de Entrada:
      - strIP: O endereço IPv4 que será analisado (ex: '192.168.1.10').
      - intCIDR: A máscara de sub-rede no formato CIDR (ex: 24).
'''
from ip_calc_v2_funcoes import *

# ----------------------------------------------------------------------
# Informando os dados de entrada (IPv4 e CIDR) com validação
print('\n--- Cálculo de Faixa de Rede IPv4 ---\n')
while True:
   try:
      strIP   = input('Informe o Endereço IPv4 (ex: 192.168.1.10): ')
      try:
         intCIDR = int(input('Informe a Máscara de Sub-rede no formato CIDR (0-32): '))
      except ValueError:
         raise ValueError('ERRO...: O CIDR deve ser um número inteiro.')
      else:
         if validarIP(strIP) and validarCIDR(intCIDR): break
   except Exception as e:
      print(f'\n{e}.\nTente novamente...\n')
         
# ----------------------------------------------------------------------
# 1 - Convertendo o Endereço IPv4 e a Máscara CIDR para Binário
intIP      = int.from_bytes(bytes([int(x) for x in strIP.split('.')]), 'big')
intMascara = 0xFFFFFFFF >> (32 - intCIDR) << (32 - intCIDR)

# ----------------------------------------------------------------------
# 2 - Calculando o Endereço de Rede:
intIPRede = intIP & intMascara
strIPRede = '.'.join([str(x) for x in intIPRede.to_bytes(4)])

# ----------------------------------------------------------------------
# 3 - Calculando o Primeiro Host:
intIPPrimeiroHost = intIPRede | 0x00000001
strIPPrimeiroHost = '.'.join([str(x) for x in intIPPrimeiroHost.to_bytes(4)])

# ----------------------------------------------------------------------
# 4 - Calculando o Endereço de Broadcast:
intIPBroadcast = intIPRede | (~intMascara & 0xFFFFFFFF)
strIPBroadcast = '.'.join([str(x) for x in intIPBroadcast.to_bytes(4)])

# ----------------------------------------------------------------------
# 5 - Calculando o Último Host:
intIPUltimoHost = intIPBroadcast & 0xFFFFFFFE
strIPUltimoHost = '.'.join([str(x) for x in intIPUltimoHost.to_bytes(4)])

# ----------------------------------------------------------------------
# 6 - Calculando a Máscara de Sub-rede em Decimal:
strIPMascara = '.'.join([str(x) for x in intMascara.to_bytes(4)])

# ----------------------------------------------------------------------
# 7 - Calculando o Número de Hosts Válidos:
intQtHosts = 2 ** (32 - intCIDR) - 2

# ----------------------------------------------------------------------
# Exibindo os dados de entrada
print('\nRESULTADOS OBTIDOS (os IP\'s estão no formato IPV4):\n')
print(f'O Endereço é (IPV4).........................: {strIP:>15} -> {intIP:032b}')
print(f'O IP da Máscara para o CIDR /{intCIDR:<2} é...........: {strIPMascara:>15} -> {intMascara:032b}\n')

# Classificação do IP
strClasse, strTipo = classificarIP(strIP)
print(f'A Classe do Endereço IP é...................: {strClasse}')
print(f'O Tipo do Endereço IP é.....................: {strTipo}\n')

# ----------------------------------------------------------------------
# Exibindo os resultados
print(f'O Endereço da Rede é (IPv4).................: {strIPRede:>15} -> {intIPRede:032b}')
print(f'O Endereço do 1º Host da Rede é (IPV4)......: {strIPPrimeiroHost:>15} -> {intIPPrimeiroHost:032b}')
print(f'O Endereço do Broadcast da Rede é (IPV4)....: {strIPBroadcast:>15} -> {intIPBroadcast:032b}')
print(f'O Endereço do Último Host da Rede é (IPV4)..: {strIPUltimoHost:>15} -> {intIPUltimoHost:032b}')
print(f'A Quantidade de Hosts Válidos na Rede é.....: {intQtHosts:>15}\n')