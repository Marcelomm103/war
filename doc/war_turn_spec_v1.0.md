# Turno e resolução das regras — WAR 1 clássico

**Passo do roadmap:** 0.6 — certificar o turno completo

**Data da revisão:** 2026-10-02

**Estado:** regras do turno consolidadas documentalmente para o perfil WAR 1. As regras explícitas do manual e do usuário estão separadas das convenções operacionais. Há questões de desempate de vitória simultânea e descarte/reutilização de cartas que impedem certificação estrita da engine até revisão; a especificação não inventa resoluções para esses casos.

## Fontes e precedência

- Manual escaneado, páginas 3–8: reforços, ataques, batalha, conquista, deslocamentos, compra/troca de cartas, eliminação e vitória. As páginas foram renderizadas e conferidas visualmente; o OCR serve somente como auxílio.
- Tabela I e Tabela II do tabuleiro físico em [mapa_war_classico.webp](images/mapa_war_classico.webp).
- Esclarecimentos normativos do usuário, registrados na [matriz de rastreabilidade](war_rules_traceability_v1.0.md): fórmula de reforço também na primeira colocação, progressão das trocas após a 7ª, troca opcional com cinco cartas, descarte escolhido quando a carta de conquista elevar a mão a seis, defesa obrigatória com todos os dados permitidos até três e verificação imediata da vitória.
- A lista de adjacências está em [war_adjacency_review_v1.0.md](war_adjacency_review_v1.0.md) e [war_adjacency_candidate_v1.0.json](war_adjacency_candidate_v1.0.json). São 79 pares fornecidos pelo usuário, sem classificação por tipo de ligação nem auditoria visual independente de cada aresta.
- A preparação e as convenções da primeira rodada estão em [war_setup_spec_v1.0.md](war_setup_spec_v1.0.md).

Se o manual e uma instrução posterior do usuário divergirem para a edição-alvo, prevalece a instrução explícita do usuário, com a divergência registrada. Valores não determinados pelas fontes permanecem pendentes; protótipos do analyzer não servem como autoridade normativa.

## 1. Sequência do turno

A primeira rodada segue a [especificação da preparação](war_setup_spec_v1.0.md): atribuição dos territórios e exército inicial, seguida da colocação dos reforços iniciais; ataques começam somente na segunda rodada. A partir da segunda rodada, cada jogador, na sua vez, executa nesta ordem:

1. Recebe os reforços territoriais, de continente e de cartas; confere e, se optar, troca um conjunto de cartas no começo da vez.
2. Coloca os exércitos recebidos.
3. Ataca, se desejar, resolvendo uma batalha por vez.
4. Depois de encerrar os ataques, faz os deslocamentos finais permitidos, se desejar.
5. Se conquistou pelo menos um território na vez, recebe uma carta de território ao final, depois dos deslocamentos.
6. Passa a vez ao próximo jogador, salvo se a partida já terminou por vitória.

A troca deve ser decidida na janela inicial; a carta por conquista é recebida no fim do turno. As regras de mão com cinco/seis cartas e a diferença entre descarte escolhido e descarte por eliminação estão detalhadas na seção 3.

## 2. Reforços e colocação

### 2.1. Reforço por territórios

No começo da vez, conte os territórios atualmente controlados pelo jogador ativo, $T$, e calcule:

$$R(T)=\max\left(3,\left\lfloor\frac{T}{2}\right\rfloor\right).$$

A fórmula e o mínimo de três são confirmados pelo manual, p. 3, e pelo esclarecimento do usuário. Exemplos: $T=7\to3$, $T=8\to4$, $T=11\to5$. Um jogador eliminado não recebe turno; $T=0$ não é um caso para aplicar a fórmula.

### 2.2. Bônus continentais

Um continente só dá bônus quando o jogador controla todos os seus territórios **no início da vez**. Valores da Tabela I:

| Continente | Reforço |
|---|---:|
| América do Norte | 5 |
| Europa | 5 |
| Ásia | 7 |
| América do Sul | 2 |
| África | 3 |
| Oceania | 2 |

Cada exército de bônus continental deve ser colocado em território próprio daquele continente. Perder ou conquistar o último território de um continente durante a vez não altera retroativamente a reserva já recebida; a mudança será considerada no próximo início de vez. Para a primeira rodada, aplicar o bônus também é a convenção operacional adotada e identificada no passo 0.5, não uma exceção explicitamente descrita na p. 2.

### 2.3. De onde podem ser colocados os reforços

| Origem do reforço | Destino permitido |
|---|---|
| Contagem de territórios $R(T)$ | Qualquer território controlado pelo jogador. |
| Continente completo | Somente territórios próprios daquele continente. |
| Valor-base da troca de cartas | Qualquer território controlado pelo jogador. |
| +2 por carta trocada que represente território próprio | Obrigatoriamente o território dessa carta. |

Os reforços recebidos devem ser colocados conforme a estratégia do jogador; não há outro limite numérico de colocação indicado no manual. O bônus de território da carta é somado ao valor da Tabela II, não o substitui.

## 3. Trocas de cartas

### 3.1. Combinações válidas e valor global

Pode-se trocar exatamente três cartas com três símbolos iguais ou três símbolos diferentes. Um curinga pode representar qualquer uma das três figuras. As cartas usadas são retiradas da mão e colocadas à parte.

O valor da troca é contado **globalmente para a partida**, não por jogador. Tabela II do tabuleiro e esclarecimento do usuário:

| Número global da troca $n$ | Exércitos-base |
|---:|---:|
| 1 | 4 |
| 2 | 6 |
| 3 | 8 |
| 4 | 10 |
| 5 | 12 |
| 6 | 15 |
| 7 | 20 |
| $n\geq8$ | $20+5(n-7)$ |

Assim, a 8ª troca vale 25, a 9ª vale 30, e cada troca global posterior acrescenta mais cinco exércitos. O contador avança uma vez por conjunto entregue, independentemente de quem o trocou.

Para cada carta trocada que represente um território atualmente pertencente ao jogador, somam-se mais dois exércitos, obrigatoriamente naquele território (manual, pp. 7–8). Cada uma das três cartas é verificada separadamente.

### 3.2. Janela e obrigatoriedade — precedência do usuário

O manual, p. 7, diz que a troca não é obrigatória até quatro cartas, mas parece torná-la obrigatória ao chegar a cinco. Para o perfil WAR 1 deste projeto, prevalece a instrução posterior do usuário: **a troca com cinco cartas é opcional**. O conjunto pode ser trocado no começo da vez, antes da colocação e dos ataques. Não se força uma troca somente por a mão conter cinco cartas.

Ao conquistar território, recebe-se uma carta no fim da vez. Se essa compra elevar a mão de cinco para seis, o jogador deve escolher imediatamente uma carta da própria mão para descartar, ficando com cinco. Esse descarte à escolha é a regra-alvo informada pelo usuário; não confundi-la com o descarte aleatório por eliminação descrito no manual.

### 3.3. Eliminação e reciclagem de cartas

Quando um jogador elimina outro, recebe as cartas da mão eliminada, salvo se a eliminação cumprir seu próprio objetivo de eliminar aquela cor e encerrar a partida. Se a transferência elevar a mão do eliminador para mais de cinco, o manual, p. 8, manda retirar cartas **sem olhar**, aleatoriamente, até ficar com cinco. Isso é diferente do descarte à escolha após uma carta de conquista elevar uma mão de cinco a seis.

As cartas entregues em trocas ficam à parte; quando o monte de compra se esgota, são recolhidas, embaralhadas e formam um novo monte (manual, p. 8). O texto do manual não determina se as cartas descartadas pelo limite de mão — à escolha após a compra ou aleatoriamente após eliminação — também entram nesse monte reciclável. Manter esse destino em campo separado e não misturá-las silenciosamente com as cartas trocadas até decisão normativa; esse detalhe bloqueia uma implementação canônica da reciclagem quando essas cartas existirem.

## 4. Ataques, dados e batalha

### 4.1. Início e sequência de ataques

- Ataques são permitidos a partir da segunda rodada.
- O território de origem deve ser do atacante e conter pelo menos dois exércitos: um permanece como exército de ocupação e não pode participar do ataque.
- O alvo deve pertencer a um adversário e ser contíguo ao território de origem. O manual, p. 3, define a contiguidade de ataque como fronteira comum **ou** ligação por linha pontilhada. A quantidade de exércitos defensores não impede que o território seja atacado.
- O atacante declara origem, destino e quantos exércitos participam. Pode escolher de um até três, limitado a deixar a ocupação na origem. Cada exército participante corresponde a um dado vermelho, até o máximo de três.
- Podem ocorrer várias batalhas na mesma vez, a partir de uma ou mais origens, mas resolve-se uma de cada vez. O jogador pode encerrar os ataques quando quiser.

### 4.2. Dados de defesa e resolução

A regra do manual limita cada lado a no máximo três exércitos/dados participantes. O esclarecimento do usuário fixa a quantidade defensiva: o defensor usa obrigatoriamente um dado por exército presente no território, até três:

$$D=\min(\text{exércitos defensores},3).$$

O atacante escolhe a quantidade de exércitos participantes, de 1 a 3, sem usar o exército de ocupação. O defensor pode usar o exército de ocupação e não escolhe reduzir a quantidade de dados sob o perfil confirmado pelo usuário. Dados vermelhos são do atacante; amarelos, da defesa.

Ordene cada conjunto do resultado maior para o menor e compare os dados por posição, do maior para o maior. Para cada par comparado, quem tiver o menor resultado perde um exército; empate favorece a defesa. Dados sem par correspondente não causam perda. Exemplo textual do manual, p. 4: ataque 5, 4, 1 contra defesa 6, 3, 1 dá duas perdas ao atacante e uma à defesa. Os exércitos perdidos retornam às caixas dos jogadores e podem ser reutilizados (p. 5).

Cada rolagem resolve uma confrontação. Se ambos continuam com exércitos no território, o atacante decide se realiza outra batalha ou para. Não há conversão de uma rolagem em várias rodadas automáticas de combate.

## 5. Conquista, continuidade e eliminação

Quando todos os exércitos defensores de um território são destruídos, o atacante conquista esse território e deve transferir para ele pelo menos um exército, no máximo o número de exércitos participantes do **último ataque** (manual, p. 6); a origem conserva seu exército de ocupação. A escolha do número respeita também os exércitos ainda disponíveis na origem.

Durante a fase de ataques, a movimentação permitida é a transferência dos atacantes para o território que acabou de ser conquistado; não é permitido aproveitar essa fase para deslocar exércitos para outro território qualquer. Após ocupar a conquista, o atacante pode iniciar outro ataque, inclusive a partir do território recém-conquistado, ainda na mesma vez (p. 6). A transferência obrigatória de captura não é a movimentação final descrita na p. 7 e tem seu próprio limite.

Um jogador é eliminado quando seus exércitos são destruídos por completo. As consequências são:

1. Se a eliminação satisfaz o objetivo de eliminar a cor do atacante, a vitória do atacante encerra a partida; ele não recebe a mão como prêmio (manual, p. 8; objetivos físicos).
2. Caso contrário, o atacante recebe as cartas do eliminado; se ficar com mais de cinco, escolhe-se aleatoriamente, sem olhar, o necessário para voltar a cinco (manual, p. 8).
3. Se outra pessoa detinha o objetivo de eliminar a cor eliminada, aplica-se o fallback impresso na carta: o objetivo muda para conquistar 24 territórios. Isso vale mesmo quando o eliminador não é o titular daquela missão; as implementações hardcoded do analyzer são excluídas como fonte (cartas físicas e esclarecimento do usuário).
4. Atualizam-se posse, contagem de territórios e objetivos antes de oferecer a próxima decisão. A condição de vitória é verificada imediatamente conforme a seção 7.

## 6. Deslocamento final

Depois de declarar encerrados os ataques, o jogador pode, se desejar, deslocar exércitos entre territórios próprios contíguos (manual, p. 7). Regras identificadas no texto e exemplo:

- Deve permanecer em cada território pelo menos um exército de ocupação; esse exército não pode ser deslocado.
- Um mesmo exército pode ser deslocado uma única vez nessa fase/vez. Não se pode mover uma unidade de A para B e depois essa mesma unidade de B para C na mesma jogada. Isso não limita as demais unidades que não foram movidas.
- O deslocamento final é diretamente entre territórios contíguos. Podem ser feitas transferências distintas com exércitos ainda não movidos; o manual não define um número máximo global de transferências além dessas restrições.
- A regra de uma movimentação por exército nesta seção é diferente da transferência de atacantes para território recém-conquistado durante o combate.

**Convenção operacional sobre contiguidade de deslocamento:** o manual usa “territórios contíguos” na p. 7 sem repetir a definição de fronteira/linha pontilhada que dá para ataques na p. 3. A especificação trata cada ligação direta da lista de adjacências do usuário como elegível também para esse deslocamento, inclusive as linhas pontilhadas. O arquivo atual não classifica as arestas; essa aplicação comum do grafo deve ser revista antes de certificar uma engine contra uma transcrição física independente.

Não foram encontrados no manual suporte para movimento de vários passos através de territórios intermediários, movimento por território de adversário, remoção do último exército de um território, ou reutilização da mesma unidade no movimento final. Não adicionar essas regras.

## 7. Compra de carta e encerramento do turno

Após concluir o deslocamento final, se o jogador conquistou um ou mais territórios durante a vez, recebe **uma única carta de território**, não uma carta por conquista. O conteúdo fica secreto até a troca (manual, p. 7). Sem conquista, não recebe carta. Depois da compra, aplica-se o descarte escolhido para evitar que a mão chegue a seis, conforme a regra do usuário na seção 3.2.

Se o monte se esgotar, a regra explícita da p. 8 recicla as cartas anteriormente trocadas. O destino separado das cartas descartadas por limite de mão continua pendente; não as tratar como cartas trocadas sem confirmação.

## 8. Verificação de objetivo e vitória

O manual, p. 8, diz que o jogo termina quando um jogador atinge seu objetivo e que, nesse momento, deve mostrar sua carta para comprovar a vitória. O usuário determinou verificação **imediata** após qualquer ação que possa satisfazer um objetivo, inclusive nas fases de reforço, ataque e movimentação. No perfil do projeto:

- Conferir os objetivos secretos de todos os jogadores ativos após cada ação de colocação de exércitos, resolução de batalha/conquista, eliminação/fallback e transferência de movimento, incluindo os efeitos automáticos dessa ação.
- Não esperar até o fim da vez. Se a condição for satisfeita, interromper antes de oferecer outra decisão, fase ou carta de fim de turno; o vencedor revela sua missão.
- Se a eliminação pelo atacante satisfizer sua missão de eliminar aquela cor, encerrar em vez de transferir as cartas do eliminado.
- Uma missão de eliminação de cor convertida para conquistar 24 deve passar a ser avaliada como esse novo objetivo imediatamente após o evento que causou a conversão.
- O árbitro pode avaliar missões privadas, mas não deve expor objetivo ou estado oculto de outros jogadores antes de uma vitória ser anunciada.

**Granularidade operacional:** cada colocação de tropas, rolagem/resolução de batalha com suas consequências obrigatórias e transferência final de exércitos é uma ação atômica. A checagem ocorre após todas as consequências automáticas dessa ação e antes da próxima decisão. Se uma operação futura agrupar várias colocações ou movimentos, deverá preservar checagem entre as ações constituintes, em vez de adiar a vitória para o fim da fase.

**Vitórias simultâneas — sem desempate normativo identificado:** uma única ação pode alterar a missão de eliminação de uma pessoa para “conquistar 24 territórios” ao mesmo tempo que completa outro objetivo. O manual e o esclarecimento do usuário exigem vitória imediata, mas não indicam prioridade para duas missões que passem a ser verdadeiras na mesma transição. A engine não deve escolher um vencedor por ordem de lista, cor ou implementação acidental; deixar o estado como conflito de adjudicação até decisão do usuário/regra de referência. Esse ponto é bloqueante para certificar o encerramento em 100% dos estados.

## 9. Pontos que ainda requerem revisão

| Ponto | Evidência atual | Estado/impacto |
|---|---|---|
| Vitória simultânea em uma mesma ação | Sem desempate no manual nem instrução do usuário; seção 8. | **Pendente e bloqueante** para certificação total do término. |
| Ligações pontilhadas no movimento final | P. 7 fala em contíguos; p. 3 define linha pontilhada para ataque; a lista de adjacências não tipa arestas. | **Convenção operacional**: usar toda adjacência direta do grafo no movimento. Revisar com mapa/regras antes de homologar. |
| Reciclagem dos descartes por limite de mão | P. 8 recicla explicitamente cartas trocadas; não menciona descartes aleatórios da eliminação nem descarte escolhido após compra. | **Pendente**: mantê-los distintos da pilha de cartas trocadas; decidir reutilização antes de certificar o ciclo do baralho. |
| Revisão independente e testes | Engine ainda não implementada; não há testes de transição no checkout. | **Pendente** para certificação executável; este arquivo é uma especificação, não um certificado de código. |

## Resultado do passo 0.6

O ciclo normal de reforço, troca, combate, conquista, deslocamento, compra de carta, eliminação e vitória está extraído e especificado, incluindo os esclarecimentos explícitos do usuário e as divergências do manual. O passo 0.6 está **concluído documentalmente**, com a ressalva de que a certificação normativa integral permanece aberta para os pontos da seção 9. Não foi alterado código nem criada suíte de testes; validar uma implementação pertence a fases posteriores. Por decisão do usuário, a Fase 0 está concluída por ora; os passos 0.7 e 0.8 serão retomados durante o futuro desenvolvimento do cliente de jogo do `war_analyzer`, antes da certificação das integrações online e física.
