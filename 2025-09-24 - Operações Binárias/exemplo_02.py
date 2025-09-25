'''
   Exemplo 02 - Calculando a máscara de sub-rede em formato inteiro 
   com base em um valor de CIDR (Classless Inter-Domain Routing)
'''
intCIDR = 24
print(f'Valor CIDR (bits na máscara)..............: /{intCIDR}\n')

intMascara = 0xFFFFFFFF >> (32 - intCIDR)

intMascara = intMascara << (32 - intCIDR)

print(f'Máscara de sub-rede como inteiro..........: {intMascara}\n')

print(f'Máscara de sub-rede em binário é (32 bits): {intMascara:032b}\n')  