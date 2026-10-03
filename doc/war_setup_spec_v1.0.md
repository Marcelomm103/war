# Preparação da partida — WAR 1 clássico

**Passo do roadmap:** 0.5 — certificar preparação

**Data da revisão:** 2026-10-02
**Estado:** passo 0.5 concluído documentalmente para o perfil operacional. Três interpretações foram adotadas por delegação do usuário e ficam identificadas para revisão posterior; não são apresentadas como texto literal do manual.

## Escopo e fontes

- Manual escaneado: [war_manual_table_games.pdf](war_manual_table_games.pdf), principalmente pp. 2–3. As páginas foram renderizadas e conferidas visualmente; o OCR anterior foi apenas auxiliar.
- Fonte física da edição alvo: [mapa_war_classico.webp](images/mapa_war_classico.webp) e [cartas de território e objetivo](images/war_cartas1.png) a [war_cartas8.png](images/war_cartas8.png).
- Esclarecimentos normativos do usuário: jogadores válidos (3–6), desempate do dado, aplicação do mínimo de três reforços à colocação inicial, identidade das cores e regras das missões de eliminação; também registrados na [matriz de rastreabilidade](war_rules_traceability_v1.0.md).
- Os protótipos de análise visual não são fonte normativa. Eles não implementam a preparação completa e usam cores/objetivos divergentes; seus defaults de sorteio e fallback não devem ser copiados.

**Convenção:** “confirmado” significa sustentado pela página/cartas indicadas ou por esclarecimento expresso do usuário; não significa implementado nem testado em uma engine. Cálculos de distribuição abaixo decorrem do número de cartas e da distribuição sequencial descrita no manual.

## Sequência normativa conhecida

### 1. Jogadores e cores

- A partida alvo aceita **3 a 6 jogadores**, conforme esclarecimento do usuário.
- O manual lista seis conjuntos de exércitos — branco, vermelho, preto, azul, amarelo e verde — e diz que cada participante escolhe a cor de sua preferência. A escolha pode ser feita por sorteio ou por acordo comum entre participantes (p. 2).
- Para que cada jogador seja identificável no tabuleiro, cada participante usa um conjunto de cor distinto. A forma de escolha entre sorteio e acordo fica a critério da mesa, como permite o manual.

### 2. Objetivos secretos

- Há 14 cartas de objetivo. Cada jogador recebe uma por sorteio; a carta não é revelada aos adversários e as cartas restantes não são usadas na partida (manual, p. 2).
- Antes do sorteio, o manual recomenda que participantes iniciantes leiam os objetivos possíveis.
- Com menos de seis jogadores, retiram-se antes do sorteio as cartas cujo alvo seja uma cor não participante (manual, p. 2). Dadas seis missões de eliminação, uma por cor, e as oito outras missões físicas, o conjunto elegível contém $14-(6-P)=8+P$ cartas para $P$ jogadores: 11, 12, 13 ou 14 para mesas de 3, 4, 5 ou 6. Distribuir uma carta por pessoa sem reposição deixa oito cartas fora da partida.
- Se alguém receber a missão de eliminar a própria cor, a condição impressa na carta converte o objetivo em conquistar 24 territórios. Se outro jogador eliminar a cor-alvo, aplica-se a mesma conversão ao titular dessa missão. Essas condições vêm das cartas físicas e do esclarecimento normativo do usuário; não são fallback genérico para falta de cartas.

### 3. Distribuidor e ordem de distribuição

- Cada participante lança um dado; o maior resultado escolhe o distribuidor (manual, p. 2).
- O manual não explica empate. Conforme esclarecimento do usuário, somente os empatados repetem o lançamento; o resultado mais alto resolve o empate e escolhe o distribuidor.
- **Interpretação operacional adotada:** se os empatados voltarem a empatar, somente os que continuam empatados lançam novamente, repetindo até haver um maior resultado único. O manual não descreve esse caso-limite; a decisão torna a escolha do distribuidor determinística.
- A distribuição de territórios começa com a pessoa imediatamente à esquerda do distribuidor e segue no sentido horário (manual, p. 2).
- Depois de distribuídas as cartas de território, o primeiro jogador da primeira rodada é o seguinte à pessoa que recebeu a última carta; os demais seguem no sentido horário (manual, p. 2; esclarecimento do usuário). Portanto, não se deve assumir que o distribuidor sempre seja o primeiro a colocar os reforços iniciais.

### 4. Distribuição dos territórios e excedentes

- O manual lista 44 cartas de território, incluindo dois curingas. Para a atribuição inicial, o distribuidor remove os dois curingas; restam as 42 cartas correspondentes aos territórios.
- As 42 cartas são distribuídas sequencialmente, uma por vez, no sentido horário, começando à esquerda do distribuidor. A consequência aritmética para cada número de jogadores permitido é:

| Jogadores | Cartas por jogador, na ordem a partir da esquerda do distribuidor | Último a receber carta | Primeiro a jogar/colocar reforços iniciais |
|---:|---|---|---|
| 3 | 14, 14, 14 | Distribuidor | À esquerda do distribuidor |
| 4 | 11, 11, 10, 10 | Segundo jogador após o distribuidor | Terceiro jogador após o distribuidor |
| 5 | 9, 9, 8, 8, 8 | Segundo jogador após o distribuidor | Terceiro jogador após o distribuidor |
| 6 | 7, 7, 7, 7, 7, 7 | Distribuidor | À esquerda do distribuidor |

Para $P$ jogadores, $42=qP+r$, com $q=\lfloor42/P\rfloor$ e $r=42\bmod P$. Os primeiros $r$ participantes da ordem de distribuição recebem $q+1$ cartas; os demais recebem $q$. Essa regra dos excedentes é consequência direta de distribuir as cartas uma a uma até acabarem, não de uma instrução separada para fazer pilhas iguais.

**Interpretação operacional adotada — embaralhamento antes da distribuição territorial:** a p. 2 manda remover os curingas e distribuir as cartas, mas não explicita um embaralhamento prévio. Para que a atribuição seja um sorteio imparcial e reproduzível, embaralham-se as 42 cartas territoriais após retirar os dois curingas e antes da distribuição. Após a colocação de um exército em cada território, o distribuidor recolhe as cartas, recoloca os curingas, embaralha as 44 cartas e deixa o baralho fechado para o jogo. O primeiro embaralhamento é uma convenção do perfil do projeto, não uma instrução literal identificada no manual.

### 5. Exércitos e colocação inicial

- Cada jogador coloca **um exército de sua cor em cada território que recebeu**. Ao terminar a distribuição, todos os 42 territórios estão ocupados por um exército (manual, p. 2).
- Na primeira rodada, cada participante, na sua vez, recebe exércitos e os coloca no tabuleiro conforme sua estratégia (manual, p. 2). O esclarecimento do usuário determina que a reserva inicial adicional segue $R(T)=\max(3,\lfloor T/2\rfloor)$, em que $T$ é o número de territórios que o jogador recebeu. O mínimo de três aplica-se também à colocação inicial.
- O manual determina que os exércitos recebidos pela contagem de territórios sejam colocados em um ou mais territórios do próprio jogador, conforme sua estratégia (p. 3). Assim, os reforços territoriais iniciais não são limitados a uma colocação por território: podem ser concentrados em qualquer conjunto de territórios próprios, sem exceder a reserva recebida. Se o bônus continental também se aplicar na primeira rodada, seus exércitos continuam sujeitos à regra própria de colocação dentro do continente correspondente.
- Totais-base derivados da distribuição e de $R(T)$, **antes de qualquer possível bônus continental na primeira rodada**:

| Jogadores | Territórios por jogador, na ordem de distribuição | Reforços iniciais adicionais por jogador | Exércitos no tabuleiro após a colocação inicial, sem bônus continental |
|---:|---|---|---|
| 3 | 14, 14, 14 | 7, 7, 7 | 21, 21, 21 |
| 4 | 11, 11, 10, 10 | 5, 5, 5, 5 | 16, 16, 15, 15 |
| 5 | 9, 9, 8, 8, 8 | 4, 4, 4, 4, 4 | 13, 13, 12, 12, 12 |
| 6 | 7, 7, 7, 7, 7, 7 | 3, 3, 3, 3, 3, 3 | 10, 10, 10, 10, 10, 10 |

#### Bônus continental na primeira rodada — interpretação operacional adotada

A p. 2 diz que, na primeira rodada, cada jogador, na sua vez, recebe e posiciona exércitos. A p. 3 determina que, no início da vez, quem possuir um continente inteiro recebe, além dos exércitos pela contagem de territórios, o bônus da Tabela I; não traz exceção explícita para a primeira rodada. Adoto, portanto, que o bônus se aplica já na colocação inicial se o jogador tiver o continente completo no início de sua vez. Esses exércitos devem ser colocados nos territórios do próprio continente, como manda a p. 3. Esta é uma interpretação explícita do perfil do projeto, não uma frase específica do manual sobre a primeira rodada.

### 6. Retorno do baralho

Depois de todos os territórios receberem o exército inicial, o distribuidor recolhe as cartas de território, recoloca os dois curingas, embaralha o conjunto e deixa as cartas viradas para baixo perto do tabuleiro (manual, p. 2). As cartas territoriais não permanecem nas mãos dos jogadores como comprovantes de posse.

### 7. Primeira rodada e transição ao turno normal

- A partida começa pelo jogador seguinte a quem recebeu a última carta de território; a ordem segue no sentido horário (manual, p. 2).
- Na primeira rodada, cada jogador recebe e posiciona os reforços iniciais. O manual autoriza ataques somente **a partir da segunda rodada** (p. 3); o fluxo de ataque, deslocamento e recebimento de carta por conquista também é apresentado a partir da segunda rodada (p. 2).
- Portanto, a primeira rodada não inclui ataques, deslocamento final nem carta por conquista. A posse inicial já cobre todos os territórios; as cartas voltam ao baralho antes de começar o jogo.
- O total de reforços da primeira colocação é $R(T)$ mais os bônus dos continentes inteiros que o jogador possui no início de sua vez. Não há suporte para substituir essa soma por uma quantidade fixa de exércitos baseada no número de jogadores.

## Implementação existente — somente diagnóstico

Os protótipos do analyzer não certificam a preparação:

- `initialize_players` restringe a contagem a 3–6, mas sorteia dentre azul, vermelho, amarelo, verde, cinza e roxo, em divergência com as seis cores físicas; não oferece a escolha por acordo prevista no manual.
- [war_analyzer_gemini.py](../lib/war_analyzer/src/war_analyzer_gemini.py) filtra objetivos usando cinza/roxo e contém um objetivo padrão se o sorteio esgotar. Ambos os comportamentos são incompatíveis com as cartas físicas e não devem ser usados como regra.
- Não foi encontrada implementação canônica que realize a sequência completa de distribuição das 42 cartas, escolha do primeiro jogador, colocação inicial, devolução/embaralhamento do baralho ou tratamento completo dos objetivos.

Consulte a [matriz de rastreabilidade](war_rules_traceability_v1.0.md) para os IDs e casos de teste propostos. Esta especificação não executa esses testes.

## Decisões operacionais e revisão

O usuário informou que não poderia responder às perguntas naquele momento, autorizou decisões autônomas e indicou que revisará o trabalho depois. Por isso, o perfil operacional adota explicitamente: (1) embaralhar as 42 cartas territoriais antes de distribuí-las; (2) repetir o desempate apenas entre os empatados até haver um resultado único; (3) conceder na primeira rodada o bônus de cada continente completo, além de $R(T)$, colocando esse bônus dentro do continente correspondente.

As três decisões preenchem lacunas de procedimento sem serem atribuídas literalmente ao manual. Se a revisão do usuário alterar alguma delas, a especificação, a matriz e os testes derivados deverão ser atualizados antes da certificação da engine. **O passo 0.5 está concluído no perfil operacional documentado.** O passo 0.6 foi iniciado posteriormente e está registrado em [war_turn_spec_v1.0.md](war_turn_spec_v1.0.md).
