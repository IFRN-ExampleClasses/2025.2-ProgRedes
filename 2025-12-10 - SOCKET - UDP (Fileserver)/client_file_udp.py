# Importando as bibliotecas necessárias
import socket, os, struct

# Importando o arquivo de constantes e funções
import constantes, funcoes

# Limpando a tela do terminal
os.system('cls') if os.name == 'nt' else os.system('clear')

try:
   # Criando o socket
   sockClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   
   # Definindo o timeout para o socket do cliente
   sockClient.settimeout(constantes.TIMEOUT_SOCKET)

   # Enviando uma 'sinalização' de que um cliente se conectou ao servidor (FRAGMENTADO)
   strMensagemEntrada = f'{chr(175)} {constantes.HOST_IP_CLIENT}'
   byteMensagemEntrada = strMensagemEntrada.encode(constantes.CODE_PAGE)
   
   # Itera e envia cada fragmento da sinalização, chamando o Gerador diretamente
   for byteFragmento in funcoes.fragmentarDados(byteMensagemEntrada):
      sockClient.sendto(byteFragmento, constantes.TUPLA_SERVER)

   # Mensagem inicial do cliente
   print('\n' + '-'*100)
   print('CLIENTE UDP Inicializado - Enviando Comandos...')
   print('Digite SAIR para sair do cliente...\n')
   print(f'IP/Porta do Cliente.:{constantes.TUPLA_CLIENTE}')
   print('-'*100 + '\n')

   # Variáveis de estado global para recebimento contínuo de arquivo
   strNomeArquivoReceber = '' 
   objArquivoRecebimento = None # Objeto arquivo aberto em 'wb'
   intTotalFragmentosEsperados = 0 
   
   # Loop principal do cliente
   while True:
      # LÓGICA DE ENVIO DO COMANDO
      # Só pede input se não houver um arquivo aberto (modo de streaming inativo)
      if objArquivoRecebimento is None:
         strMensagem = input('Digite o comando: ').lower().strip()
      else:
         # Se estiver em modo de download, não pede input, força o recebimento
         strMensagem = ''
         
      if strMensagem == 'sair':
         byteMensagemSaida = strMensagem.encode(constantes.CODE_PAGE)
         for byteFragmento in funcoes.fragmentarDados(byteMensagemSaida):
            sockClient.sendto(byteFragmento, constantes.TUPLA_SERVER)
         break

      # Só envia o comando se tiver recebido input e não for download contínuo
      if strMensagem:
         # LÓGICA DE ENVIO DO COMANDO COM FRAGMENTAÇÃO
         byteMensagem = strMensagem.encode(constantes.CODE_PAGE)
         try:
            for byteFragmento in funcoes.fragmentarDados(byteMensagem):
               sockClient.sendto(byteFragmento, constantes.TUPLA_SERVER)
         except Exception as e:
            print(f'\nERRO ao enviar fragmento: {e}')
            continue 

      # LÓGICA DE RECEBIMENTO CONTÍNUO
      
      # Controla se o cliente deve processar mais mensagens/chunks.
      boolReceberProximaMensagem = True 

      while boolReceberProximaMensagem:
         
         # 1. Checa a condição de parada: se não houver arquivo aberto E não houver comando enviado, sai do loop de recebimento.
         if objArquivoRecebimento is None and not strMensagem:
             boolReceberProximaMensagem = False
             break
             
         # 1. Lógica de Recebimento de UMA Mensagem Fragmentada (Chunk)
         dictFragmentosRecebidos = {}
         intTotalFragmentos = 0
         
         boolTransferenciaFalhou = False
         
         # Loop interno para receber todos os fragmentos de UM chunk
         while True:
             try:
                 byteFragmento, tuplaServidor = sockClient.recvfrom(constantes.BUFFER_SIZE)
                 
                 byteCabecalho = byteFragmento[:8]
                 intTotalFragmentos, intNumFragmento = struct.unpack('<II', byteCabecalho)
                 
                 dictFragmentosRecebidos[intNumFragmento] = byteFragmento[8:] 
                 
                 if len(dictFragmentosRecebidos) == intTotalFragmentos:
                     break
                 
             except socket.timeout:
                 # Timeout durante o recebimento do CHUNK (Fim do Stream ou Falha)
                 if objArquivoRecebimento:
                    # Se estava baixando, o timeout indica o fim da transferência.
                    objArquivoRecebimento.close()
                    print(f'\nDOWNLOAD CONCLUÍDO/INTERROMPIDO. Arquivo salvo: "{strNomeArquivoReceber}".')
                    objArquivoRecebimento = None
                    strNomeArquivoReceber = '' 
                 else:
                    print('\nERRO: Timeout na recepcao da mensagem do servidor.')
                 
                 boolTransferenciaFalhou = True
                 boolReceberProximaMensagem = False # Força a saída do loop de recebimento contínuo
                 break
             except Exception as e:
                 print(f'\nERRO ao processar fragmento de resposta: {e}')
                 boolTransferenciaFalhou = True
                 boolReceberProximaMensagem = False
                 break
         
         # 2. Processamento da Mensagem Remontada
         if boolTransferenciaFalhou:
             if objArquivoRecebimento:
                 # Se a falha ocorreu no while interno (e não foi timeout, já tratado acima)
                 objArquivoRecebimento.close()
                 print(f'DOWNLOAD FALHOU. Arquivo "{strNomeArquivoReceber}" parcial salvo: {os.path.getsize(objArquivoRecebimento.name)} bytes.')
                 objArquivoRecebimento = None
                 strNomeArquivoReceber = '' 
             break # Sai do loop for

         elif intTotalFragmentos > 0 and len(dictFragmentosRecebidos) == intTotalFragmentos:
            
            listPayloads = [dictFragmentosRecebidos[k] for k in sorted(dictFragmentosRecebidos)]
            byteMensagemCompleta = b''.join(listPayloads)
            
            if objArquivoRecebimento is None:
               # Processamento da primeira mensagem (Controle/Texto)
               
               try:
                   strMensagemRemontada = byteMensagemCompleta.decode(constantes.CODE_PAGE)
               except UnicodeDecodeError:
                   print('\nERRO: Mensagem recebida nao e string de controle valida.')
                   boolReceberProximaMensagem = False
                   continue

               if strMensagemRemontada.startswith('FILE_START:'):
                   # É a mensagem de controle
                   partes = strMensagemRemontada[11:].strip().split(':')
                   strNomeArquivoReceber = partes[0]
                   intTotalFragmentosEsperados = int(partes[1])
                   
                   # **[CORREÇÃO: REMOVIDA CHECAGEM DE EXISTÊNCIA PARA PERMITIR SOBRESCRITA]**
                   strCaminhoLocal = os.path.join(constantes.DIR_IMG_CLIENT, strNomeArquivoReceber)
                   
                   print(f'INICIANDO DOWNLOAD: {strNomeArquivoReceber} ({intTotalFragmentosEsperados} fragmentos totais) ...')
                   # Abre o arquivo para escrita, sobrescrevendo se existir
                   objArquivoRecebimento = open(strCaminhoLocal, 'wb') 
                   boolReceberProximaMensagem = True 
                   
               else:
                   # Mensagem de texto normal (resposta de \?, \f ou erro)
                   print(f'\n{strMensagemRemontada}')
                   boolReceberProximaMensagem = False # Finaliza o loop
                   
            else:
               # Processamento da mensagem sequencial (Dados Binários do Chunk)
               
               try:
                  objArquivoRecebimento.write(byteMensagemCompleta)
                  print(f'Recebido chunk ({len(byteMensagemCompleta)} bytes). Progresso: {os.path.getsize(objArquivoRecebimento.name)} bytes.')
                  
                  boolReceberProximaMensagem = True # Mantém o loop ativo para o próximo chunk
                  
               except Exception as e:
                  print(f'\nERRO ao escrever chunk no arquivo: {e}')
                  objArquivoRecebimento.close()
                  print(f'DOWNLOAD ABORTADO. Arquivo parcial salvo: {os.path.getsize(objArquivoRecebimento.name)} bytes.')
                  objArquivoRecebimento = None
                  strNomeArquivoReceber = ''
                  boolReceberProximaMensagem = False
                  
         else:
            # Caso não atinja a condição de montagem
            boolReceberProximaMensagem = False
            
except KeyboardInterrupt:
   print('\nAVISO.........: Foi Pressionado CTRL+C...\nSaindo do Cliente...\n\n')
except socket.error as strErro:
   print(f'\nERRO DE SOCKET: {strErro}\n\n')
except Exception as strErro:
   print(f'\nERRO GENÉRICO..: {strErro}\n\n')
finally:
   # Garante que o arquivo é fechado ao finalizar o programa (interrupção abrupta)
   if objArquivoRecebimento:
      objArquivoRecebimento.close()
      print(f'AVISO: Arquivo parcial "{strNomeArquivoReceber}" fechado por interrupção do programa.')
   sockClient.close()
   print('Cliente finalizado com Sucesso...\n\n')