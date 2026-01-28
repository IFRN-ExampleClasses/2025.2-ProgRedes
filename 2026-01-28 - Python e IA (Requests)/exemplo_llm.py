import funcoes_llm

str_service = funcoes_llm.selecionarServico()

while True:
   strPrompt = input("\nDigite sua pergunta (SAIR - Encerra): ").lower()
   if strPrompt == "sair":
      print("\nSaindo do Programa...")
      break

strResposta = funcoes_llm.solicitarServico(str_service, strPrompt)
print(f"\nResposta:\n{strResposta}")