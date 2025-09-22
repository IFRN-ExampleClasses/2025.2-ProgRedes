# ----------------------------------------------------------------------
intNumeroA = 150
intNumeroB = 120

resultadoAND = intNumeroA | intNumeroB

print(f'\nNúmero A..: {bin(intNumeroA):>16} ({int(bin(intNumeroA), 2)})')
print(f'Número B..: {bin(intNumeroB):>16} ({int(bin(intNumeroB), 2)})')
print(f'AND.......: {bin(resultadoAND):>16} ({int(bin(resultadoAND), 2)})\n\n')

# ----------------------------------------------------------------------
binNumeroA = bin(intNumeroA)
binNumeroB = bin(intNumeroB)

resultadoAND = int(binNumeroA, 2) | int(binNumeroB, 2)

print(f'\nNúmero A..: {bin(intNumeroA):>16} ({int(bin(intNumeroA), 2)})')
print(f'Número B..: {bin(intNumeroB):>16} ({int(bin(intNumeroB), 2)})')
print(f'AND.......: {bin(resultadoAND):>16} ({int(bin(resultadoAND), 2)})\n\n')