'''
   Exemplo 03 -  Calculando do endereço de rede a partir de um IP e CIDR
'''
strIP   = '192.168.1.10'
print(f'O Endereço IPv4 é...........................: {strIP}\n')

intCIDR = 24
print(f'Valor CIDR (bits na máscara)................: /{intCIDR}\n')

intIP      = int.from_bytes(bytes([int(x) for x in strIP.split('.')]), 'big')
print(f'O Endereço IPv4 em binário é (32 bits)......: {intIP:032b}\n')  

intMascara = 0xFFFFFFFF >> (32 - intCIDR) << (32 - intCIDR)
print(f'Máscara de sub-rede em binário é (32 bits)..: {intMascara:032b}\n')  

intIPRede  = intIP & intMascara
print(f'Endereço IPv4 da Rede em binário é (32 bits): {intIPRede:032b}\n')  

strIPRede = '.'.join([str(x) for x in intIPRede.to_bytes(4)])
print(f'O Endereço IPv4 da Rede é...................: {strIPRede}\n')
