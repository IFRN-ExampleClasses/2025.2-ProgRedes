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

# ----------------------------------------------------------------------
# VARIÁVEIS DE ENTRADA (Altere estes valores para testar)
strIP   = '192.168.1.10'   # Endereço IPv4 em formato string
intCIDR = 22               # Notação CIDR. Quantidade de bits '1' no início 
                           # da máscara de sub-rede

# ----------------------------------------------------------------------
# 1 - Convertendo o Endereço IPv4 e a Máscara CIDR para Binário
intIP      = int.from_bytes(bytes([int(x) for x in strIP.split('.')]), 'big')
intMascara = 0xFFFFFFFF >> (32 - intCIDR) << (32 - intCIDR)

# ----------------------------------------------------------------------
# 2 - Calculando o Endereço de Rede:
# Realizando uma operação AND bit a bit entre o endereço IPv4 e a 
# máscara de sub-rede
intIPRede = intIP & intMascara
strIPRede = '.'.join([str(x) for x in intIPRede.to_bytes(4)])

# ----------------------------------------------------------------------
# 3 - Calculando o Primeiro Host:
# O primeiro host é o endereço de rede com o último bit alterado para 1
intIPPrimeiroHost = intIPRede | 0x00000001
strIPPrimeiroHost = '.'.join([str(x) for x in intIPPrimeiroHost.to_bytes(4)])

# ----------------------------------------------------------------------
# 4 - Calculando o Endereço de Broadcast:
# O endereço de broadcast é o endereço de rede com todos os últimos n bits 
# do host alterados para 1 ('& 0xFFFFFFFF' garante que o número seja de 32 bits)
intIPBroadcast = intIPRede | (~intMascara & 0xFFFFFFFF)
strIPBroadcast = '.'.join([str(x) for x in intIPBroadcast.to_bytes(4)])

# ----------------------------------------------------------------------
# 5 - Calculando o Último Host:
# O último host é o endereço de broadcast com o último bit alterado para 0
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

# ----------------------------------------------------------------------
# Exibindo os resultados
print(f'O Endereço da Rede é (IPv4).................: {strIPRede:>15} -> {intIPRede:032b}')
print(f'O Endereço do 1º Host da Rede é (IPV4)......: {strIPPrimeiroHost:>15} -> {intIPPrimeiroHost:032b}')
print(f'O Endereço do Broadcast da Rede é (IPV4)....: {strIPBroadcast:>15} -> {intIPBroadcast:032b}')
print(f'O Endereço do Último Host da Rede é (IPV4)..: {strIPUltimoHost:>15} -> {intIPUltimoHost:032b}')
print(f'A Quantidade de Hosts Válidos na Rede é.....: {intQtHosts:>15}\n')