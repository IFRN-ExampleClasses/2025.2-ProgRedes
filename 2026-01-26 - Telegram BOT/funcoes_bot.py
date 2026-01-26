# ----------------------------------------------------------------------
def startBot() -> str:
   """
      Retorna mensagem de boas vindas do bot.
   """
   return (
      "Bem-vindo ao BOT TELEGRAM!\n\n"
      "Este é um bot simples para aprendizado.\n\n"
      "/? → Exibe mensagem de ajuda."
    )


# ----------------------------------------------------------------------
def ajudaBot() -> str:
   """
      Retorna instruções de uso do bot.
   """
   return (
      "COMANDOS DISPONÍVEIS:\n"
      "/fatorial:valor → Calcula o fatorial do número informado.\n"
      "\tExemplo: /fatorial:5 → Fatorial de 5 = 120\n\n"
      "/fibonacci:valor → Retorna os n primeiros números da sequência de Fibonacci.\n"
      "\tExemplo: /fibonacci:7 → 1, 1, 2, 3, 5, 8, 13\n\n"
      "/? → Exibe esta mensagem de ajuda."
    )


# ----------------------------------------------------------------------
# Função para calcular o fatorial de um número inteiro não negativo.
def fatorialBot(valor: int) -> str:
   """
      Calcula o fatorial de um número inteiro não negativo.
   """
   if not valor:
      raise Exception("ERRO:\nEstá faltando ser informado um valor...")

   try:
      valor = int(valor)
   except ValueError:
      raise Exception("ERRO: informe um número inteiro válido...")

   if valor < 0:
      raise Exception("ERRO: não existe fatorial de número negativo...")

   intFatorial = 1
   for i in range(2, valor + 1): intFatorial *= i

   return f"{valor}! = {intFatorial}"


# ----------------------------------------------------------------------
def fibonacciBot(valor: int) -> str:
   """
      Retorna os n primeiros números da sequência de Fibonacci.
   """
   if not valor:
      raise Exception("ERRO:\nEstá faltando ser informado um valor...")

   try:
      valor = int(valor)
   except ValueError:
      raise Exception("ERRO: informe um número inteiro válido...")

   if valor <= 0:
      raise Exception("ERRO: o valor deve ser maior que zero.")
    
   lstFibonacci = [1, 1]
   while len(lstFibonacci) < valor:
      lstFibonacci.append(lstFibonacci[-1] + lstFibonacci[-2])

   return f"Sequência de Fibonacci ({valor} termos):\n" + "\n".join(map(str, lstFibonacci[:valor]))


