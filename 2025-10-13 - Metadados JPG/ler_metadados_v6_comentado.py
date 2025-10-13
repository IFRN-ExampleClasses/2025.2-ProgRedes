'''
   Lendo Metadados de Imagens JPG (EXIF)
   --------------------------------------
   Este script foi projetado para ler e interpretar os metadados EXIF (Exchangeable Image File Format)
   contidos em um arquivo de imagem no formato JPEG (.jpg). A leitura é feita em baixo nível,
   analisando os bytes do arquivo de acordo com a especificação do formato EXIF, que utiliza
   a estrutura do formato TIFF (Tagged Image File Format) para organizar os dados.
'''
import os
import sys

# Importa as funções auxiliares que abstraem a leitura de tipos de dados específicos.
# Ex: lerDadosASCII, lerDadosRational, converterGrausDecimais.
# Isso mantém o código principal mais limpo e focado na lógica de navegação do arquivo.
from metadados_funcoes import *

# Importa os dicionários que mapeiam os códigos numéricos (tags) para nomes legíveis.
# Ex: TAG_NUMBER = { 0x0110: 'Model' }, GPS_TAG_NUMBER = { 0x0002: 'GPSLatitude' }, etc.
# Isso torna a saída do programa compreensível para um ser humano.
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
CODE_PAGE = 'utf-8'

# Define o nome e o caminho completo do arquivo de imagem que será analisado.
strNomeArq = f'{DIR_IMG}\\presepio_natalino.jpg'


# ------------------------------------------------------------------------------------------
# O bloco try...except...else é usado para tratar possíveis erros de forma elegante.
try:
   # Tenta abrir o arquivo de imagem especificado em modo de leitura binária ('rb').
   # O modo binário é essencial porque precisamos ler os bytes exatos do arquivo,
   # sem qualquer interpretação ou conversão de texto automática.
   fileInput = open(strNomeArq, 'rb')

except FileNotFoundError:
   # Se o arquivo não for encontrado no caminho especificado, o programa é encerrado
   # com uma mensagem de erro clara.
   sys.exit('\nERRO: Arquivo Não Existe...\n')

except Exception as erro:
   # Captura qualquer outra exceção que possa ocorrer ao tentar abrir o arquivo
   # e encerra o programa, exibindo o erro.
   sys.exit(f'\nERRO: {erro}...\n')

else:
   # Este bloco 'else' só é executado se o 'try' for bem-sucedido (o arquivo foi aberto).

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

   # --- PASSO 2: LEITURA DO CABEÇALHO EXIF (que contém o cabeçalho TIFF) ---

   exifSize      = fileInput.read(2) # Tamanho do segmento EXIF.
   exifHeader    = fileInput.read(4) # Deve conter a string "Exif".
   temp1         = fileInput.read(2) # Dois bytes nulos de preenchimento (padding).
   
   # --- Início do Cabeçalho TIFF ---
   endianHeader  = fileInput.read(2) # Ordem dos bytes (Endianness): 'II' (Little) ou 'MM' (Big).
   temp2         = fileInput.read(2) # Fixo, versão do TIFF (0x002A).
   temp3         = fileInput.read(4) # Offset para o primeiro diretório de metadados (IFD).
   countMetadata = fileInput.read(2) # Quantidade de metadados (tags) no primeiro diretório.

   # --- PASSO 3: INTERPRETAÇÃO DO CABEÇALHO ---

   # Determina a ordem dos bytes ('little' ou 'big'). Isso é CRUCIAL para ler
   # corretamente qualquer número que ocupe mais de um byte no restante do arquivo.
   # 'II' (b'\x49\x49') -> Little Endian (Intel)
   # 'MM' (b'\x4D\x4D') -> Big Endian (Motorola)
   strOrderByte  = 'little' if endianHeader == b'\x49\x49' else 'big'

   # Converte os valores lidos como bytes para números inteiros, usando a ordem de bytes correta.
   exifSize      = int.from_bytes(exifSize, byteorder=strOrderByte)
   countMetadata = int.from_bytes(countMetadata, byteorder=strOrderByte)

   # Armazena as informações do cabeçalho em um dicionário para fácil visualização.
   dictEXIF = { 'exifSize' : exifSize, 'exifMarker': exifHeader, 
                'padding'  : temp1, 'endian'    : endianHeader, 
                'tiffVersion': temp2, 'ifdOffset' : temp3,
                'metaCount': countMetadata }
   
   # Variável para armazenar o endereço (offset) do subdiretório de GPS.
   # A tag 0x8825 não contém os dados de GPS em si, mas sim um ponteiro para eles.
   intGPSInfoOffset = None
   
   # --- PASSO 4: LEITURA DO DIRETÓRIO PRINCIPAL DE METADADOS (IFD0) ---
   lstMetadata   = list()
   lstMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
   for _ in range(countMetadata):
      # Cada entrada de metadado (tag) tem uma estrutura fixa de 12 bytes.

      # Bytes 0-1: O número da TAG (identificador do metadado).
      idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      strTagNumber     = TAG_NUMBER.get(idTAGNumber, 'Unknown Tag')
      
      # Bytes 2-3: O formato do dado (string, inteiro, racional, etc.).
      idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')

      # Bytes 4-7: O número de componentes (ex: o número de caracteres em uma string).
      numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte) 

      # Bytes 8-11: O valor do dado OU um OFFSET (ponteiro) para a localização do dado.
      # Se o dado for maior que 4 bytes, este campo armazena o endereço onde o dado real está.
      dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte) 

      # Se encontrarmos a tag de GPS (0x8825), guardamos o offset para uso posterior.
      if idTAGNumber == 0x8825: intGPSInfoOffset = dataValue

      # Se o formato for ASCII (string), o `dataValue` é um offset.
      # Chamamos uma função auxiliar para ir até esse offset, ler e decodificar a string.
      if idDataFormat == 0x0002: # 0x0002 é o código para ASCII String
         dataValue = lerDadosASCII(fileInput, dataValue, numberComponents, CODE_PAGE)

      # Monta e armazena o metadado lido.
      lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
      lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

   # --- PASSO 5: LEITURA E TRATAMENTO DOS METADADOS DE GPS (SE EXISTIREM) ---
   lstGpsMetadata = list()
   if intGPSInfoOffset:
      # Posiciona o leitor do arquivo no início do bloco de dados de GPS,
      # usando o offset que guardamos anteriormente. O '+ 12' ajusta o offset
      # para ser relativo ao início do cabeçalho TIFF.
      fileInput.seek(intGPSInfoOffset + 12)
      # Lê a quantidade de tags de GPS existentes neste subdiretório.
      countGpsMetadata = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
      
      # ETAPA 1: Ler todas as tags de GPS do arquivo e armazená-las "cruas".
      # Esta abordagem é necessária porque a interpretação de uma tag (ex: GPSLatitude)
      # depende do valor de outra (ex: GPSLatitudeRef - Norte ou Sul).
      # Primeiro, coletamos todas as "peças do quebra-cabeça".
      gps_data_raw = dict()
      for _ in range(countGpsMetadata):
         idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strTagNumber     = GPS_TAG_NUMBER.get(idTAGNumber, 'Unknown GPS Tag')
         idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte)
         strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')
         numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)
         
         # Assim como antes, se o dado for maior que 4 bytes, `dataValue` é um offset.
         # Usamos funções auxiliares para ler os dados reais nesses offsets.
         valor_final = dataValue
         if strDataFormat == 'ASCII String':
            valor_final = lerDadosASCII(fileInput, dataValue, numberComponents, CODE_PAGE)
         elif strDataFormat == 'Unsigned Rational': # Formato para coordenadas (graus/min/seg)
            valor_final = lerDadosRational(fileInput, dataValue, numberComponents, strOrderByte)

         # Armazena o dado bruto (a "peça") no dicionário de apoio.
         gps_data_raw[strTagNumber] = valor_final

      # ETAPA 2: Tratar os dados brutos e construir a lista final de metadados de GPS.
      # Agora que temos todas as "peças", podemos "montar o quebra-cabeça".
      lat_ref_bruto = gps_data_raw.get('GPSLatitudeRef')
      lat_val       = gps_data_raw.get('GPSLatitude')
      lon_ref_bruto = gps_data_raw.get('GPSLongitudeRef')
      lon_val       = gps_data_raw.get('GPSLongitude')
      alt_ref_val   = gps_data_raw.get('GPSAltitudeRef') # 0 = Acima do nível do mar, 1 = Abaixo
      alt_val       = gps_data_raw.get('GPSAltitude')
      timestamp     = gps_data_raw.get('GPSTimeStamp')   # Hora, Minuto, Segundo (UTC)
      datestamp     = gps_data_raw.get('GPSDateStamp')   # Data (UTC)

      # Converte as coordenadas de graus/minutos/segundos para graus decimais,
      # que é um formato mais fácil de usar (ex: para exibir em um mapa).
      if lat_val:
         lat_ref = lat_ref_bruto if lat_ref_bruto in ['N', 'S'] else 'S'
         lstGpsMetadata.append({'TAGNumber': 'Latitude', 'DataValue': converterGrausDecimais(lat_val, lat_ref)})
         lstGpsMetadata.append({'TAGNumber': 'Ref. Latitude', 'DataValue': MAPEAMENTO_REF.get(lat_ref)})

      if lon_val:
          lon_ref = lon_ref_bruto if lon_ref_bruto in ['E', 'W'] else 'W'
          lstGpsMetadata.append({'TAGNumber': 'Longitude', 'DataValue': converterGrausDecimais(lon_val, lon_ref)})
          lstGpsMetadata.append({'TAGNumber': 'Ref. Longitude', 'DataValue': MAPEAMENTO_REF.get(lon_ref)})

      # Trata a altitude, aplicando sinal negativo se estiver abaixo do nível do mar.
      if alt_val:
         altitude = alt_val[0] if isinstance(alt_val, list) else alt_val
         if alt_ref_val == 1: altitude = -altitude
         lstGpsMetadata.append({'TAGNumber': 'Altitude', 'DataValue': f"{altitude:.2f} metros"})

      # Combina data e hora em um único campo legível.
      if timestamp and datestamp:
         hora = f"{int(timestamp[0]):02d}:{int(timestamp[1]):02d}:{int(timestamp[2]):02d} UTC"
         lstGpsMetadata.append({'TAGNumber': 'Data e Hora (UTC)', 'DataValue': f"{datestamp} {hora}"})

   # --- PASSO 6: FINALIZAÇÃO E EXIBIÇÃO ---
   
   # Fecha o arquivo para liberar os recursos do sistema. É uma boa prática fundamental.
   fileInput.close()

   # Imprime os dados do cabeçalho EXIF de forma organizada.
   print('\n\nDados do Cabeçalho EXIF\n' + '-'*30)
   for key,value in dictEXIF.items(): print(f'{key:15}: {value}')

   # Imprime os metadados principais lidos.
   print('\n\nMetadados Lidos\n' + '-'*30)
   for metaData in lstMetadata: print(f'{metaData}')

   # Imprime os metadados de GPS, se tiverem sido encontrados e tratados.
   if lstGpsMetadata:
      print('\n\nMetadados de GPS Lidos\n' + '-'*30)
      for metaData in lstGpsMetadata: print(f'{metaData}')

   print('\n\n')