'''
   Lendo Metadados de Imagens JPG (EXIF)
   --------------------------------------
   Este script lê e interpreta os metadados EXIF de um arquivo de imagem JPEG.
   Esta versão foi modificada para identificar e ler o subdiretório de metadados
   de GPS, que não está no bloco principal de metadados, mas em uma área separada
   apontada por uma tag específica (0x8825).
'''
import os
import sys

# Supondo a existência de metadados_contantes.py com os dicionários:
# TAG_NUMBER: Mapeia tags do diretório principal (ex: {0x0110: 'Model'}).
# GPS_TAG_NUMBER: Mapeia tags do subdiretório de GPS (ex: {0x0002: 'GPSLatitude'}).
# DATA_FORMAT: Mapeia formatos de dados (ex: {2: 'ASCII String'}).
from metadados_contantes import *

# ------------------------------------------------------------------------------------------
# Variáveis e Constantes
DIR_APP    = os.path.dirname(__file__)
DIR_IMG    = f'{DIR_APP}\\imagens'
CODE_PAGE  = 'utf-8'  # Página de Código para Decodificação dos Metadados (ASCII)
strNomeArq = f'{DIR_IMG}\\presepio_natalino.jpg'


# ------------------------------------------------------------------------------------------
try:
   # Abre o arquivo em modo de leitura binária ('rb')
   fileInput = open(strNomeArq, 'rb')
except FileNotFoundError:
   sys.exit('\nERRO: Arquivo Não Existe...\n')
except Exception as erro:
   sys.exit(f'\nERRO: {erro}...\n')
else:
   # --- PASSO 1: VERIFICAÇÃO DO FORMATO DO ARQUIVO E EXISTÊNCIA DE METADADOS ---

   # Verifica se é um arquivo JPG (deve começar com 0xFFD8)
   if fileInput.read(2) != b'\xFF\xD8':
      fileInput.close()
      sys.exit('\nERRO: Arquivo informado não é JPG...\n')

   # Verifica se possui um segmento APP1, onde os metadados EXIF são armazenados (marcador 0xFFE1)
   if fileInput.read(2) != b'\xFF\xE1':
      fileInput.close()
      sys.exit('\nAVISO: Este arquivo não possui metadados EXIF...\n')

   # --- PASSO 2: LEITURA E INTERPRETAÇÃO DO CABEÇALHO EXIF/TIFF ---

   # Lê os componentes do cabeçalho EXIF
   exifSize      = fileInput.read(2) # Tamanho do segmento EXIF
   exifHeader    = fileInput.read(4) # Marcador "Exif\0\0"
   temp1         = fileInput.read(2) # Preenchimento
   
   # Início do Cabeçalho TIFF
   endianHeader  = fileInput.read(2) # Ordem dos bytes (Endianness)
   temp2         = fileInput.read(2) # Versão do TIFF (fixo 0x002A)
   temp3         = fileInput.read(4) # Offset para o primeiro diretório de metadados (IFD0)
   countMetadata = fileInput.read(2) # Quantidade de metadados no diretório principal

   # Determina a ordem dos bytes ('little' ou 'big') para ler números corretamente
   strOrderByte  = 'little' if endianHeader == b'\x49\x49' else 'big'
   # Converte os valores lidos para inteiros usando a ordem de bytes correta
   exifSize      = int.from_bytes(exifSize, byteorder=strOrderByte)
   countMetadata = int.from_bytes(countMetadata, byteorder=strOrderByte)

   # Armazena as informações do cabeçalho em um dicionário para exibição
   dictEXIF = { 'exifSize' : exifSize, 'exifMarker': exifHeader, 
                'padding'  : temp1, 'endian'    : endianHeader, 
                'tiffVersion': temp2, 'ifdOffset' : temp3,
                'metaCount': countMetadata }
   
   # --- INÍCIO DA MODIFICAÇÃO 1 ---
   # Variável para armazenar o endereço (offset) do subdiretório de dados de GPS.
   # A tag 0x8825 não contém os dados de GPS em si, mas sim um ponteiro para eles.
   # Inicializamos com None. Se após lermos todas as tags principais ela continuar
   # como None, significa que a imagem não tem informações de GPS.
   gps_info_offset = None
   # --- FIM DA MODIFICAÇÃO 1 ---
   
   # --- PASSO 3: LEITURA DO DIRETÓRIO PRINCIPAL DE METADADOS (IFD0) ---
   lstMetadata   = list()
   lstMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
   for _ in range(countMetadata):
      # Cada entrada de metadado (tag) tem 12 bytes.
      idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      strTagNumber     = TAG_NUMBER.get(idTAGNumber, 'Unknown Tag')
      
      idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')

      numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte) 

      # Este campo pode conter o valor do dado (se couber em 4 bytes) ou um
      # ponteiro (offset) para a localização real do dado.
      dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte) 

      # --- INÍCIO DA MODIFICAÇÃO 2: Capturar o offset da TAG GPSInfo ---
      # A tag com ID 0x8825 (GPSInfo) é especial. Seu valor é sempre um offset
      # que aponta para o início de um subdiretório contendo apenas tags de GPS.
      if idTAGNumber == 0x8825:
          gps_info_offset = dataValue
      # --- FIM DA MODIFICAÇÃO 2 ---

      # Se o formato for ASCII (string), o `dataValue` é um offset.
      if idDataFormat == 0x0002:
         # Salva a posição atual do leitor
         current_position = fileInput.tell()
         # Pula para o local onde a string está armazenada
         # O offset é relativo ao início do header TIFF (+12 bytes)
         fileInput.seek(dataValue + 12, 0)
         # Lê e decodifica a string, removendo caracteres nulos no final
         dataValue = fileInput.read(numberComponents).decode(CODE_PAGE).rstrip('\x00')
         # Retorna o leitor para a posição original para ler a próxima tag
         fileInput.seek(current_position) 

      lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
      lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

   # --- INÍCIO DA MODIFICAÇÃO 3: Ler e processar os metadados de GPS ---
   lstGpsMetadata = list()
   # Este bloco só será executado se a tag GPSInfo (0x8825) foi encontrada no passo anterior.
   if gps_info_offset:
      # Move o leitor do arquivo para o início do bloco de dados de GPS,
      # usando o offset que guardamos. O ajuste de '+ 12' é necessário porque
      # o offset é relativo ao início do cabeçalho TIFF.
      fileInput.seek(gps_info_offset + 12, 0)

      # O subdiretório de GPS tem a mesma estrutura: primeiro, lemos a quantidade
      # de tags de GPS que ele contém.
      countGpsMetadata = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)

      # Loop para ler cada metadado de GPS.
      lstGpsMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
      for _ in range(countGpsMetadata):
         # O processo é idêntico ao do loop principal, mas usamos o dicionário
         # GPS_TAG_NUMBER para obter os nomes corretos das tags.
         idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strTagNumber     = GPS_TAG_NUMBER.get(idTAGNumber, 'Unknown GPS Tag')

         idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')

         numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         
         # NOTA EDUCACIONAL: Nesta versão, estamos apenas lendo o valor bruto.
         # Dados de GPS como latitude e longitude estão no formato "Rational"
         # e exigiriam um tratamento adicional aqui para converter seus offsets
         # em valores legíveis (ex: graus, minutos, segundos).

         lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
         lstGpsMetadata.append(dict(zip(lstGpsMetaHeader, lstTemp)))
   # --- FIM DA MODIFICAÇÃO 3 ---

   # --- PASSO 4: FINALIZAÇÃO E EXIBIÇÃO ---
   
   # Fecha o arquivo para liberar os recursos do sistema.
   fileInput.close()

   # Imprime os dados do cabeçalho EXIF.
   print('\n\nDados do Cabeçalho EXIF\n' + '-'*30)
   for key,value in dictEXIF.items(): 
      print(f'{key:15}: {value}')

   # Imprime os metadados principais lidos.
   print('\n\nMetadados Lidos\n' + '-'*30)
   for metaData in lstMetadata:
      print(f'{metaData}')

   # --- INÍCIO DA MODIFICAÇÃO 4: Imprimir os metadados de GPS lidos ---
   # Verifica se a lista de metadados de GPS contém algum item.
   if lstGpsMetadata:
      print('\n\nMetadados de GPS Lidos (Valores Brutos)\n' + '-'*50)
      for metaData in lstGpsMetadata:
         print(f'{metaData}')
   else:
      # Informa ao usuário caso nenhuma tag de GPS tenha sido encontrada.
      print('\n\nNenhuma informação de GPS encontrada.\n' + '-'*30)
   # --- FIM DA MODIFICAÇÃO 4 ---
   
   print('\n\n')