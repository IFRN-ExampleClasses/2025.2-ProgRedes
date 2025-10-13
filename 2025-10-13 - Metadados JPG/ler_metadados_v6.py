'''
   Lendo Metadados de Imagens JPG (EXIF)
'''
import os, sys

from metadados_funcoes import *

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
   
   # Variável para armazenar o offset do subdiretório de dados de GPS (TAG 0x8825)
   intGPSInfoOffset = None
   
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

      # A TAG 0x8825 (GPSInfo) contém o offset para o subdiretório de dados de GPS.
      if idTAGNumber == 0x8825: intGPSInfoOffset = dataValue

      # Interpretando o valor do metadado quando for ASCII
      if idDataFormat == 0x0002: 
         dataValue = lerDadosASCII(fileInput, dataValue, numberComponents, CODE_PAGE)

      lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
      lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

   # Lendo e tratando os metadados de GPS, se existirem
   lstGpsMetadata = list()
   if intGPSInfoOffset:
      # Posiciona o leitor no início do bloco de dados de GPS
      fileInput.seek(intGPSInfoOffset + 12)
      countGpsMetadata = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
      
      # ETAPA 1: Ler todas as tags de GPS do arquivo.
      # É necessário ler todas primeiro porque o tratamento de uma tag
      # (ex: GPSLatitude) depende do valor de outra (ex: GPSLatitudeRef).
      gps_data_raw = dict()
      for _ in range(countGpsMetadata):
         idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strTagNumber     = GPS_TAG_NUMBER.get(idTAGNumber, 'Unknown GPS Tag')
         idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')
         numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         
         # Decodifica valores que são ponteiros (offset)
         valor_final = dataValue
         if strDataFormat == 'ASCII String':
            valor_final = lerDadosASCII(fileInput, dataValue, numberComponents, CODE_PAGE)
         elif strDataFormat == 'Unsigned Rational':
            valor_final = lerDadosRational(fileInput, dataValue, numberComponents, strOrderByte)

         # Armazena a "peça" bruta no dicionário de apoio
         gps_data_raw[strTagNumber] = valor_final

      # ETAPA 2: Imediatamente após a leitura, tratar os dados e construir a lista final.
      # Agora que temos todas as peças, podemos combiná-las.
      lat_ref_bruto = gps_data_raw.get('GPSLatitudeRef')
      lat_val       = gps_data_raw.get('GPSLatitude')
      lon_ref_bruto = gps_data_raw.get('GPSLongitudeRef')
      lon_val       = gps_data_raw.get('GPSLongitude')
      alt_ref_val   = gps_data_raw.get('GPSAltitudeRef')
      alt_val       = gps_data_raw.get('GPSAltitude')
      timestamp     = gps_data_raw.get('GPSTimeStamp')
      datestamp     = gps_data_raw.get('GPSDateStamp')

      # Preenche a lista lstGpsMetadata diretamente com os dicionários tratados
      if lat_val:
         lat_ref = lat_ref_bruto if lat_ref_bruto in ['N', 'S'] else 'S'
         lstGpsMetadata.append({'TAGNumber': 'Latitude', 'DataValue': converterGrausDecimais(lat_val, lat_ref)})
         lstGpsMetadata.append({'TAGNumber': 'Ref. Latitude', 'DataValue': MAPEAMENTO_REF.get(lat_ref)})

      if lon_val:
          lon_ref = lon_ref_bruto if lon_ref_bruto in ['E', 'W'] else 'W'
          lstGpsMetadata.append({'TAGNumber': 'Longitude', 'DataValue': converterGrausDecimais(lon_val, lon_ref)})
          lstGpsMetadata.append({'TAGNumber': 'Ref. Longitude', 'DataValue': MAPEAMENTO_REF.get(lon_ref)})

      if alt_val:
         altitude = alt_val[0] if isinstance(alt_val, list) else alt_val
         if alt_ref_val == 1: altitude = -altitude
         lstGpsMetadata.append({'TAGNumber': 'Altitude', 'DataValue': f"{altitude:.2f} metros"})

      if timestamp and datestamp:
         hora = f"{int(timestamp[0]):02d}:{int(timestamp[1]):02d}:{int(timestamp[2]):02d} UTC"
         lstGpsMetadata.append({'TAGNumber': 'Data e Hora (UTC)', 'DataValue': f"{datestamp} {hora}"})

   # Fechando o arquivo
   fileInput.close()

   # Imprimindo os dados do cabeçalho EXIF
   print('\n\nDados do Cabeçalho EXIF\n' + '-'*30)
   for key,value in dictEXIF.items(): print(f'{key:15}: {value}')

   # Imprimindo os metadatas lidos
   print('\n\nMetadados Lidos\n' + '-'*30)
   for metaData in lstMetadata: print(f'{metaData}')

   # Imprimindo os metadados de GPS lidos
   if lstGpsMetadata:
      print('\n\nMetadados de GPS Lidos\n' + '-'*30)
      for metaData in lstGpsMetadata: print(f'{metaData}')

   print('\n\n')
