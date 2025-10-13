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
   
   # --- INÍCIO DA MODIFICAÇÃO 1: Variável para armazenar o offset do GPS
   gps_info_offset = None
   # --- FIM DA MODIFICAÇÃO 1 ---
   
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

      # --- INÍCIO DA MODIFICAÇÃO 2: Capturar o offset da TAG GPSInfo
      # A TAG 0x8825 (GPSInfo) contém o offset para o subdiretório de dados de GPS.
      if idTAGNumber == 0x8825:
          gps_info_offset = dataValue
      # --- FIM DA MODIFICAÇÃO 2 ---

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

   # --- INÍCIO DA MODIFICAÇÃO 3: Ler e processar os metadados de GPS ---
   lstGpsMetadata = list()
   if gps_info_offset:
      # Posiciona o cursor no início dos dados de GPS
      # O offset é relativo ao início do header TIFF (12 bytes do início do arquivo)
      fileInput.seek(gps_info_offset + 12, 0)

      # Lê a quantidade de metadados de GPS
      countGpsMetadata = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)

      # Loop para ler cada metadado de GPS
      lstGpsMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
      for _ in range(countGpsMetadata):
         idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strTagNumber     = GPS_TAG_NUMBER.get(idTAGNumber, 'Unknown GPS Tag')

         idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')

         numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         
         # O tratamento para dados ASCII ou RATIONAL (lat/long) pode ser adicionado aqui,
         # mas para este exemplo, apenas o valor/offset bruto é lido.

         lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
         lstGpsMetadata.append(dict(zip(lstGpsMetaHeader, lstTemp)))
   # --- FIM DA MODIFICAÇÃO 3 ---

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

   # --- INÍCIO DA MODIFICAÇÃO 4: Imprimir os metadados de GPS lidos ---
   if lstGpsMetadata:
      print('\n\nMetadados de GPS Lidos\n' + '-'*30)
      for metaData in lstGpsMetadata:
         print(f'{metaData}')
   else:
      print('\n\nNenhuma informação de GPS encontrada.\n' + '-'*30)
   # --- FIM DA MODIFICAÇÃO 4 ---
   
   print('\n\n')
