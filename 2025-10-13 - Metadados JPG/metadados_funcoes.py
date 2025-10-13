from typing import List

def lerDadosASCII(file_handle, offset: int, num_components: int, code_page: str) -> str:
    """Lê uma string ASCII a partir de um offset."""
    current_pos = file_handle.tell()
    # O offset é relativo ao início do TIFF Header (12 bytes do começo do arquivo)
    file_handle.seek(offset + 12)
    val = file_handle.read(num_components).decode(code_page).rstrip('\x00')
    file_handle.seek(current_pos)
    return val


def lerDadosRational(file_handle, offset: int, num_components: int, byte_order: str) -> List[float]:
    """
    Lê um ou mais valores no formato RATIONAL (numerador/denominador)
    e retorna uma lista de números float.
    """
    current_pos = file_handle.tell()
    file_handle.seek(offset + 12)
    
    valores = []
    for _ in range(num_components):
        numerador   = int.from_bytes(file_handle.read(4), byteorder=byte_order)
        denominador = int.from_bytes(file_handle.read(4), byteorder=byte_order)
        if denominador == 0:
            valores.append(0.0)
        else:
            valores.append(numerador / denominador)
            
    file_handle.seek(current_pos)
    return valores

def converterGrausDecimais(graus_min_seg: List[float], ref: str) -> float:
    """Converte [graus, minutos, segundos] para graus decimais."""
    if len(graus_min_seg) != 3:
        return 0.0
        
    graus    = graus_min_seg[0]
    minutos  = graus_min_seg[1]
    segundos = graus_min_seg[2]
    
    decimal_degrees = graus + (minutos / 60.0) + (segundos / 3600.0)
    
    if ref in ['S', 'W']:
        return -decimal_degrees
    return decimal_degrees