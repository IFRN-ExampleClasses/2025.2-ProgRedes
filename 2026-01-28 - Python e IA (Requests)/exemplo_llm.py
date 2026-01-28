import funcoes_llm  # Importa o módulo local contendo a lógica de conexão e seleção de serviços

# ----------------------------------------------------------------------
# 1. Configuração Inicial e Seleção do Modelo
# Esta etapa é executada apenas uma vez, antes de entrar no loop de chat.
# O usuário define qual "cérebro" (Gemini, OpenAI, DeepSeek) processará as perguntas.
str_service = funcoes_llm.selecionarServico()

print(f"\n--- Iniciando Chat com {str_service.upper()} ---")

# ----------------------------------------------------------------------
# 2. Loop Principal da Aplicação (REPL - Read-Eval-Print Loop)
# Mantém o programa rodando continuamente para permitir múltiplas perguntas
# sem precisar reiniciar o script a cada interação.
while True:

    # ------------------------------------------------------------------
    # 2.1 Captura de Entrada (Input)
    # Solicitamos o texto ao usuário. 
    # IMPORTANTE: Não usamos .lower() aqui para preservar a formatação original.
    # LLMs entendem melhor o contexto com letras maiúsculas/minúsculas corretas 
    # (ex: distinguir "Apple" empresa de "apple" fruta).
    strPrompt = input("\nDigite sua pergunta (ou 'SAIR' para encerrar): ")
    
    # ------------------------------------------------------------------
    # 2.2 Verificação de Saída
    # Aqui sim usamos .lower() apenas para a comparação lógica.
    # Isso garante que "Sair", "SAIR", "sair" ou "SaIr" funcionem para fechar o programa.
    if strPrompt.lower() == "sair":
        print("\nSaindo do Programa. Até logo!")
        break  # O comando 'break' interrompe o loop 'while' imediatamente.

    # ------------------------------------------------------------------
    # 2.3 Validação de Conteúdo
    # O método .strip() remove espaços em branco no início e fim.
    # O 'if' verifica se sobrou algum texto. Isso impede o envio de perguntas 
    # vazias (apenas ENTER ou espaços), economizando chamadas de API desnecessárias.
    if strPrompt.strip():
        
        print(f"   >> Enviando para {str_service}...") # Feedback visual de carregamento
        
        # --------------------------------------------------------------
        # 2.4 Chamada ao Serviço (CORRIGIDO: Agora dentro do Loop)
        # Chama a função que monta o JSON, envia o POST request e trata o erro.
        # Esta é uma chamada "bloqueante" (síncrona): o código espera a resposta chegar
        # antes de continuar para a próxima linha.
        strResposta = funcoes_llm.solicitarServico(str_service, strPrompt)
        
        # --------------------------------------------------------------
        # 2.5 Exibição da Resposta
        # Imprime o texto retornado pela IA.
        print(f"\nResposta:\n{strResposta}")
        
    else:
        # Caso o usuário aperte Enter sem digitar nada
        print("   (Por favor, digite algum texto antes de enviar)")

# Fim do loop while. O programa volta para a linha 'strPrompt = input(...)'