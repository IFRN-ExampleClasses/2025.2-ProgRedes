'''
   Lendo Metadados de Imagens JPG (EXIF)
   --------------------------------------
   Este script foi projetado para ler e interpretar os metadados EXIF (Exchangeable Image File Format)
   contidos em um arquivo de imagem no formato JPEG (.jpg). Ele faz isso abrindo o arquivo em modo
   binário e lendo os bytes de acordo com a especificação do formato EXIF, que é embutido dentro
   da estrutura do arquivo JPEG.

   Nesta versão (v3), o script lê o cabeçalho e a lista de metadados, mas ainda não interpreta
   os valores que são "offsets" (ponteiros para outros locais do arquivo), como no caso de strings.
'''
import os
import sys

# Supondo que o arquivo metadados_contantes.py exista e contenha os dicionários
# TAG_NUMBER e DATA_FORMAT, que mapeiam os códigos numéricos dos metadados para
# nomes e tipos legíveis por humanos.
# Exemplo: TAG_NUMBER = { 0x0110: 'Model', 0x010F: 'Make', ... }
from metadados_contantes import *

# ------------------------------------------------------------------------------------------
# Variáveis e Constantes Globais

# Obtém o caminho absoluto do diretório onde este script está localizado.
# __file__ é uma variável especial do Python que contém o caminho para o arquivo atual.
DIR_APP    = os.path.dirname(__file__)

# Define o diretório onde as imagens a serem analisadas estão localizadas.
DIR_IMG    = f'{DIR_APP}\\imagens'

# Define o nome e o caminho completo do arquivo de imagem que será analisado.
strNomeArq = f'{DIR_IMG}\\presepio_natalino.jpg'


# ------------------------------------------------------------------------------------------
# O bloco try...except...else é usado para tratar possíveis erros de forma elegante.
try:
   # Tenta abrir o arquivo de imagem especificado em modo de leitura binária ('rb').
   # O modo binário é essencial porque precisamos ler os bytes exatos do arquivo,
   # sem qualquer interpretação ou conversão de caracteres que o modo texto faria.
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

   # Os próximos bytes formam o cabeçalho EXIF, que por sua vez contém um cabeçalho TIFF.
   # Esta estrutura define como os metadados estão organizados.

   exifSize      = fileInput.read(2) # Tamanho total do segmento EXIF.
   exifHeader    = fileInput.read(4) # Marcador "Exif" que identifica o início dos dados.
   temp1         = fileInput.read(2) # Dois bytes nulos de preenchimento (padding).
   
   # --- Início do Cabeçalho TIFF ---
   # O padrão EXIF utiliza a estrutura do formato TIFF para armazenar os metadados.

   # Endianness: A ordem dos bytes. É a informação mais crítica para a leitura correta dos dados.
   # 'II' (b'\x49\x49') -> Little Endian (usado pela Intel). Ex: 0x1234 é lido como 34 12.
   # 'MM' (b'\x4D\x4D') -> Big Endian (usado pela Motorola). Ex: 0x1234 é lido como 12 34.
   endianHeader  = fileInput.read(2)

   # Bytes fixos que fazem parte da especificação TIFF.
   temp2         = fileInput.read(2) # Versão do TIFF, geralmente 0x002A.
   temp3         = fileInput.read(4) # Offset (endereço) para o primeiro diretório de metadados.

   # Número de entradas de metadados (tags) que estão neste primeiro diretório.
   countMetadata = fileInput.read(2)

   # --- PASSO 3: INTERPRETAÇÃO DO CABEÇALHO ---

   # Verifica a ordem dos bytes (Endianness) e define uma string para usar nas conversões.
   # A partir deste ponto, toda leitura de números com mais de 1 byte DEVE usar essa ordem.
   strOrderByte  = 'little' if endianHeader == b'\x49\x49' else 'big'

   # Agora que sabemos a ordem dos bytes, podemos converter os valores que lemos para inteiros.
   exifSize      = int.from_bytes(exifSize, byteorder=strOrderByte)
   countMetadata = int.from_bytes(countMetadata, byteorder=strOrderByte)

   # Armazena as informações do cabeçalho em um dicionário para fácil visualização.
   dictEXIF = { 'exifSize' : exifSize, 'exifMarker': exifHeader, 
                'padding'  : temp1, 'endian'    : endianHeader, 
                'tiffVersion': temp2, 'ifdOffset' : temp3,
                'metaCount': countMetadata }

   # --- PASSO 4: LEITURA DOS METADADOS (TAGS) ---

   lstMetadata   = list()
   lstMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
   # Itera sobre o número de metadados que foi identificado no cabeçalho.
   for _ in range(countMetadata):
      # Cada entrada de metadado (tag) no diretório (IFD) tem uma estrutura fixa de 12 bytes.
      
      # Bytes 0-1: O número da TAG (identificador do metadado). Ex: 0x0110 para "Modelo da Câmera".
      idTAGNumber      = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      # Usa o dicionário do arquivo 'metadados_contantes' para obter o nome legível da TAG.
      strTagNumber     = TAG_NUMBER.get(idTAGNumber, 'Unknown Tag')
      
      # Bytes 2-3: O formato do dado. Ex: 2 para string ASCII, 3 para inteiro curto.
      idDataFormat     = int.from_bytes(fileInput.read(2), byteorder=strOrderByte) 
      strDataFormat    = DATA_FORMAT.get(idDataFormat, 'Unknown Format')

      # Bytes 4-7: O número de componentes. Para uma string, é o número de caracteres. Para um
      # único inteiro, é 1.
      numberComponents = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)

      # Bytes 8-11: O valor do dado OU um OFFSET (ponteiro) para a localização do dado.
      # Se o dado (ex: um inteiro curto) couber em 4 bytes, ele é armazenado aqui mesmo.
      # Se for maior (como uma string longa), aqui fica um endereço (offset) para onde o dado está.
      # NOTA: Nesta versão do código, estamos apenas lendo este valor, sem ainda verificar
      # se ele é um dado direto ou um ponteiro.
      dataValue        = int.from_bytes(fileInput.read(4), byteorder=strOrderByte)

      # Cria uma lista temporária com os dados da tag e a adiciona à lista principal de metadados.
      lstTemp = [strTagNumber, strDataFormat, numberComponents, dataValue]
      lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

   # --- PASSO 5: FINALIZAÇÃO E EXIBIÇÃO ---

   # Fecha o arquivo para liberar os recursos do sistema. É uma boa prática fundamental.
   fileInput.close()

   # Imprime os dados do cabeçalho EXIF que foram lidos e interpretados.
   print('\n\nDados do Cabeçalho EXIF\n' + '-'*30)
   for key,value in dictEXIF.items(): 
      print(f'{key:15}: {value}')

   # Imprime cada metadado encontrado, de forma organizada.
   # Note que para strings, o 'DataValue' será um número (o offset), não o texto em si.
   print('\n\nMetadados Lidos (Valores Brutos)\n' + '-'*30)
   for metaData in lstMetadata:
      print(f'{metaData}')

   print('\n\n')