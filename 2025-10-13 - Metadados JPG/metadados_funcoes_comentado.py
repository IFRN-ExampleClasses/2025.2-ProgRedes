# Importa o tipo 'List' do módulo 'typing' para melhorar a legibilidade
# e a verificação estática do código, indicando que a função retorna uma lista.
from typing import List

# ------------------------------------------------------------------------------------------
# --- Funções para Leitura de Tipos de Dados Específicos do EXIF ---
# ------------------------------------------------------------------------------------------

def lerDadosASCII(file_handle, offset: int, num_components: int, code_page: str) -> str:
    """
    Lê uma string de texto (formato ASCII) de uma posição específica no arquivo.

    No padrão EXIF, se um valor (como uma string) for maior que 4 bytes, ele não é
    armazenado diretamente na entrada da tag. Em vez disso, a entrada da tag contém um
    "offset", que é um ponteiro (endereço) para o local real dos dados no arquivo.
    Esta função navega até esse local, lê a string e retorna ao ponto de origem.

    Args:
        file_handle: O objeto do arquivo aberto em modo de leitura binária ('rb').
        offset (int): O endereço (ponteiro) para o início da string de dados.
        num_components (int): O comprimento da string em bytes (número de caracteres).
        code_page (str): A codificação a ser usada para decodificar os bytes em texto (ex: 'utf-8').

    Returns:
        str: A string de metadados lida e decodificada.
    """
    # 1. Salva a posição atual do leitor no arquivo. É crucial para que, após
    #    lermos este dado específico, possamos voltar exatamente para onde estávamos
    #    e continuar a ler a próxima tag de metadado em sequência.
    current_pos = file_handle.tell()

    # 2. Move o leitor para a posição onde a string está armazenada.
    #    O offset armazenado na tag é relativo ao início do cabeçalho TIFF.
    #    Este cabeçalho começa 12 bytes após o início do segmento de dados EXIF.
    #    Por isso, somamos 12 para obter a posição absoluta no arquivo.
    file_handle.seek(offset + 12)

    # 3. Lê o número exato de bytes que compõem a string, decodifica esses bytes
    #    para texto usando a página de código fornecida e remove quaisquer
    #    caracteres nulos ('\x00') que possam existir no final, que são
    #    frequentemente usados como preenchimento.
    val = file_handle.read(num_components).decode(code_page).rstrip('\x00')

    # 4. Restaura a posição do leitor para o local original, garantindo que
    #    o loop principal possa continuar de onde parou.
    file_handle.seek(current_pos)

    return val


def lerDadosRational(file_handle, offset: int, num_components: int, byte_order: str) -> List[float]:
    """
    Lê um ou mais valores no formato RATIONAL ou UNSIGNED RATIONAL do EXIF.

    O formato "Rational" é uma forma de representar um número fracionário com alta
    precisão, usando dois inteiros de 4 bytes: um numerador e um denominador.
    É comumente usado para armazenar dados como coordenadas de GPS (graus, minutos, segundos),
    abertura da lente, tempo de exposição, etc.

    Args:
        file_handle: O objeto do arquivo aberto.
        offset (int): O ponteiro para o local onde os dados racionais começam.
        num_components (int): O número de valores racionais a serem lidos.
                              (Ex: coordenadas de GPS têm 3: graus, minutos, segundos).
        byte_order (str): A ordem dos bytes ('little' ou 'big') para ler os inteiros corretamente.

    Returns:
        List[float]: Uma lista de números de ponto flutuante resultantes da divisão.
    """
    # Salva a posição atual para poder retornar depois.
    current_pos = file_handle.tell()
    # Move o leitor para a localização dos dados, ajustando o offset.
    file_handle.seek(offset + 12)
    
    valores = []
    # Itera para ler cada componente racional.
    for _ in range(num_components):
        # Lê 4 bytes para o numerador e os converte para um inteiro.
        numerador   = int.from_bytes(file_handle.read(4), byteorder=byte_order)
        # Lê 4 bytes para o denominador e os converte para um inteiro.
        denominador = int.from_bytes(file_handle.read(4), byteorder=byte_order)
        
        # Evita um erro de divisão por zero. Se o denominador for zero, o valor é inválido.
        if denominador == 0:
            valores.append(0.0)
        else:
            # Calcula o valor final e o adiciona à lista.
            valores.append(numerador / denominador)
            
    # Retorna o leitor à sua posição original.
    file_handle.seek(current_pos)
    return valores

def converterGrausDecimais(graus_min_seg: List[float], ref: str) -> float:
    """
    Converte uma coordenada geográfica do formato [Graus, Minutos, Segundos] (DMS)
    para o formato Graus Decimais (DD), que é mais fácil de usar em mapas e cálculos.

    Args:
        graus_min_seg (List[float]): Uma lista contendo três valores: [graus, minutos, segundos].
        ref (str): A referência direcional da coordenada ('N', 'S' para latitude,
                   'E', 'W' para longitude). Isso determina se o valor final é positivo ou negativo.

    Returns:
        float: A coordenada no formato de graus decimais.
    """
    # Validação para garantir que os dados de entrada estão no formato esperado.
    if len(graus_min_seg) != 3:
        return 0.0
        
    # Desempacota a lista em variáveis para maior clareza.
    graus    = graus_min_seg[0]
    minutos  = graus_min_seg[1]
    segundos = graus_min_seg[2]
    
    # Aplica a fórmula de conversão padrão de DMS para DD.
    # 1 grau = 60 minutos.
    # 1 grau = 3600 segundos.
    decimal_degrees = graus + (minutos / 60.0) + (segundos / 3600.0)
    
    # Ajusta o sinal do valor com base na referência.
    # Por convenção geográfica:
    # - Latitudes ao Sul (S) são negativas.
    # - Longitudes a Oeste (W) são negativas.
    if ref in ['S', 'W']:
        return -decimal_degrees
        
    return decimal_degrees