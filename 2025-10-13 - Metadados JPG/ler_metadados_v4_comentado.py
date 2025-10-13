'''
   Lendo Metadados de Imagens JPG (EXIF)
   --------------------------------------
   Este script foi projetado para ler e interpretar os metadados EXIF (Exchangeable image file format)
   contidos em um arquivo de imagem no formato JPEG (.jpg). Ele faz isso abrindo o arquivo em modo
   binário e lendo os bytes de acordo com a especificação do formato EXIF, que é embutido dentro
   da estrutura do arquivo JPEG.
'''
import os
import sys

# Supondo que o arquivo metadados_contantes.py exista e contenha os dicionários
# TAG_NUMBER e DATA_FORMAT, que mapeiam os códigos numéricos dos metadados para
# nomes e tipos legíveis por humanos.
# Exemplo de metadados_contantes.py:
# TAG_NUMBER = { 0x0110: 'Model', 0x010F: 'Make', ... }
# DATA_FORMAT = { 1: 'unsigned byte', 2: 'ascii string', ... }
from metadados_contantes import *

# ------------------------------------------------------------------------------------------
# Variáveis e Constantes Globais

# Obtém o caminho absoluto do diretório onde este script está localizado.
# __file__ é uma variável especial do Python que contém o caminho para o arquivo atual.
DIR_APP = os.path.dirname(__file__)

# Define o diretório onde as imagens a serem analisadas estão localizadas.
# Ele é construído a partir do diretório do script, garantindo que funcione em qualquer sistema.
DIR_IMG = f'{DIR_APP}\\imagens'

# Define a página de código (encoding) para decodificar os metadados de texto.
# UTF-8 é um padrão comum e flexível para lidar com caracteres de texto.
CODE_PAGE = 'utf-8'

# Define o nome e o caminho completo do arquivo de imagem que será analisado.
caminho_arquivo_imagem = f'{DIR_IMG}\\presepio_natalino.jpg'


# ------------------------------------------------------------------------------------------
# O bloco try...except...else é usado para tratar possíveis erros de forma elegante.
try:
   # Tenta abrir o arquivo de imagem especificado em modo de leitura binária ('rb').
   # O modo binário é essencial porque precisamos ler os bytes exatos do arquivo,
   # sem qualquer interpretação ou conversão de caracteres.
   fileInput = open(caminho_arquivo_imagem, 'rb')

except FileNotFoundError:
   # Se o arquivo não for encontrado no caminho especificado, o programa é encerrado
   # com uma mensagem de erro clara.
   sys.exit('\nERRO: Arquivo Não Existe...\n')

except Exception as erro:
   # Captura qualquer outra exceção que possa ocorrer ao tentar abrir o arquivo
   # e encerra o programa, exibindo o erro.
   sys.exit(f'\nERRO: {erro}...\n')

else:
   # Este bloco 'else' só é executado se o 'try' for bem-sucedido (ou seja, o arquivo foi aberto).

   # --- PASSO 1: VERIFICAÇÃO DO FORMATO DO ARQUIVO ---

   # Lê os 2 primeiros bytes do arquivo. Em um arquivo JPG válido, esses bytes
   # devem ser sempre 0xFFD8, que é o marcador "Start of Image" (SOI).
   if fileInput.read(2) != b'\xFF\xD8':
      fileInput.close() # Garante que o arquivo seja fechado antes de sair.
      sys.exit('\nERRO: Arquivo informado não é JPG...\n')

   # Lê os 2 bytes seguintes. Para arquivos com metadados EXIF, esperamos o marcador
   # 0xFFE1, conhecido como "APP1". É neste segmento que os dados EXIF são armazenados.
   if fileInput.read(2) != b'\xFF\xE1':
      fileInput.close()
      sys.exit('\nAVISO: Este arquivo não possui metadados EXIF...\n')

   # --- PASSO 2: LEITURA DO CABEÇALHO EXIF ---

   # Os próximos bytes formam o cabeçalho EXIF, que por sua vez contém um cabeçalho TIFF.
   # Esta estrutura define como os metadados estão organizados.

   # Tamanho do segmento EXIF (não incluindo os 2 bytes do marcador APP1 e estes 2 bytes de tamanho).
   exifSize = fileInput.read(2)
   # Marcador "Exif" seguido por dois bytes nulos (0x0000), confirmando que é um bloco EXIF.
   exifHeader = fileInput.read(4) # Deverá ser b'Exif'
   temp1 = fileInput.read(2)      # Deverá ser b'\x00\x00'

   # --- Início do Cabeçalho TIFF ---
   # O padrão EXIF utiliza a estrutura do formato TIFF para armazenar os metadados.

   # Endianness: Ordem dos bytes. Determina como números com mais de um byte são lidos.
   # b'\x49\x49' ("II") -> Little Endian (usado pela Intel). Ex: 0x1234 é lido como 34 12.
   # b'\x4D\x4D' ("MM") -> Big Endian (usado pela Motorola). Ex: 0x1234 é lido como 12 34.
   endianHeader = fileInput.read(2)

   # Bytes fixos que fazem parte da especificação TIFF.
   temp2 = fileInput.read(2) # Versão do TIFF, geralmente 0x002A.
   temp3 = fileInput.read(4) # Offset para o primeiro diretório de metadados (IFD - Image File Directory).

   # Número de entradas de metadados (tags) que estão neste primeiro diretório.
   countMetadata = fileInput.read(2)

   # --- PASSO 3: INTERPRETAÇÃO DO CABEÇALHO ---

   # Verifica a ordem dos bytes (Endianness) e define uma string para usar nas conversões.
   # Esta etapa é CRUCIAL para ler corretamente os números do restante do arquivo.
   strOrderByte = 'little' if endianHeader == b'\x49\x49' else 'big'

   # Agora que sabemos a ordem dos bytes, podemos converter os valores que lemos para inteiros.
   exifSize = int.from_bytes(exifSize, byteorder=strOrderByte)
   countMetadata = int.from_bytes(countMetadata, byteorder=strOrderByte)

   # Armazena as informações do cabeçalho em um dicionário para fácil visualização.
   dictEXIF = { 'exifSize' : exifSize, 'exifMarker': exifHeader,
                'padding'  : temp1, 'endian'    : endianHeader,
                'tiffVersion': temp2, 'ifdOffset' : temp3,
                'metaCount': countMetadata }

   # --- PASSO 4: LEITURA DOS METADADOS (TAGS) ---

   lstMetadata = list()
   lstMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']

   # Itera sobre o número de metadados que foi identificado no cabeçalho.
   for _ in range(countMetadata):
      # Cada entrada de metadado (tag) no diretório (IFD) tem 12 bytes de comprimento.

      # Bytes 0-1: O número da TAG (identificador do metadado). Ex: 0x0110 para "Modelo da Câmera".
      idTAGNumber = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
      # Usa o dicionário do arquivo 'metadados_contantes' para obter o nome legível da TAG.
      strTagNumber = TAG_NUMBER.get(idTAGNumber, 'Unknown Tag')

      # Bytes 2-3: O formato do dado. Ex: 2 para string ASCII, 3 para inteiro curto.
      idDataFormat = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
      strDataFormat = DATA_FORMAT.get(idDataFormat, 'Unknown Format')

      # Bytes 4-7: O número de componentes. Para uma string, é o número de caracteres.
      numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)

      # Bytes 8-11: O valor do dado OU um offset (ponteiro) para a localização do dado.
      # Se o dado couber em 4 bytes, ele é armazenado aqui.
      # Se for maior (como uma string longa), aqui fica um endereço (offset) para onde o dado está.
      dataValue = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)

      # --- TRATAMENTO ESPECIAL PARA STRINGS ASCII (Formato 2) ---
      # Strings geralmente são maiores que 4 bytes.
      if idDataFormat == 0x0002:
         # Salva a posição atual do leitor no arquivo. Precisamos voltar aqui depois.
         current_position = fileInput.tell()

         # O 'dataValue' é um offset relativo ao início do cabeçalho TIFF.
         # O cabeçalho TIFF começa 12 bytes após o início do arquivo (após 0xFFD8, 0xFFE1, tamanho, 'Exif\0\0').
         # Então, pulamos para a localização absoluta do dado no arquivo.
         fileInput.seek(dataValue + 12, 0) # O '0' significa que o seek é a partir do início do arquivo.

         # Lê o número de bytes correspondente ao tamanho da string.
         # Decodifica os bytes para uma string usando a página de código definida.
         # .rstrip('\x00') remove quaisquer caracteres nulos que possam estar no final.
         dataValue = fileInput.read(numberComponents).decode(CODE_PAGE).rstrip('\x00')

         # Retorna o leitor para a posição onde ele estava, para que possa ler a próxima tag.
         fileInput.seek(current_position)

      # Cria uma lista temporária com os dados da tag e a adiciona à lista principal de metadados.
      lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
      lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

   # --- PASSO 5: FINALIZAÇÃO E EXIBIÇÃO ---

   # Fecha o arquivo para liberar os recursos do sistema.
   fileInput.close()

   # Imprime os dados do cabeçalho EXIF que foram lidos e interpretados.
   print('\n\nDados do Cabeçalho EXIF\n' + '-'*30)
   for key,value in dictEXIF.items():
      print(f'{key:15}: {value}')

   # Imprime cada metadado encontrado, de forma organizada.
   print('\n\nMetadados Lidos\n' + '-'*30)
   for metaData in lstMetadata:
      print(f'{metaData}')

   print('\n\n')