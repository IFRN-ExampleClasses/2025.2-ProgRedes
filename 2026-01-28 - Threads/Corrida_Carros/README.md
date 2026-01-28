## Simulação de Corrida F1 com Threads em Python

<p>Este repositório contém uma série de scripts didáticos em Python projetados para ensinar conceitos fundamentais de Programação Concorrente, Multithreading, Sincronização e Condições de Corrida (Race Conditions).</p>

<hr>

<p>🎯 O Problema</p>

<p>O cenário é uma corrida de Fórmula 1 com três pilotos: Lewis Hamilton, Sebastian Vettel e Max Verstappen.</p>

<p>O objetivo é simular a corrida onde cada carro possui uma velocidade diferente. O desafio evolui de uma execução simples e sequencial para uma execução paralela (vários carros correndo ao mesmo tempo), lidando com problemas clássicos de computação como:</p>

<ul>
  <li>Compartilhamento de recursos (o terminal/tela);</li>
  <li>Acesso simultâneo a variáveis globais (quem é o vencedor?);</li>
  <li>Uso de travas (Lock) para garantir a integridade dos dados.</li>
</ul>

<hr>

<p>📂 Evolução das Versões</p>

<p>Abaixo está a descrição detalhada de cada versão e os conceitos abordados.</p>

<ul>
  <li><strong>📄 Arquivo: corrida_v.0.0.py</strong></li>
  <ul>
    <li>Sequencial (Bloqueante);</li>
    <li>Conceito: Programação Síncrona;</li>
    <li>Comportamento: Um carro só começa a correr depois que o anterior termina todas as voltas;</li>
    <li>O que observar: O programa é seguro e previsível, mas ineficiente, pois não utiliza o poder do processamento paralelo. O tempo total é a soma do tempo de todos os pilotos.<br/><br/></li>
  </ul>

  <li><strong>📄 Arquivo: corrida_v.0.1.py</strong></li>
  <ul>
    <li>Paralelismo "Caótico" (Sem Join);</li>
    <li>Conceito: Introdução à classe threading.Thread;</li>
    <li>Mudança: Os carros são disparados em threads separadas (t.start());</li>
    <li>Problema: A Thread Principal (Main) não espera os pilotos terminarem. O programa imprime "A corrida terminou" antes mesmo dos carros completarem a primeira volta. O terminal fica "sujo" com prints aparecendo após o fim do script.<br/><br/></li>
  </ul>

  <li><strong>📄 Arquivo: corrida_v.0.2.py</strong></li>
  <ul>
    <li>Sincronização Básica (Barrier);</li>
    <li>Conceito: Método .join();</li>
    <li>Mudança: A Thread Principal agora aguarda (join) todas as threads dos pilotos terminarem antes de encerrar o programa;</li>
    <li>Resultado: Temos processamento paralelo real e o programa só termina quando o último piloto cruza a linha de chegada.<br/><br/></li>
  </ul>
  
  <li><strong>📄 Arquivo: corrida_v.0.3.py</strong></li>
  <ul>
    <li>Recurso Compartilhado & Visualização;</li>
    <li>Conceito: Acesso a Variáveis Globais e Concorrência de I/O;</li>
    <li>Mudança:</li>
    <ul>
      <li>Introdução da variável global strVencedor;</li>
      <li>Alteração no visual do print usando end=' -> '.</li>
    </ul>
    <li>O que observar: A saída no terminal fica "misturada" (Ex: S01.L01.S02...). Isso prova visualmente que o processador está alternando entre as threads rapidamente.<br/><br/></li>
  </ul>
  
  <li><strong>📄 Arquivo: corrida_v.0.4.py</strong></li>
  <ul>
    <li>A Teoria da "Condição de Corrida";</li>
    <li>Conceito: Race Condition (Teórico);</li>
    <li>Mudança: As velocidades dos pilotos são alteradas para milésimos de diferença (2.001, 2.002...), forçando uma chegada quase simultânea;</li>
    <li>O Problema: O código documenta (comentários M1-M5) como dois pilotos podem testar if vencedor is None ao mesmo tempo, gerando uma inconsistência onde o segundo piloto a chegar sobrescreve o nome do verdadeiro vencedor.<br/><br/></li>
  </ul>

  <li><strong>📄 Arquivo: corrida_v.0.5.py</strong></li>
  <ul>
    <li>Solução Drástica (Granularidade Grossa);</li>
    <li>Conceito: Mutex / Lock Global;</li>
    <li>Mudança: Introdução de lck = threading.Lock(). O bloqueio (acquire) é feito antes do loop de voltas;</li>
    <li>Efeito Colateral: Embora resolva o problema do vencedor, mata o paralelismo. O código volta a se comportar como sequencial (fila indiana), pois um carro bloqueia a pista inteira para si até terminar.<br/><br/></li>
  </ul>
  
  <li><strong>📄 Arquivo: corrida_v.0.6.py</strong></li>
  <ul>
    <li>Solução Ideal (Granularidade Fina);</li>
    <li>Conceito: Otimização de Bloqueio (Critical Section);</li>
    <li>Mudança: O lock é removido do loop de voltas e colocado apenas no momento de cruzar a linha de chegada e verificar o vencedor;</li>
    <li>Resultado: O paralelismo é restaurado (saída misturada no terminal) e a integridade da variável vencedor é mantida. Temos o melhor dos dois mundos.<br/><br/></li>
  </ul>
  
  <li><strong>📄 Arquivo: corrida_v.0.7.py</strong></li>
  <ul>
    <li>Checagem em Tempo Real (Atomicidade);</li>
    <li>Conceito: Verificação dentro do Loop;</li>
    <li>Mudança: O bloqueio (acquire/release) é movido para dentro do loop while;</li>
    <li>Lógica: A cada volta, a thread trava momentaneamente para incrementar o contador de voltas e verificar se aquela foi a última. Isso permite definir o vencedor no exato instante matemático da última volta, mantendo a corrida paralela.<br/><br/></li>
  </ul>
</ul>

<hr/>
