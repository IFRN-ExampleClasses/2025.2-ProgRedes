'''
   Lendo Metadados de Imagens JPG (EXIF)
'''
import os, sys

from metadados_contantes import *

# ------------------------------------------------------------------------------------------
# Variáveis e Constantes
DIR_APP    = os.path.dirname(__file__)
DIR_IMG    = f'{DIR_APP}\\imagens'
CODE_PAGE  = 'utf-8'  # Página de Código para Decodificação dos Metadados (ASCII)
strNomeArq = f'{DIR_IMG}\\presepio_natalino.jpg'


# ------------------------------------------------------------------------------------------
try:
   fileInput = open(strNomeArq, 'rb')
except FileNotFoundError:
   sys.exit('\nERRO: Arquivo Não Existe...\n')
except Exception as erro:
   sys.exit(f'\nERRO: {erro}...\n')
else:
   # Verificando se o arquivo informado é JPG 
   if fileInput.read(2) != b'\xFF\xD8':
      fileInput.close()
      sys.exit('\nERRO: Arquivo informado não é JPG...\n')

   # Verifica se o arquivo possui metadados
   if fileInput.read(2) != b'\xFF\xE1':
      fileInput.close()
      sys.exit('\nAVISO: Este arquivo não possui metadados...\n')

   # Obtendo o header do EXIF
   exifSize      = fileInput.read(2)
   exifHeader    = fileInput.read(4) # EXIF Header (marcador EXIF)
   temp1         = fileInput.read(2) # EXIF Header (fixo)
   endianHeader  = fileInput.read(2) # Endian do arquivo (Big ou Little)
   temp2         = fileInput.read(2) # TIFF Header (fixo)
   temp3         = fileInput.read(4) # TIFF Header (fixo)
   countMetadata = fileInput.read(2) # Metadata Count

   # Verificando o Endian do arquivo
   # (49 49: Little Endian - Intel / 4D 4D: Big Endian - Motorola)
   strOrderByte  = 'little' if endianHeader == b'\x49\x49' else 'big'
   exifSize      = int.from_bytes(exifSize, byteorder=strOrderByte)
   countMetadata = int.from_bytes(countMetadata, byteorder=strOrderByte)

   # Montando o dicionário do header do  EXIF
   dictEXIF = { 'exifSize' : exifSize     , 'exifMarker': exifHeader, 
                'temp1'    : temp1        , 'tiffHeader': endianHeader, 
                'temp2'    : temp2        , 'temp3'     : temp3     ,
                'metaCount': countMetadata }

   # Obtendo os Metadados
   lstMetadata   = list()
   lstMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
   for _ in range(countMetadata):
      # Identificador do Metadado
      idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      strTagNumber     = TAG_NUMBER.get(idTAGNumber, 'Unknown Tag')
      
      # Formato do Metadado
      idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')

      # Número de Componentes do Metadado
      numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte) 

      # Valor do Metadado (ou Offset quando o formato do metadado for ASCII)      
      dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte) 

      if idDataFormat == 0x0002: # Formato ASCII
         # Guardar a posição atual no arquivo
         current_position = fileInput.tell()
         # Fazer o fileInput.seek() para ler o valor real (offset)
         fileInput.seek(dataValue + 12, 0)
         dataValue = fileInput.read(numberComponents).decode(CODE_PAGE).rstrip('\x00')
         # Retornar à posição original
         fileInput.seek(current_position) 

      lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
      lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

   # Fechando o arquivo
   fileInput.close()

   # Imprimindo os dados do cabeçalho EXIF
   print('\n\nDados do Cabeçalho EXIF\n' + '-'*30)
   for key,value in dictEXIF.items(): 
      print(f'{key:15}: {value}')

   # Imprimindo os metadatas lidos
   print('\n\nMetadados Lidos\n' + '-'*30)
   for metaData in lstMetadata:
      print(f'{metaData}')

   print('\n\n')
