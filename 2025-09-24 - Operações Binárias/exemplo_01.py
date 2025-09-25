'''
   Exemplo 01 - Convertendo um endereço IP em inteiro de 32 bits
'''
# Define a variável 'strIP' com o endereço IP como uma string 
# (formato 'xxx.xxx.xxx.xxx')
strIP = '192.168.1.10'
print(f'O Endereço IPv4 é.....................: {strIP}\n')

# Converte o endereço IP de string para uma lista de inteiros, 
# dividindo a string pelos pontos (".") e convertendo cada parte 
# para um inteiro
lstIP = [int(x) for x in strIP.split(".")]

# Exibe a lista de inteiros que representa o endereço IP
print(f'Lista de inteiros (octetos)...........: {lstIP}\n')

# Converte a lista de inteiros (que representam os octetos do IP) 
# para uma sequência de bytes. A função 'bytes()' cria um objeto 
# bytes a partir da lista de inteiros
bytesIP = bytes(lstIP)

# Exibe o endereço IP como uma sequência de bytes
print(f'Endereço IPv4 como bytes..............: {bytesIP}\n')

# Converte a sequência de bytes de volta para um inteiro, utilizando 
# a ordem de bytes 'big-endian'. A ordem 'big-endian' significa que o byte 
# mais significativo (MSB) é armazenado primeiro (no início), ou seja, o 
# byte mais à esquerda é o de maior valor. A função 'int.from_bytes()' 
# converte a sequência de bytes em um número inteiro, respeitando essa 
# ordem de bytes.
intIP = int.from_bytes(bytes(lstIP), byteorder='big')

# Exibe o endereço IP como um número inteiro
print(f'Endereço IPv4 como inteiro ...........: {intIP}\n')

# Exibe o número inteiro em formato binário, com 32 bits, preenchido com 
# zeros à esquerda
print(f'O Endereço IPv4 em binário é (32 bits): {intIP:032b}\n')  