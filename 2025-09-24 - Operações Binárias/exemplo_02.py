'''
   Exemplo 02 - Calculando a máscara de sub-rede em formato inteiro 
   com base em um valor de CIDR (Classless Inter-Domain Routing)
'''
# Define a variável 'intCIDR' com o valor 24, 
# representando a quantidade de bits na máscara de sub-rede (CIDR)
intCIDR = 24

# Calcula a máscara de sub-rede deslocando 32 bits para a direita, 
# com base no valor de 'intCIDR'. O valor 0xFFFFFFFF tem todos os bits 
# setados como 1 (32 bits). O deslocamento à direita elimina os bits à 
# direita da máscara
intMascara = 0xFFFFFFFF >> (32 - intCIDR)

# Desloca novamente a máscara para a esquerda para restabelecer a posição 
# original dos bits. O deslocamento à esquerda garante que a máscara tenha 
# o número correto de bits à esquerda para a rede
intMascara = intMascara << (32 - intCIDR)

# Exibe o valor final da máscara de sub-rede calculada (em formato inteiro)
print(intMascara)
