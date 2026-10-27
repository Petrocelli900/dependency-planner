# Decisões técnicas

Entrada JSON mapeia nome de tarefa para a lista de tarefas que devem terminar antes dela. Dependências desconhecidas são rejeitadas; repetidas são deduplicadas. O grafo de entrada não é modificado.

O algoritmo de Kahn agrupa nós com grau de entrada zero em ondas. Cada onda é ordenada alfabeticamente; qualquer tarefa em uma onda depende somente de ondas anteriores. Essa ordem é estável mesmo quando a ordem das chaves JSON muda.

Complexidade do grafo é O(V+E), acrescida da ordenação dos nós de cada onda. O algoritmo é iterativo e não sofre limite de recursão em cadeias longas.

Ciclos geram CycleError. A lista blocked inclui participantes de ciclos e tarefas que dependem deles: não é uma descrição exata do caminho de um ciclo.

Esta ferramenta só planeja. Não executa comandos, não inicia threads, não agenda horários nem resolve capacidades de recursos. Ondas podem rodar em paralelo apenas se o executor e os recursos permitirem.

CLI retorna 0 para planejamento válido e 2 para erro de leitura, esquema ou ciclo.
