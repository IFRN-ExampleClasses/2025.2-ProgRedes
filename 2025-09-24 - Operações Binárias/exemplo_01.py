'''
   Exemplo 01 - Convertendo um endereço IP em inteiro de 32 bits
'''
strIP = '192.168.1.10'
print(f'O Endereço IPv4 é.....................: {strIP}\n')

lstIP = [int(x) for x in strIP.split(".")]

print(f'Lista de inteiros (octetos)...........: {lstIP}\n')

bytesIP = bytes(lstIP)

print(f'Endereço IPv4 como bytes..............: {bytesIP}\n')

intIP = int.from_bytes(bytes(lstIP), byteorder='big')

print(f'Endereço IPv4 como inteiro ...........: {intIP}\n')

print(f'O Endereço IPv4 em binário é (32 bits): {intIP:032b}\n')  