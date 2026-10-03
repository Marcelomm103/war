## Plano: Roadmap técnico WAR v1.0

A recomendação é desenvolver **um simulador certificado como fonte única das regras**, uma **plataforma de pesquisa de IA multiagente** e **dois clientes de execução**: site Grow e tabuleiro físico. A evolução será determinada por testes e critérios de aprovação, não por prazos ou quantidade arbitrária de treinamento.

**Status de execução (2026-10-03):** por decisão do usuário, a Fase 0 é considerada concluída por ora no escopo de planejamento e documentação: os passos 0.1–0.6 estão documentados. A lista do passo 0.4 foi validada estruturalmente a partir dos dados fornecidos pelo usuário, sem auditoria visual independente. O passo 0.5 inclui três convenções operacionais sujeitas à revisão; o passo 0.6 permanece documental e registra lacunas normativas para resolver antes da certificação integral da engine. Os passos 0.7 e 0.8 estão adiados para o futuro desenvolvimento do cliente de jogo do `war_analyzer`; não são considerados executados nem certificados. Essa decisão não equivale a certificação do canal online/físico ou de uma implementação.

---

# 1. Premissas e definição da versão 1.0

Como não houve disponibilidade para responder às perguntas de alinhamento, adotam-se estas premissas, sujeitas à revisão:

- Suportar a edição física identificada no manual fornecido e todas as quantidades de jogadores autorizadas por ele. **Mesas de 3–6 jogadores são a premissa inicial**, ainda dependente da certificação do manual.
- Usar o manual como autoridade para o jogo físico. Diferenças comprovadas do site terão **perfis de regras separados e versionados**.
- Usar uma PWA no celular, com processamento de visão e inferência em computador/servidor local ou remoto.
- Priorizar câmera fixa e calibrada. Permitir recapturas e correções manuais quando houver oclusão, dúvida ou informação que a câmera não consiga observar.
- Tornar obrigatórias a **saída por voz**, a interface textual e as confirmações por botões. Reconhecimento de voz será opcional.
- Automatizar o site somente em condições autorizadas. A integração não dependerá de contornar proteções ou acessar informações privadas de outros jogadores.
- Interpretar “melhor IA possível” como **a melhor solução sustentada pela pesquisa e pelos benchmarks documentados**, sem afirmar ótimo global ou invencibilidade.

A v1.0 incluirá:

1. Simulação completa, sem interface gráfica, para treinamento e avaliação.
2. Um humano contra instâncias da mesma IA ou contra modelos diferentes.
3. Treinamento por RL, comparação de abordagens e liga de adversários.
4. Cliente capaz de jogar no site.
5. Cliente capaz de acompanhar o tabuleiro físico e orientar a execução humana.
6. Homologação científica da força da IA e operacional dos clientes.

---

# 2. Situação atual encontrada

| Componente | Situação verificada |
|---|---|
| `war_game_engine` | Apenas descrição; não foi encontrada implementação da simulação. |
| `war_AI` | Apenas descrição e licença; não foram encontrados agentes, treinamento ou avaliação. |
| `war_analyzer` | Protótipos Python de captura, identificação de cores, OCR e calibração. |
| Infraestrutura | Não foram encontrados manifests de dependências, testes automatizados ou CI nas buscas realizadas. |
| Manual | PDF de oito páginas baseadas em imagens; exige OCR e conferência visual. As regras ainda não foram extraídas nesta sessão. |

O analisador existente é material para reaproveitamento, **não uma fonte normativa das regras nem um componente já homologado**. Foram identificados pontos que precisarão de caracterização e correção:

- OCR pode devolver `0` quando falha.
- Cor desconhecida pode ser representada como `"neutral"`.
- Coordenadas e paletas estão fixadas.
- Há inicialização com acesso a arquivos e possível encerramento do processo durante importação.
- `create_cards()` contém entradas duplicadas/inconsistentes.
- Objetivos e dados de territórios estão hardcoded, sem certificação contra o manual.

---

# 3. Arquitetura proposta

## 3.1. Responsabilidades dos submódulos

### `war_game_engine`

Será responsável por:

- Regras e dados canônicos por edição/perfil.
- Estado completo do simulador.
- Observação permitida a cada jogador.
- Validação e aplicação de ações.
- Resolução de dados e outros eventos aleatórios.
- Preparação, turnos, cartas, objetivos, eliminações e vitória.
- Snapshots, replays e execução determinística a partir de sementes.
- Protocolo genérico de agente e runner headless.
- CLI para um humano contra agentes configuráveis.

**Não dependerá de câmera, navegador, servidor web ou bibliotecas de redes neurais.**

### `war_AI`

Será responsável por:

- Adaptadores de ambiente RL sobre a engine.
- Codificação de observações e ações.
- Agentes heurísticos e neurais.
- Algoritmos de aprendizado.
- Currículo, self-play, liga e treinamento de melhores respostas.
- Busca com informação imperfeita.
- Experimentos, avaliação e seleção dos modelos.
- Exportação e execução das políticas treinadas.

### `war_analyzer`

Será responsável por:

- Captura do site e da câmera.
- Percepção e tratamento da incerteza.
- Rastreamento do estado observado.
- Clientes online e físico.
- Serviço de sessões.
- PWA, voz, ACK e correção manual.
- Conversão de ações semânticas em comandos externos.
- Verificação do resultado das ações executadas.

**Não conterá outra implementação independente das regras.**

### Repositório agregador

Conterá documentação, configuração de integração, instalação, orquestração, containers e testes entre submódulos.

---

## 3.2. Contratos fundamentais

| Contrato | Conteúdo e restrições |
|---|---|
| `RulesetSpec` | Edição, versão, mapa, baralhos, objetivos, fases, fórmulas e regras certificadas. |
| `FullGameState` | Estado verdadeiro do simulador/árbitro, incluindo informações privadas atuais. Nunca fornecido diretamente ao ator. |
| `PublicGameState` | Apenas informações públicas da partida. |
| `PlayerObservation` | Estado público, objetivo e cartas próprios, histórico permitido e interface de ações legais. |
| `ObservedBoard` | Evidência da visão: valores conhecidos/desconhecidos, confiança, origem, tempo e regiões de imagem. |
| `PlayerKnowledgeState` | Fatos conhecidos pelo jogador, separados de hipóteses. |
| `BeliefState` | Distribuição sobre informações ocultas compatíveis com o histórico. |
| `Action` | Ação semântica tipada, independente de pixels, voz ou framework RL. |
| `ChanceRequest` / `ChanceOutcome` | Separação entre decisões e resultados aleatórios. |
| `GameEvent` / `Snapshot` | Histórico auditável, versões, visibilidade e hashes de estado. |
| `AgentProtocol` | Inicialização, decisão, memória por jogador, RNG próprio e orçamento de inferência. |
| `ActionIntent` / `ExecutionReceipt` / `Ack` | Identificação do comando, versão esperada do estado, execução e evidências. |
| `PolicyManifest` | Pesos, versões, codificadores, configuração de busca, amostragem e compatibilidade. |

### Regras de isolamento

- O ator não poderá acessar objetivos/cartas alheios, próximo dado, sementes internas ou ordem futura do baralho.
- Um crítico privilegiado poderá usar informações privadas atuais **somente durante treinamento**, em experimentos separados. Não receberá resultados futuros de aleatoriedade.
- Busca utilizará estados hipotéticos amostrados de crenças, não o estado oculto verdadeiro.
- Instâncias da mesma rede poderão compartilhar pesos, mas **não memória recorrente, cartas, objetivos ou RNG de política**.
- No jogo externo, informações desconhecidas permanecerão desconhecidas. Não serão inventadas para preencher um estado completo.
- Logs, caches, API, replays e áudio respeitarão a mesma separação de informações.

---

# 4. Organização das fases

| Fase | Objetivo | Dependências |
|---|---|---|
| 0 | Regras documentadas (0.1–0.6); canais online/físico adiados (0.7–0.8) | Nenhuma |
| 1 | Infraestrutura e contratos | Descoberta da fase 0 |
| 2 | Núcleo, tabuleiro e preparação | 0–1 |
| 3 | Regras completas e conclusão das partidas | 2 |
| 4 | Certificação da engine e modo humano | 3 |
| 5 | Ambiente RL, ações, baselines e arena | 4 |
| 6 | Primeiro agente RL | 5 |
| 7 | Comparação de arquiteturas e algoritmos | 6 |
| 8 | Liga e resistência à exploração | Primeiros modelos de 6–7 |
| 9 | Busca e seleção do candidato | Engine certificada e modelos; seleção final após 8 |
| 10 | Analyzer comum e rastreamento | Contratos; regras públicas para consolidação |
| 11 | Cliente online | Autorização/perfil, engine e analyzer |
| 12 | Visão física | Domínio físico, contratos e analyzer |
| 13 | PWA, voz e ACK | Analyzer; visão/política para integração final |
| 14 | Homologação e release | Todas as entregas obrigatórias |

**Paralelismo:** captura, anotação de dados, PWA e investigação do site poderão avançar enquanto a IA é desenvolvida. O treinamento amplo, entretanto, ficará bloqueado até a certificação da engine.

---

# 5. Fases e passos técnicos

## Fase 0 — Certificação normativa e viabilidade (encerrada por ora no escopo documental)

**Objetivo:** impedir que a IA aprenda uma aproximação incorreta do WAR.

### 0.1. Inventariar fontes e versões

- Registrar os commits dos três submódulos e os assets disponíveis.
- Calcular hashes dos dois exemplares do manual.
- Confirmar se são cópias idênticas e estabelecer um exemplar principal.
- Identificar edição do tabuleiro, cartas, peças e eventuais diferenças físicas.
- Separar licença do código de direitos sobre manual, imagens, tabuleiro e pesos de terceiros.

#### Registro de execução — 2026-10-02

**Escopo desta verificação:** inventário de arquivos, referências Git, licenças e metadados; não houve OCR nem revisão do conteúdo normativo, reservados ao passo 0.2.

| Repositório | Branch/commit verificado | Estado da árvore de trabalho |
|---|---|---|
| Agregador `war` | `main` / `04a813ccd1f00dd0a7477e5bc4d0ec551ae3a782` | Limpa |
| `war_AI` | `main` / `67d6d8707b44ba74f7b594c5b6fedf395fb6bcdd` | Limpa |
| `war_game_engine` | `main` / `cc13350f9b4f9aedd08ba082d14f6774b391678c` | Limpa |
| `war_analyzer` | `main` / `93823505b2533cd9ff49d005cf4a44223bdc2f84` | Limpa |

Os dois arquivos abaixo têm 1.973.576 bytes cada e o mesmo SHA-256 (`1969b38acdbfe0ccd761c91995988e96cef5d2acfc5aea5abecebcaecc6e394c`); a comparação byte a byte também confirmou que são idênticos. Fica estabelecido como exemplar principal o [manual do agregador](war_manual_table_games.pdf). A cópia mantida no submódulo `war_analyzer` permanece como duplicata; não foi removida.

- [doc/war_manual_table_games.pdf](war_manual_table_games.pdf)
- [lib/war_analyzer/doc/war_manual_table_games.pdf](../lib/war_analyzer/doc/war_manual_table_games.pdf)

O manual tem oito páginas. A capa identifica “Regras — O jogo da estratégia WAR” e exibe a marca Grow. Os metadados do PDF indicam processamento pelo Adobe Acrobat 7.0 Image Conversion Plug-in em 2006; isso não identifica a data de publicação, a edição ou a revisão do jogo.

**Identificação e hierarquia de fontes informadas pelo usuário (2026-10-02):** as versões física e digital alvo são WAR 1 clássico. Para os objetivos, deve prevalecer a referência da versão física; os protótipos existentes de `war_analyzer` não são normativos e podem estar incorretos, devendo ser corrigidos posteriormente contra essa referência. A indicação do usuário fixa a autoridade funcional, mas não autentica por si só o ano/revisão ou os direitos de distribuição dos arquivos.

Há 513 imagens em `war_analyzer/image`, incluindo os screenshots digitais [war_ss_1.png](../lib/war_analyzer/image/war_ss_1.png) e [war_reference_ss_1.png](../lib/war_analyzer/image/war_reference_ss_1.png), ambos do site `play.wargrow.com.br`, [anchor_template.png](../lib/war_analyzer/image/anchor_template.png) e imagens de depuração. **Assets de referência física/digital indicados pelo usuário em 2026-10-02:** o diretório [doc/images](images) contém a imagem do tabuleiro [mapa_war_classico.webp](images/mapa_war_classico.webp) (1500 × 1125) e oito folhas de cartas em PNG (877 × 612 cada), de [war_cartas1.png](images/war_cartas1.png) a [war_cartas8.png](images/war_cartas8.png). O usuário determinou que a referência física WAR 1 é normativa para objetivos e que os protótipos de `war_analyzer` não devem prevalecer. As imagens mostram 42 cartas de território, dois curingas, 14 objetivos e as tabelas impressas. Não há imagem das peças físicas nem metadados independentes que autentiquem ano/revisão ou direitos de distribuição. Também não foram encontrados arquivos de pesos/modelos nos formatos usuais pesquisados (`.pt`, `.pth`, `.onnx`, `.safetensors`, `.ckpt`, `.bin`, `.h5`, `.pb` ou `.model`).

Quanto às licenças, [LICENSE](../LICENSE), [lib/war_AI/LICENSE](../lib/war_AI/LICENSE) e [lib/war_analyzer/LICENSE](../lib/war_analyzer/LICENSE) declaram MIT. Não foi encontrado arquivo de licença próprio em `war_game_engine`; não se presume que a licença do agregador se estenda ao submódulo. Essas licenças de código não estabelecem direitos sobre o manual, a marca/arte do jogo, imagens do produto ou do site. Nenhuma autorização separada para esses materiais foi localizada.

**Resultado do passo 0.1: concluído com ressalvas.** Os commits, o inventário digital, os hashes e o exemplar principal estão verificados; a versão alvo e a precedência normativa das referências físicas foram informadas pelo usuário, e mapa/cartas foram localizados em `doc/images`. Permanecem sem autenticação independente o ano/revisão e os direitos de uso/distribuição dos materiais não codificados; as peças físicas não estão representadas nas imagens disponíveis.

### 0.2. Extrair e revisar o manual

- Extrair/renderizar as páginas do PDF preservando a resolução disponível.
- Aplicar OCR em português.
- Conferir visualmente todas as regras, exemplos, números, tabelas e diagramas.
- Não considerar aumento de resolução como recuperação de detalhes inexistentes.
- Obter uma reprodução legível da mesma edição quando necessário.
- Não preencher lacunas por conhecimento de Risk.

#### Registro de execução — 2026-10-02

**Método e qualidade da fonte**

- Fonte revisada: [manual WAR do agregador](war_manual_table_games.pdf), oito páginas, SHA-256 `1969b38acdbfe0ccd761c91995988e96cef5d2acfc5aea5abecebcaecc6e394c`.
- O PDF não tem camada de texto extraível; cada página é um scan em imagem, com resolução original de aproximadamente 668–675 × 908–915 pixels (72 ppi). As páginas foram renderizadas nessa resolução nativa.
- OCR: Tesseract 4.1.1, idioma português (`por`), modelo `tessdata_best` cujo SHA-256 é `711de9dbb8052067bd42f16b9119967f30bada80d57e2ef24f65d09f531adb04`; segmentação automática de página (`--psm 3`). O OCR teve erros de leitura e ordem de colunas, em especial em ilustrações; não foi tratado como autoridade. O texto abaixo é uma síntese conferida visualmente, não uma transcrição corrigida palavra por palavra.
- Os diagramas foram ampliados somente para inspeção. A ampliação não aumenta a resolução nem recupera informação ausente do scan.
- Foi localizada uma cópia pública no [site TableGames](https://tablegames.com.br/wp-content/uploads/2017/10/war_manual_table_games.pdf). O hash é idêntico ao arquivo local; portanto, essa cópia não oferece resolução ou conteúdo adicional.
- As oito páginas foram inspecionadas visualmente e comparadas ao OCR.

**Conteúdo conferido por página (síntese)**

| Página | Conteúdo normativo identificado |
|---|---|
| 1 | Introdução; objetivo individual secreto. |
| 2 | Componentes: tabuleiro, seis conjuntos de exércitos, seis caixas, 14 cartas-objetivo, 44 cartas de território com dois curingas e seis dados (três vermelhos e três amarelos). Ficha pequena vale um exército; grande, dez. Cores listadas: branca, vermelha, preta, azul, amarela e verde. Cada jogador recebe um objetivo secreto; objetivos que dependam de cores não participantes devem ser retirados. O distribuidor tira os curingas do baralho e distribui as cartas de território no sentido horário, começando à sua esquerda. Coloca-se um exército da própria cor em cada território recebido; ao fim, todos estão ocupados. Os curingas voltam ao baralho e as cartas são embaralhadas. Conforme esclarecimento do usuário, o distribuidor é escolhido pelo maior resultado de dado; empate é resolvido por novo arremesso entre os empatantes, que determina quem começa, e a ordem dos demais segue no sentido horário da mesa. A primeira rodada consiste em receber e posicionar exércitos; da segunda em diante, a ordem do turno é receber/posicionar reforços, atacar, deslocar e receber carta se conquistou território. O primeiro a reforçar é o jogador seguinte àquele que recebeu a última carta de território, seguindo a ordem horária da mesa. |
| 3 | Reforços: metade inteira do número de territórios, mínimo de três mesmo com menos de seis territórios (exemplos: oito dão quatro; 11 dão cinco); bônus por continente inteiro conforme Tabela I do tabuleiro, colocados obrigatoriamente no próprio continente. Exemplo: 19 territórios dão nove reforços básicos; América do Sul controlada dá mais dois, total 11, dos quais os dois continentais devem ir à América do Sul. Trocas de cartas também podem conceder reforços. Ataques começam na segunda rodada: origem com pelo menos dois exércitos; alvo adversário contíguo por fronteira ou linha pontilhada, independentemente do número de exércitos que o ocupa; qualquer número de ataques na vez, mas um por vez, possivelmente partindo de origens diferentes; declarar origem, alvo e exércitos usados; máximo de três participantes/dados por batalha. O atacante usa dados vermelhos e o defensor amarelos; o defensor pode usar o exército de ocupação. |
| 4 | Continuação das regras de ataque e comparação decrescente dos dados (maior com maior, segundo com segundo, terceiro com terceiro); cada par dá uma perda a quem tiver o menor resultado, e empate favorece a defesa. Cada lado lança tantos dados quantos exércitos participarão da batalha, até três. Exemplo: atacante com quatro exércitos e defensor com três usam três dados cada; atacante 5, 4, 1 contra defesa 6, 3, 1 resulta em duas perdas do atacante e uma da defesa. A ilustração mostra três dados vermelhos do México contra um amarelo de Nova York. |
| 5 | Exemplo: atacante com três exércitos usa dois dados contra um defensor; ataque 3, 2 contra defesa 6 faz o atacante perder um. A nota diz que cada vez que o atacante perde, perde o número de exércitos com que a defesa se defendeu. Para 10 contra 4, o texto descreve uma vitória do ataque e duas da defesa, deixando 8 contra 3; essa contabilidade é coerente com uma perda do defensor e duas do atacante. |
| 6 | Continuação: em nova batalha de três dados contra três, o exemplo termina com três vitórias do ataque e remoção dos três últimos exércitos defensores. A conquista ocorre quando o defensor perde todos os exércitos; o atacante transfere de um a, no máximo, tantos exércitos quanto participaram do último ataque e pode atacar novamente a partir do território conquistado. Deslocamentos durante ataques só para territórios atacados. |
| 7 | Movimento final entre territórios próprios contíguos: deixar ao menos um exército em cada território e não mover o mesmo exército novamente na mesma jogada. Exemplo: unidades do Brasil podem ir à Venezuela, mas essas mesmas unidades não podem seguir para o México na mesma jogada. Ao conquistar pelo menos um território, recebe-se uma carta no fim da jogada, após os deslocamentos; recebe-se no máximo uma por jogada e seu conteúdo fica secreto até a troca. Trocam-se três símbolos iguais ou três diferentes, pelos valores da Tabela II; as três primeiras trocas dão 4, 6 e 8 exércitos. Não é obrigatório trocar com até quatro cartas; com cinco, a troca de três é obrigatória na vez. Cada carta trocada que represente território próprio dá mais dois exércitos, obrigatoriamente nesse território. |
| 8 | Curinga pode representar qualquer símbolo. Cartas trocadas ficam à parte e, quando o monte se esgota, são recolhidas, embaralhadas e recolocadas. Ao eliminar um jogador, recebem-se suas cartas; se isso elevar a mão acima de cinco, descarta-se aleatoriamente até cinco. Se o jogador eliminado era o objetivo de eliminação do atacante, este vence em vez de receber as cartas. Vitória ao cumprir o objetivo e revelar a carta. Traz resumo do turno. |

**Complemento de evidências — mapa e cartas fornecidos pelo usuário**

Foram examinadas a imagem do tabuleiro [mapa_war_classico.webp](images/mapa_war_classico.webp) (1500 × 1125) e as oito folhas de cartas [war_cartas1.png](images/war_cartas1.png), [war_cartas2.png](images/war_cartas2.png), [war_cartas3.png](images/war_cartas3.png), [war_cartas4.png](images/war_cartas4.png), [war_cartas5.png](images/war_cartas5.png), [war_cartas6.png](images/war_cartas6.png), [war_cartas7.png](images/war_cartas7.png) e [war_cartas8.png](images/war_cartas8.png) (877 × 612 cada). A inspeção foi visual, com OCR apenas auxiliar; em especial, o OCR da foto do mapa não leu as tabelas de forma confiável. A ampliação de regiões foi feita somente para inspeção e não recupera detalhe ausente. Os arquivos chegaram ao workspace nesta etapa, aparecem como não versionados no agregador e ainda não têm procedência, data ou edição autenticadas por documentação independente.

As folhas apresentam **42 cartas de território, dois curingas e 14 cartas de objetivo**, compatíveis em quantidade com a lista de componentes do manual. A foto do mapa torna legíveis as tabelas impressas:

| Tabela do tabuleiro | Valores lidos na imagem |
|---|---|
| I — bônus por continente | América do Norte: +5; Europa: +5; Ásia: +7; América do Sul: +2; África: +3; Oceania: +2 exércitos. |
| II — troca de cartas | 1ª troca: +4; 2ª: +6; 3ª: +8; 4ª: +10; 5ª: +12; 6ª: +15; 7ª: +20. Conforme esclarecimento do usuário, a partir da 8ª troca aumenta cinco por troca: 8ª: +25; 9ª: +30; 10ª: +35; 11ª: +40; e assim sucessivamente. |

**Esclarecimentos normativos do usuário — 2026-10-02 (WAR 1 clássico)**

- Reforço inicial e reforço na fase normal: para $T$ territórios controlados, o total disponível para colocar é $R(T)=\max(3,\lfloor T/2\rfloor)$. Assim, 8 territórios dão 4 exércitos; 11 dão 5; 7 dão 3. O mínimo de três também se aplica na colocação inicial. A regra é registrada conforme o esclarecimento do usuário; o manual escaneado descreve explicitamente a metade inteira e o mínimo de três para reforços do turno, mas não detalha separadamente a reserva da primeira colocação.
- Progressão da Tabela II: a partir da 8ª troca, acrescentar cinco exércitos por troca, conforme valores acima; para número da troca $n\geq8$, $B(n)=20+5(n-7)$.
- Ordem de preparação e primeiro reforço: conforme esclarecimento do usuário, o maior resultado escolhe o distribuidor; em caso de empate, somente os empatantes fazem novo arremesso de dado, que decide quem começa primeiro. A partir desse jogador, a ordem da mesa segue no sentido horário. Depois da distribuição dos territórios, o primeiro jogador a reforçar é o próximo após quem recebeu a última carta de território; a sequência também segue no sentido horário.
- IDs territoriais sul-americanos: usar o nome impresso na carta como ID canônico — **Colômbia** para a área rotulada Colômbia/Venezuela e **Bolívia** para a área rotulada Bolívia/Peru/Chile. Venezuela, Peru e Chile são aliases/rótulos cartográficos, não territórios ou IDs adicionais.
- Objetivos: usar a referência física WAR 1 (as cartas em `doc/images`) como normativa; não usar os objetivos hardcoded nos protótipos atuais de `war_analyzer` como fonte. As diferenças já encontradas nos protótipos são defeitos a corrigir posteriormente, não uma ambiguidade das regras físicas. A regra de fonte não implica que o comportamento de `play.wargrow.com.br` já tenha sido certificado como idêntico.

As 14 cartas de objetivo visíveis na referência física são: destruir os exércitos vermelhos, azuis, brancos, pretos, amarelos ou verdes (com conversão para conquistar 24 territórios nas condições impressas); conquistar América do Norte e Oceania; Ásia e América do Sul; Ásia e África; América do Norte e África; Europa, América do Sul e mais um continente à escolha; Europa, Oceania e mais um continente à escolha; conquistar 24 territórios à escolha; ou conquistar 18 territórios e ocupar cada um com pelo menos dois exércitos. Essa lista vem das imagens das cartas, não da camada textual do PDF, e prevalece sobre os protótipos existentes.

**Resolução de precedência entre fontes:** por decisão informada pelo usuário, para o WAR 1 físico as cartas e o mapa de referência física são normativos. Portanto, os objetivos “Europa + Oceania + terceiro continente”, as cores de eliminação (branca/preta, não cinza/roxa) e os IDs territoriais “Colômbia” e “Bolívia” são os valores a implementar. Os protótipos hardcoded em [war_analyzer.py](../lib/war_analyzer/src/war_analyzer.py), [war_analyzer_gemini.py](../lib/war_analyzer/src/war_analyzer_gemini.py) e [war_analyzer_resumed.py](../lib/war_analyzer/src/war_analyzer_resumed.py) não alteram essa fonte de verdade e precisam de correção em etapa posterior. Os rótulos Venezuela/Peru/Chile não criam territórios adicionais. A transcrição completa de adjacências fica para o passo 0.4.

**Lacunas e ambiguidades encontradas — manter sem inferência**

1. A primeira colocação e a ordem para escolher o distribuidor/começar a reforçar estão registradas conforme os esclarecimentos do usuário acima. A regra de desempate não aparece legível no manual disponível; mantém-se como confirmação normativa do usuário para a edição alvo.
2. Bônus continentais e progressão da Tabela II estão registrados acima a partir do mapa e do esclarecimento do usuário; devem ser preservados com rastreabilidade na matriz do passo 0.3.
3. A nomenclatura combinada e a precedência das cartas físicas sobre os protótipos estão resolvidas conforme o usuário. As ligações/contiguidades e IDs do tabuleiro ainda não foram transcritos integralmente como grafo validado; isso permanece para o passo 0.4.
4. No exemplo de 10 contra 4 da página 5, o resultado narrado (uma vitória do ataque, duas da defesa; 8 contra 3) é coerente com a regra de perdas. A legibilidade das faces do diagrama é limitada; os valores específicos dos dados não serão usados como base independente além do que puder ser lido diretamente.
5. A escolha obrigatória dos dados defensivos está definida pelo esclarecimento posterior do usuário e registrada na matriz do passo 0.3. A semântica do deslocamento de grupos de exércitos ainda precisa ser formalizada sem exceder o que os exemplos garantem.

**Resultado do passo 0.2: revisão do manual, complemento visual e esclarecimentos do usuário registrados, com limitações de procedência/resolução.** As oito páginas foram renderizadas, submetidas a OCR em português e conferidas visualmente; a cópia pública encontrada é byte a byte idêntica. Também foram examinados o mapa e as folhas de cartas, lidos os objetivos e as tabelas e registrados os esclarecimentos do usuário sobre exércitos iniciais, mínimo de três, ordem de preparação/primeiro reforço, progressão após a 7ª troca, nomes canônicos, autoridade das cartas físicas, dados defensivos, troca de cartas e vitória imediata. Continuam pendentes a transcrição/certificação do grafo, a formalização do movimento e a legibilidade limitada das faces no diagrama da página 5. Não se usa o `war_analyzer` como autoridade normativa.

### 0.3. Criar matriz de rastreabilidade

Cada regra terá:

- `rule_id`;
- edição, página e seção;
- descrição própria;
- pré-condições;
- transição esperada;
- exemplos e casos de fronteira;
- implementação correspondente;
- testes;
- status: confirmado, ambíguo, ausente ou divergente.

Regras de maior risco terão revisão independente.

#### Registro de execução — 2026-10-02

Foi criada a [matriz de rastreabilidade WAR 1 v1.0](war_rules_traceability_v1.0.md), com IDs estáveis para as regras, fonte/edição/página ou asset, enunciado e pré-condições, transição esperada, exemplos/fronteiras/testes propostos, implementação/testes encontrados, estado documental e fila de revisão independente. O catálogo dos 14 objetivos físicos está associado aos IDs `W1-OBJ-01` a `W1-OBJ-14`.

O inventário confirmou que `war_game_engine` e `war_AI` ainda têm apenas documentação descritiva no checkout, e não foi localizada suíte de testes automatizados. A matriz registra separadamente as informações ausentes, ambiguidades e divergências dos protótipos; nenhum comportamento dos protótipos foi promovido a regra normativa.

Uma revisão automatizada separada, somente de leitura, conferiu a matriz contra o manual, mapa, cartas e protótipos: confirmou a coerência do exemplo textual 10 contra 4 (uma vitória do ataque e duas da defesa deixam 8 contra 3), a progressão da Tabela II e os esclarecimentos do usuário; também confirmou que as divergências de cores/objetivos/territórios do analyzer estão assinaladas. A revisão não substitui parecer humano independente sobre a edição física nem execução de testes.

**Adendo normativo do usuário — 2026-10-02:** mínimo/máximo de jogadores 3–6; conjunto de cores físicas; nomes de carta Colômbia e Bolívia como IDs canônicos únicos para as áreas compostas (com aliases do mapa); referência das cartas físicas para catálogo de objetivos e exclusão das implementações analyzer para filtro/fallback; troca opcional com cinco cartas no início da rodada e descarte escolhido ao atingir seis após a carta de fim de rodada; defesa com um dado por exército no território até o máximo de três; vitória verificada imediatamente sempre que o objetivo for satisfeito, com revelação da carta. A matriz foi atualizada. A regra de troca foi marcada como divergência entre o esclarecimento normativo do usuário e a leitura literal do manual, adotando-se o esclarecimento para o perfil-alvo WAR 1.

**Resultado do passo 0.3: matriz documental criada, conferida e complementada com esclarecimentos normativos do usuário.** A matriz distingue regras do perfil-alvo, conflitos de fonte, divergências de protótipos e testes ainda não executados. Permanecem abertos o grafo do mapa, detalhes de movimentação e outros itens listados na matriz; a revisão independente humana das regras de alto risco continua pendente. O passo 0.4 não foi iniciado.

### 0.4. Certificar mapa e componentes

Verificar:

- Quantidade e identidade dos territórios.
- Continentes e bônus.
- Todas as adjacências, inclusive ligações marítimas.
- Composição e multiplicidade das cartas.
- Símbolos e coringas.
- Objetivos e condições alternativas.
- Cores e valores das peças físicas.

IDs não dependerão de nomes traduzidos ou coordenadas de imagem.

#### Registro de execução — 2026-10-02

Criado o [inventário do tabuleiro e componentes WAR 1](war_board_spec_v1.0.md). A inspeção das cartas e do mapa registra 42 territórios (9 na América do Norte, 4 na América do Sul, 7 na Europa, 6 na África, 12 na Ásia e 4 na Oceania), um símbolo por carta (14 triângulos, 14 círculos e 14 quadrados), dois curingas e a associação de cada carta ao continente. Uma verificação de consistência do inventário confirmou 42 IDs únicos, as seis cardinalidades continentais totalizando 42 e a distribuição de símbolos 14/14/14; isso valida a tabela documental, não um motor de jogo. Foram atribuídos IDs de projeto T01–T42 na ordem fixa do inventário de cartas; eles não são códigos impressos. Foram também registrados os nomes canônicos Colômbia e Bolívia, os bônus continentais, as seis cores e as denominações pequena=1/grande=10 documentadas no manual.

**Resultado da checagem da tabela do usuário:** as 42 linhas T01–T42 foram verificadas; há 158 declarações direcionadas correspondentes a 79 pares únicos, sem IDs desconhecidos, auto-adjacências, duplicatas, territórios isolados ou componentes desconexos. A correção final do usuário removeu T21–T37 em ambos os sentidos e confirmou T36–T37, que permanece nos dois sentidos. O JSON foi sincronizado. Não se importou grafo de outra variante. Conforme orientação do usuário, nomes nas cartas são os IDs e aliases compostos são Colômbia/Venezuela → Colômbia e Bolívia/Peru/Chile → Bolívia. Esta verificação atesta a consistência recíproca da lista autorizada pelo usuário, não uma auditoria visual independente de cada fronteira. A quantidade de fichas por conjunto não foi fotografada e permanece como observação suplementar.

**Resultado do passo 0.4: concluído no escopo solicitado pelo usuário.** Quantidade/identidade pelas cartas, continentes, bônus, símbolos, curingas, objetivos e denominações estão inventariados. A lista corrigida — sem T21–T37 e com T36–T37 — passou na verificação de reciprocidade e foi sincronizada no JSON: 42 territórios, 79 pares/158 declarações. Não houve auditoria fotográfica independente de cada fronteira; essa limitação está explícita no inventário e no grafo. No momento da conclusão deste registro, o passo 0.5 ainda não havia começado; sua execução foi iniciada posteriormente e está registrada abaixo.

### 0.5. Certificar preparação

Documentar precisamente:

- Quantidades válidas de participantes.
- Ordem inicial e sorteios.
- Distribuição dos territórios e tratamento de excedentes.
- Distribuição de exércitos.
- Escolhas de colocação inicial.
- Sorteio e filtragem de objetivos.
- Objetivos autorreferentes ou relacionados a cores ausentes.
- Restrições e particularidades da primeira rodada.

#### Registro de execução — 2026-10-02

As páginas 2–3 do manual foram renderizadas e conferidas visualmente para a preparação. A especificação [war_setup_spec_v1.0.md](war_setup_spec_v1.0.md) registra: escolha de cores conforme manual; limite de 3–6 jogadores conforme esclarecimento do usuário; sorteio de objetivos e exclusão de missões para cores ausentes; desempate para escolha do distribuidor; distribuição horária das 42 cartas sem curingas; cálculo dos excedentes para cada mesa válida; um exército por território; reforços adicionais iniciais pela fórmula confirmada pelo usuário; escolha de colocação; devolução/embaralhamento do baralho; e ordem/fases da primeira rodada.

**Verificações documentais:** para 3/4/5/6 jogadores, a distribuição sequencial produz 14/14/14; 11/11/10/10; 9/9/8/8/8; e 7 por jogador, respectivamente. As reservas territoriais iniciais são 7/5/4/3 exércitos adicionais por jogador. O primeiro a jogar é sempre quem segue o último a receber carta. O objetivo é sorteado sem reposição; depois do filtro de cores ausentes, restam $8+P$ cartas elegíveis para $P$ jogadores.

O usuário informou que não poderia responder às perguntas de esclarecimento naquele momento, autorizou decisões autônomas e revisará o trabalho posteriormente. Para fechar o perfil operacional, foram adotadas e justificadas na [especificação da preparação](war_setup_spec_v1.0.md) três interpretações explícitas: embaralhar as 42 cartas territoriais após remover os curingas e antes da distribuição; repetir somente entre os empatados até um resultado único; e aplicar já na primeira rodada os bônus dos continentes completos no início da vez, com colocação obrigatória dentro do continente. O manual não explicita literalmente os dois primeiros procedimentos e não isola o bônus inicial como uma exceção; essas interpretações não são apresentadas como transcrição do manual.

**Resultado do passo 0.5: concluído documentalmente para o perfil operacional, com as três interpretações identificadas e sujeitas à revisão do usuário.** Os cálculos de distribuição e reforços iniciais foram conferidos para 3–6 participantes; a matriz contém os casos de teste futuros e registra que não há engine de preparação nem testes executáveis. Naquele momento, o passo 0.6 ainda não havia começado; sua execução posterior está registrada abaixo.

### 0.6. Certificar o turno completo

Extrair, sem pressupor valores:

- Cálculo e mínimo de reforços.
- Bônus de continentes e eventuais restrições de colocação.
- Trocas de cartas e progressão dos valores.
- Obrigatoriedade de trocas.
- Dados permitidos para atacante **e defensor**.
- Empates, perdas e escolhas defensivas.
- Ocupação após conquista.
- Continuidade dos ataques.
- Deslocamentos, trajetos e reutilização de tropas.
- Compra de cartas.
- Eliminações, autoria e destino das cartas.
- Mudanças de objetivo.
- Instante exato da verificação de vitória.

#### Registro de execução — 2026-10-02

As páginas 3–8 do manual foram renderizadas e conferidas visualmente para extrair o turno completo. A especificação [war_turn_spec_v1.0.md](war_turn_spec_v1.0.md) consolida as fases da segunda rodada em diante; a fórmula de reforço e o mínimo; bônus continentais e seus destinos; conjuntos, progressão global e bônus territorial das trocas; conflito entre a leitura do manual e a regra do usuário para cinco/seis cartas; escolha do atacante e dados defensivos; resolução par a par e empates; perdas e retorno de peças; captura e ataques encadeados; deslocamento final; compra de uma carta; eliminação, efeitos sobre missões e limite de mão; e verificação imediata da vitória.

**Conferências documentais:** as regras do manual e do usuário foram mantidas separadas. Os exemplos textuais de combate (p. 4 e p. 5) e a sequência do turno (p. 8) foram cotejados com a matriz; a progressão da Tabela II e os bônus da Tabela I já conferidos no passo 0.2 foram usados sem substituí-los por dados dos protótipos. O grafo do usuário tem adjacências não tipadas; por convenção explícita, o perfil usa qualquer ligação direta para o movimento final, sujeita a revisão.

**Resultado do passo 0.6: concluído documentalmente para a extração do ciclo normal, não certificado para todos os casos-limite.** Permanecem duas lacunas normativas relevantes: como resolver dois objetivos satisfeitos pela mesma ação e se cartas descartadas por limite de mão entram na reciclagem reservada explicitamente às cartas trocadas. Nenhuma transição foi implementada ou executada em testes. Esses limites, a convenção de arestas para movimento e os casos de teste estão registrados na especificação e na matriz.

### 0.7. Investigar o site — adiado

**Status:** adiado por decisão do usuário até o futuro desenvolvimento do cliente de jogo do `war_analyzer`. Executar esta investigação antes da integração efetiva com o site e antes de certificar o cliente online; não tratar o adiamento como autorização para automação.

Em sessão autorizada:

- Confirmar o alvo indicado no screenshot: `play.wargrow.com.br`.
- Verificar termos, permissões e eventual API oficial.
- Identificar renderização, controles, telas privadas, temporizadores e animações.
- Registrar fluxos de todas as fases.
- Comparar regras observadas com o manual.
- Criar perfil online separado para divergências comprovadas.
- Não usar estado interno que revele informações indisponíveis ao jogador.

### 0.8. Investigar o tabuleiro físico — adiado

**Status:** adiado por decisão do usuário até o futuro desenvolvimento do cliente de jogo do `war_analyzer`. Executar os testes de câmera, peças e fluxo antes de certificar o cliente físico.

Testar antecipadamente:

- Câmera fixa, altura, ângulo e enquadramento.
- Resolução, foco, sombras e reflexos.
- Formatos e valores das peças.
- Pilhas, oclusões e peças próximas a fronteiras.
- Captura de dados e cartas.
- Entrada privada do objetivo da IA.
- Recaptura orientada e confirmação manual.

**Encerramento da Fase 0 por ora — 2026-10-03:** a pedido do usuário, a fase é considerada concluída para o escopo atual de análise e documentação, com os passos 0.1–0.6 registrados. Os itens de integração dos canais online e físico foram explicitamente adiados: 0.7 será retomado antes do cliente online e 0.8 antes do cliente físico, durante o futuro desenvolvimento do cliente de jogo do `war_analyzer`. Não se afirma que esses canais já foram investigados ou aprovados.

**Critérios de liberação posteriores:** resolver as lacunas normativas abertas no passo 0.6 antes de certificar a engine; concluir 0.7 antes de integrar/certificar o canal online; e concluir 0.8 antes de integrar/certificar o canal físico. O encerramento atual da Fase 0 não elimina esses gates técnicos.

---

## Fase 1 — Infraestrutura reproduzível e contratos

### 1.1. Empacotar os submódulos

- Organizar pacotes Python com layout `src`.
- Declarar dependências e extras de testes, treinamento, visão e serviço.
- Fixar versões após verificar compatibilidade real.
- Documentar dependências do sistema, especialmente Tesseract e drivers GPU.
- Manter imports da engine independentes de componentes gráficos e neurais.
- Usar `war_ai` como import Python, preservando o nome do repositório `war_AI`.

### 1.2. Adotar uma pilha inicial

Proposta:

- Engine de referência: Python e NumPy.
- IA: PyTorch.
- Ambiente multiagente: PettingZoo AEC.
- Adaptador focal: Gymnasium.
- Testes: pytest e Hypothesis.
- Qualidade: Ruff, checagem estática e mutation testing.
- Serviço: FastAPI.
- PWA: TypeScript, React e Vite.
- Experimentos: rastreador autocontido e armazenamento de artefatos por hash.

As versões e licenças serão verificadas antes de serem travadas.

### 1.3. Formalizar os contratos

- Definir os tipos da seção 3.
- Separar estado lógico de geometria visual.
- Gerar schemas de transporte e tipos TypeScript.
- Implementar validação e testes de serialização.
- Documentar exemplos públicos, privados e incompletos.
- Recusar incompatibilidades de versão explicitamente.

### 1.4. Versionar todas as semânticas relevantes

Versionar separadamente:

- Regras.
- API.
- Observações.
- Ações.
- Replays.
- Datasets.
- Modelos.
- Configuração de inferência.

Alterar regras ou codificação deverá invalidar certificados relacionados.

### 1.5. Criar CI por módulo e na raiz

- Checkout dos submódulos em commits fixos.
- Build, import headless, lint, tipos e testes.
- Testes de contrato entre módulos.
- Verificação de segredos e dependências.
- Smoke tests CPU em alterações comuns.
- Campanhas GPU e testes extensos em jobs específicos.
- Publicar commits dos submódulos antes de atualizar os gitlinks do agregador.

### 1.6. Definir reprodutibilidade

Cada execução registrará:

- Commits.
- Dependências.
- Hardware e drivers.
- Configuração completa.
- Sementes.
- Hashes de dados e pesos.
- Normalizadores, otimizador e estado do treinamento.
- Configuração da banca e orçamento de inferência.

**Critério de saída:** instalação limpa, contratos testados, CI básico aprovado e integração simulada sem dependências circulares.

---

## Fase 2 — Núcleo, tabuleiro e preparação

### 2.1. Implementar dados canônicos

- Criar `BoardSpec` e validadores.
- Verificar unicidade de IDs, referências, adjacências e composição dos continentes.
- Validar baralhos e objetivos.
- Detectar duplicidades como as existentes no protótipo.
- Preservar referência da fonte de cada dado.

### 2.2. Implementar estados

- Estado completo, público e observação individual.
- Fase, turno e jogador responsável pela próxima decisão.
- Pools de reforços com origem.
- Mãos, baralho e descarte.
- Participantes ativos/eliminados.
- Controle necessário para movimentação.
- Contadores inteiros sem saturação arbitrária.

Limites físicos de peças só serão regras se a fonte assim determinar.

### 2.3. Implementar transições e legalidade

- Preferir funções puras ou mutação estritamente encapsulada.
- Expor `validate_action()` e interface de ações legais.
- Rejeitar ações inválidas sem modificar estado ou RNG.
- Distinguir jogador do turno de jogador que precisa decidir uma defesa.
- Centralizar regras para que clientes e RL não as reimplementem.

### 2.4. Implementar aleatoriedade isolada

Criar streams separados para:

- Preparação.
- Objetivos e sorteios.
- Cartas.
- Combate.
- Cada política.

A semente permitirá reprodução pelo avaliador, mas não será observação da IA.

### 2.5. Implementar preparação completa

- Executar todos os sorteios conforme o manual.
- Expor decisões iniciais aos agentes.
- Tratar todas as quantidades de jogadores.
- Cobrir filtragem e substituição de objetivos.
- Criar fixtures para casos comuns e excepcionais.

### 2.6. Implementar snapshots e replay

- Serialização canônica e hashes.
- Restauração do estado e RNG.
- Reexecução por ações e resultados de chance.
- Replays públicos sanitizados separados dos completos.
- Detecção de incompatibilidade de schema.

**Critério de saída:** preparação reproduzível, observações sem vazamentos e restauração sem perda.

---

## Fase 3 — Regras completas e término

### 3.1. Implementar máquina de fases

Cobrir preparação, recebimento/troca, colocação, combate, ocupação, movimentação, compra/fim de turno e término, conforme a especificação certificada.

As transições terão guardas explícitas e testes.

### 3.2. Implementar reforços e cartas

- Calcular todos os pools.
- Preservar restrições de destino.
- Validar combinações de símbolos e coringas.
- Aplicar progressão das trocas.
- Tratar trocas obrigatórias.
- Tratar descarte, reembaralhamento e recebimento após eliminação.
- Testar impactos sobre o turno em andamento.

### 3.3. Implementar combate rodada a rodada

- Fixar escolhas antes de solicitar chance.
- Resolver ordenação, comparações e empates conforme o manual.
- Enumerar todos os resultados possíveis das combinações legais de dados.
- Produzir distribuições exatas de perdas.
- Comparar com um resolvedor independente.
- Testar limites de tropas e dados.

### 3.4. Implementar conquista e ocupação

- Aplicar perdas e mudança de dono.
- Exigir transferência legal.
- Preservar guarnições obrigatórias.
- Atualizar autoria de eliminação e efeitos sobre cartas.
- Verificar vitória nos instantes corretos.
- Não permitir que uma ação agregada ignore decisões intermediárias.

### 3.5. Implementar movimentação

- Validar origem, destino, quantidade e conectividade.
- Rastrear tropas já movimentadas quando necessário.
- Respeitar limites por fase e por território.
- Não pressupor regras de fortificação de outras variantes.

### 3.6. Implementar objetivos

Criar avaliadores tipados para todos os objetivos certificados:

- Territórios.
- Guarnições.
- Continentes.
- Continente adicional.
- Eliminações.
- Condições alternativas.

Testar autorreferência, alvo ausente, eliminação por terceiro e momento de conclusão.

### 3.7. Separar chance simulada e externa

- Simulação amostra `ChanceOutcome`.
- Site e tabuleiro físico fornecem resultados observados.
- Outcomes têm IDs e não podem ser aplicados duas vezes.
- Faces incompatíveis são rejeitadas.
- Resultado agregado observado não será registrado como faces que ninguém viu.
- O cliente jamais substituirá o dado real por um sorteio local.

### 3.8. Tratar término e truncamento

Distinguir:

- Vitória oficial.
- Eliminação individual.
- Desistência.
- Interrupção operacional.
- Truncamento técnico de treinamento.

**Não declarar vencedor por quantidade de territórios ao atingir um limite artificial.**

**Critério de saída:** partidas completas para todas as configurações certificadas, com replays e efeitos normativos corretos.

---

## Fase 4 — Certificação da engine e modo humano

### 4.1. Completar testes por regra

- Pelo menos um conjunto de exemplos e fronteiras por `rule_id`.
- Revisão independente.
- Casos específicos para regras da primeira rodada, trocas, eliminações e vitória.
- Outra implementação de Risk só será oráculo se sua equivalência for demonstrada.

### 4.2. Criar testes de propriedades

Verificar continuamente:

- Ausência de tropas negativas.
- Ocupação consistente.
- Contabilidade de tropas e cartas.
- Legalidade das fases.
- Exclusão correta de jogadores eliminados.
- Integridade de alterações territoriais.
- Vitória somente nas condições permitidas.

### 4.3. Criar testes metamórficos e de sigilo

- Permutar IDs/cores junto com seus objetivos preserva semântica.
- Reindexar o grafo não muda o jogo.
- Snapshot/replay não muda resultado.
- Mudar informação oculta, mantendo a mesma observação legítima, não altera observações ou máscaras.
- Não exigir simetria de territórios que possuem posições estratégicas diferentes.

### 4.4. Testar a qualidade dos testes

Mutation testing deverá detectar, por exemplo:

- Inversão do desempate.
- Alteração de bônus.
- Compra indevida de carta.
- Movimento ilegal.
- Vitória verificada no instante errado.

### 4.5. Executar stress

Metas iniciais:

- Pelo menos **1 milhão de partidas** de stress.
- Pelo menos **10 milhões de transições** verificadas.
- Zero violações de invariantes.
- Zero divergências de replay.
- Cobertura de ramificações do núcleo ≥95%.
- Mutation score ≥90% dos mutantes válidos avaliados.

Truncamentos e crashes serão registrados, não apresentados como partidas concluídas.

### 4.6. Implementar um humano contra IAs

Runner/CLI deverá aceitar:

- Quantidade de jogadores.
- Um assento humano.
- Um modelo repetido nos demais assentos.
- Modelos diferentes por assento.
- Sementes independentes.
- Save/resume.
- Estado textual e ações legais.
- Objetivo/cartas humanos privados.
- Decisões defensivas fora do turno, se previstas.

A engine conhecerá `AgentProtocol`, não implementações concretas da IA.

### 4.7. Otimizar sem alterar regras

Medir:

- Transições e partidas por segundo.
- Custo de clonagem.
- Memória.
- Latência de validação.
- Gargalos de geração de ações.

Backends acelerados exigirão comparação diferencial com a referência Python.

**Critério de saída:** engine certificada, modo humano funcional e desempenho mensurado.

---

## Fase 5 — Ambiente RL, ações, baselines e arena

### 5.1. Implementar PettingZoo AEC

- `agent_selection`, `observe()`, `step()`, recompensas e términos.
- Agentes mortos e decisões fora do turno.
- Máscaras de ações.
- Testes oficiais de API e seeding.
- Paralelismo entre partidas, não ações simultâneas fictícias dentro de uma mesa.

### 5.2. Implementar adaptador Gymnasium focal

- Um jogador recebe decisões.
- Os adversários avançam até a próxima decisão dele.
- Registrar duração semântica entre decisões.
- Tratar corretamente `terminated` e `truncated`.
- Não confundir eliminação com simples ausência temporária de ação.

### 5.3. Projetar observações

Usar:

- Grafo do tabuleiro.
- Ocupação e tropas.
- Continentes.
- Recursos de reforço.
- Fase e participantes.
- Objetivo e mão próprios.
- Histórico público.
- Máscaras para mesas de tamanho variável.

Normalização não poderá descartar quantidades legais.

### 5.4. Projetar espaço de ações completo

Preferir decodificação estruturada:

**tipo → origem → destino → parâmetros → quantidade → confirmação**

- Máscaras condicionais.
- Quantidade limitada pelo estado, não por um máximo arbitrário.
- Prefixos de ação não alteram a engine.
- Uma ação semântica só é aplicada após estar completa.
- Para intervalos variáveis, usar categorias dinâmicas ou codificação de inteiros por tokens com validação de prefixo.
- Testar cobertura e round-trip das ações legais.

Evitar um `Discrete(10000)` arbitrário que exclua estratégias válidas.

### 5.5. Implementar losses compatíveis

- Probabilidade conjunta da ação composta.
- Entropia e KL consistentes com máscaras.
- Memória recorrente por jogador.
- Máscaras válidas no rollout e no aprendizado.
- Testes de gradientes e de ações nas fronteiras.

Não presumir que recorrência, masking e ações estruturadas funcionem apenas combinando wrappers prontos.

### 5.6. Definir recompensa

- Métrica canônica: vitória oficial.
- Recompensa de avaliação: `1` para vitória, `0` para não vitória.
- Priorizar formulação episódica com $\gamma=1$.
- Desconto menor será experimento explícito, pois pode favorecer vitória rápida em vez de máxima chance de vencer.
- Shaping será opcional, baseado em potencial de informação permitida e objetivo próprio.
- Proposta inicial: $|\Phi|\leq0{,}05$, com potencial terminal zero.
- Comparar sempre com ausência de shaping.

Não premiar ataques ou territórios indefinidamente como substituto da vitória.

### 5.7. Construir baselines

- Aleatório legal.
- Expansionista.
- Conservador de fronteiras.
- Orientado ao objetivo.
- Controle de continentes.
- Eliminação oportunista.
- Planejamento com probabilidades exatas locais.

O aleatório servirá para sanidade e currículo, **não para facilitar a homologação final**.

### 5.8. Construir arena

- Modelos congelados por assento.
- Seeds e budgets registrados.
- Resultado oficial.
- Replays completos.
- Classificação de falhas.
- Estatística por adversário, missão e mesa.
- Testes com resultados conhecidos.

**Critério de saída:** ambiente RL confiável, ações completas, baselines e avaliação auditável.

---

## Fase 6 — Primeiro agente RL

### 6.1. Implementar PPO de referência

- PPO feedforward mascarado.
- Versão recorrente GRU/LSTM.
- Crítico local inicial.
- Testes de clipping, razões de importância, entropia e normalização.
- Testes de reset da memória e retorno após término.

### 6.2. Demonstrar aprendizado em tarefas pequenas

Treinar e avaliar:

- Colocação legal.
- Atacar ou parar.
- Ocupação.
- Movimentação.
- Trocas.
- Conclusão de objetivos simples.

Em subproblemas enumeráveis, comparar com solução exata.

### 6.3. Introduzir currículo

- Cenários táticos.
- Estados intermediários válidos.
- Adversários progressivamente melhores.
- Aumento da complexidade até as regras completas.
- Manutenção de amostras de partidas completas.

Cenários simplificados nunca entrarão na homologação do WAR completo.

### 6.4. Iniciar self-play histórico

- Treinar contra snapshots e estilos variados.
- Variar assento, cor, missão e quantidade de jogadores.
- Não usar apenas a versão atual.
- Não compartilhar segredos entre instâncias.

### 6.5. Registrar e reproduzir treinamento

- Vitórias reais e recompensa shaped separadas.
- Curvas por objetivo e mesa.
- KL, entropia, gradientes e losses.
- Comprimento e truncamentos.
- Throughput e recursos.
- Checkpoints com estado completo de retomada.

### 6.6. Repetir por sementes

- Pelo menos 10 seeds para configurações promovidas.
- Avanço condicionado a aprendizado reproduzível e ganho estatístico.
- Nenhum modelo será considerado final por atingir determinado número de timesteps.

**Critério de saída:** primeiro agente treinável e exportável, capaz de completar partidas legais.

---

## Fase 7 — Comparação de arquiteturas e algoritmos

### 7.1. Separar os eixos experimentais

Comparar independentemente:

- Algoritmo.
- Encoder.
- Memória.
- Representação da ação.
- Currículo.
- Shaping.
- Liga.
- Busca.

Isso evita atribuir a um Transformer um ganho causado apenas por mais computação.

### 7.2. Avaliar arquiteturas

- MLP.
- Rede de grafo com message passing.
- Graph Transformer.
- GRU/LSTM.
- Transformer causal de eventos.
- Heads condicionados por fase.
- Representação do objetivo e das cartas.
- Heads de política, valor e crença.

### 7.3. Avaliar algoritmos

Ramos mínimos:

1. PPO feedforward.
2. PPO recorrente.
3. Actor-critic com encoder de grafo.
4. IMPALA/V-trace.
5. Off-policy recorrente, como abordagem inspirada em R2D2, adaptada a ações estruturadas.
6. Política/valor combinados com busca.

SAC contínuo, DDPG e métodos cooperativos como QMIX não serão escolhas padrão para este problema.

### 7.4. Avaliar treinamento centralizado

- Crítico local versus crítico privilegiado.
- Labels de segredos usados somente em losses de treinamento apropriados.
- Ator estritamente limitado à observação do jogador.
- Testes contrafactuais de não interferência.
- Separação entre arquitetura de treinamento e artefato de produção.

### 7.5. Fazer busca de hiperparâmetros

Faixas iniciais propostas:

| Parâmetro | Exploração inicial |
|---|---|
| Learning rate | $10^{-5}$ a $3\times10^{-4}$, escala log |
| PPO clip | 0,1 / 0,2 / 0,3 |
| GAE $\lambda$ | 0,90 / 0,95 / 0,98 / 1 |
| Desconto semântico | 0,99 / 0,995 / 0,999 / 1 |
| Entropia inicial | 0 / 0,01 / 0,03 / 0,05 |
| Camadas de grafo | 3 / 6 / 12 |
| Dimensão oculta | 128 / 256 / 512 / 1024 |
| Histórico | 64 / 256 / 1024 eventos |

Esses valores iniciam a pesquisa; não limitam a solução final.

### 7.6. Varrer configurações de treinamento

- Batch e rollout.
- Número de workers.
- Burn-in e truncamento de backpropagation.
- Relação replay/updates.
- Lag de políticas.
- Normalização.
- Amostragem de adversários.
- Proporção de currículo.
- Distribuição de mesas e objetivos.

Dados de versões incompatíveis não serão misturados silenciosamente.

### 7.7. Comparar com rigor

- Orçamento controlado na comparação inicial.
- Curvas por amostras, compute e tempo.
- Avaliações pareadas em desenvolvimento.
- Pelo menos 20 seeds para finalistas.
- Ablações e registros de resultados negativos.
- Estudos adicionais de scaling sem teto arbitrário.

**Critério de saída:** catálogo de abordagens comparáveis e seleção fundamentada dos ramos fortes.

---

## Fase 8 — Liga e resistência à exploração

### 8.1. Construir população

Manter:

- Agentes principais.
- Snapshots históricos.
- Líderes por arquitetura/seed.
- Especialistas por missão/estilo.
- Agentes de exploração de fraquezas.
- Modelos independentes de generalização.

### 8.2. Treinar contra mesas completas

- Amostrar lineups de vários jogadores.
- Combinar histórico uniforme e prioridade para confrontos difíceis.
- Registrar probabilidades de amostragem.
- Preservar diversidade.
- Não reduzir WAR a uma coleção de duelos.

### 8.3. Explorar PSRO e metajogo empírico

- Treinar respostas a misturas de políticas.
- Registrar payoffs por lineup.
- Estudar metaestratégias, regret e métodos de ranking adequados.
- Detectar ciclos: A vence B, B vence C, C vence A.

Elo pairwise sozinho não representará toda a força multiplayer.

### 8.4. Treinar melhores respostas

- Pelo menos três abordagens independentes.
- Várias sementes.
- Cada explorador maximiza sua própria vitória.
- Nenhum compartilhamento de segredos ou política de equipe escondida.
- Colusões deliberadas poderão ser stress tests separados, não a banca normal.

### 8.5. Medir generalização

- Cross-play entre sementes e arquiteturas.
- Desempenho contra modelos não usados no treinamento.
- Pior adversário e pior lineup.
- Regressão contra históricos.
- Fraquezas por missão.
- Adaptação indevida a cores ou assentos.

### 8.6. Formar banca congelada

Proposta rigorosa:

- Pelo menos oito políticas distintas.
- Pelo menos três abordagens bem-sucedidas.
- Líderes relevantes e adversários independentes.
- Inclusão dos adversários fortes encontrados.
- Não preencher o banco com agentes aleatórios ou versões intencionalmente fracas.
- Não contar muitos checkpoints quase idênticos como diversidade suficiente.

**Critério de saída:** população reproduzível, banca forte e avaliação empírica de vulnerabilidades.

---

## Fase 9 — Busca, informação imperfeita e candidato final

### 9.1. Implementar crenças

Estimar objetivos/cartas adversários a partir de:

- Prior correspondente às regras de distribuição.
- Histórico público.
- Ações observadas.
- Informações próprias.

Comparar prior simples, partículas e modelos aprendidos. Avaliar calibração.

### 9.2. Implementar busca apropriada

Investigar ISMCTS/POMCP adaptados:

- Nós de chance.
- Amostragem de estados compatíveis.
- Histórico/conjunto informacional.
- Rollouts por jogador.
- Política e valor neurais.

Não consultar o `FullGameState` verdadeiro para planejar.

### 9.3. Evitar erros de informação

- Evitar *strategy fusion*: escolher ações como se diferentes segredos já fossem conhecidos.
- Cada oponente simulado recebe apenas sua própria observação.
- A política focal não sabe qual hipótese de segredo foi sorteada.
- Determinização ingênua permanece baseline limitado, não solução automaticamente correta.

### 9.4. Integrar probabilidades exatas

- Usar distribuições certificadas de combate.
- Avaliar campanhas por programação dinâmica quando semanticamente equivalente.
- Não substituir várias rodadas por uma macro que ignore parada, ocupação ou vitória intermediária.
- Comparar busca agregada com execução rodada a rodada.

### 9.5. Comparar soluções de inferência

- Política sem busca.
- Política com busca.
- Crença simples/aprendida.
- Orçamento crescente.
- Ensemble ou portfólio.
- Distilação.

Um portfólio não poderá escolher políticas conhecendo a identidade interna do adversário.

### 9.6. Definir perfis de execução

- Perfil rápido.
- Perfil forte.
- Perfil de pesquisa, se necessário.

O orçamento considerará o turno inteiro, não quantidade de tokens produzidos. Cada perfil publicado será avaliado separadamente.

### 9.7. Selecionar por evidência

Após legalidade e sigilo:

1. Probabilidade de vitória.
2. Pior adversário/grupo.
3. Resistência aos exploradores.
4. Desempenho no canal real.
5. Custo operacional.

Como evidência de plateau local, exigir pelo menos três ciclos independentes de pesquisa sem ganho confirmado de 2 pontos percentuais em validação. Isso **não prova ótimo global**.

### 9.8. Congelar e exportar

- Pesos e hash.
- Encoder/decoder.
- Estado recorrente.
- Configuração de amostragem.
- Busca e budgets.
- Compatibilidade com regras.
- Testes de paridade.
- Model card.

**Critério de saída:** candidato reproduzível e congelado antes de revelar os testes finais.

---

## Fase 10 — Analyzer comum e rastreamento

### 10.1. Caracterizar os protótipos

- Criar testes com as imagens existentes.
- Identificar diferenças entre variantes.
- Retirar efeitos de importação.
- Corrigir caminhos de assets.
- Preservar baseline antes de consolidar.

### 10.2. Separar percepção de domínio

- Migrar dados normativos para a engine.
- Externalizar resolução, geometria e paleta.
- Usar IDs canônicos.
- Representar desconhecido explicitamente.
- Não tratar falha de OCR como zero.

### 10.3. Criar interfaces

- `CaptureSource`.
- `PerceptionBackend`.
- `StateTracker`.
- `ActionExecutor`.

Screenshot digital e peças físicas terão implementações distintas.

### 10.4. Controlar o fluxo de imagens

- Timestamp e `frame_id`.
- Detecção de estabilidade.
- Filas com backpressure.
- Descarte de frames antigos.
- Invalidação após movimento da câmera.
- Qualidade e confiança calibradas.

Correlação de template matching não é probabilidade calibrada.

### 10.5. Fundir evidências

- Combinar observações temporais e eventos confirmados.
- Conferir transições possíveis.
- Preservar hipóteses quando mais de uma trajetória for possível.
- Solicitar informação quando a regra depender de eventos não observados.
- Não atribuir automaticamente discrepâncias ao jogador.

### 10.6. Implementar o ciclo de execução

**Observar → validar → decidir → emitir intenção → executar → receber ACK → verificar → consolidar**

- Uma ação mutante pendente.
- `command_id` persistente.
- `state_version`.
- Precondições.
- Recuperação após desconexão.
- Correções auditáveis.

**Critério de saída:** percepção e execução desacopladas, incerteza explícita e comandos não duplicados.

---

## Fase 11 — Cliente online

### 11.1. Implementar adaptador autorizado

Preferência:

1. API oficial autorizada.
2. Automação de controles visíveis.
3. Visão sobre canvas/screenshot quando necessária.

Não presumir que os territórios estejam acessíveis pelo DOM.

### 11.2. Reconhecer todas as informações necessárias

- Mapa e tropas.
- Fase.
- Jogador ativo.
- Recursos de colocação.
- Objetivo e mão próprios.
- Dados/resultados.
- Trocas.
- Eliminações.
- Vitória.
- Temporizador e modais.

### 11.3. Automatizar a partida inteira

- Entrada/configuração de mesa.
- Preparação.
- Colocação.
- Trocas.
- Ataque/parada.
- Defesa, se exigida.
- Ocupação.
- Movimentação.
- Fim de turno.
- Finalização.

Login, 2FA e CAPTCHA continuarão humanos.

### 11.4. Verificar cada interação

- Confirmar precondições.
- Executar.
- Esperar estabilização.
- Ler pós-condições.
- Reconciliar antes de repetir após timeout.

**Clique não é operação idempotente.**

### 11.5. Tratar mudanças e falhas

- Mudança de layout.
- Zoom/DPI.
- Idioma.
- Modal inesperado.
- Perda de foco.
- Rede.
- Turno alheio.
- Estado incompleto.

Adicionar pausa e interrupção imediata.

### 11.6. Testar

- Mock do site e fixtures para CI.
- Testes por versão.
- Partidas privadas autorizadas.
- Detecção de drift.
- Recertificação após mudança incompatível.

**Critério de saída:** jogar integralmente, não apenas interpretar screenshots.

---

## Fase 12 — Visão do tabuleiro físico

### 12.1. Construir dataset real

Capturar e anotar:

- Tabuleiros da edição alvo.
- Donos e quantidades.
- Valores/formas das peças.
- Dados.
- Diferentes aparelhos, focos e iluminação.
- Sombras e reflexos.
- Pilhas, fronteiras e oclusões.
- Mãos em movimento.

Ground truth será contagem independente, não previsão da engine.

### 12.2. Separar os dados corretamente

- Splits por sessão, tabuleiro e aparelho.
- Não distribuir frames vizinhos entre treino e teste.
- Reservar condições não vistas.
- Usar dados sintéticos apenas como complemento.

### 12.3. Calibrar geometria

- Cantos, landmarks ou marcadores opcionais.
- Homografia robusta.
- Correção de distorção quando necessária.
- Orientação.
- Detecção de deslocamento da câmera.
- Tratamento de peças 3D próximas a fronteiras.

### 12.4. Comparar percepção

- Segmentação HSV/Lab.
- Detecção/segmentação de instâncias.
- Contagem de agrupamentos.
- Reconhecimento de denominações.
- Combinações dos métodos.

Contar peças não basta quando existem peças de valores diferentes.

### 12.5. Tratar oclusões honestamente

Quando não for possível observar:

- Pedir retirada da mão.
- Melhorar iluminação.
- Reorganizar pilha.
- Solicitar close-up orientado.
- Permitir entrada manual.

Não inferir certeza de uma peça completamente escondida.

### 12.6. Integrar dados e informações privadas

- Área auxiliar opcional para dados.
- Confirmação de faces.
- Entrada estruturada quando a câmera não captar.
- Captura privada do objetivo e cartas da IA.
- Auxiliar/árbitro de confiança para entrada manual de segredo.
- Não anunciar objetivo pela voz.

### 12.7. Acompanhar os adversários

- Observar mudanças fora do turno da IA.
- Solicitar confirmação de eventos que não possam ser reconstruídos.
- Reconhecer fase concluída, combate resolvido e movimentação.
- Não criar histórico fictício a partir de um snapshot.

### 12.8. Medir confiança e autonomia

- Precisão por território.
- Tabuleiro completamente correto.
- Precisão entre estados aceitos automaticamente.
- Cobertura automática.
- Correções.
- Recapturas.
- Erros silenciosos.
- Condições fora do domínio.

**Critério de saída:** percepção real útil, calibrada e capaz de se abster.

---

## Fase 13 — PWA, voz e ACK

### 13.1. Implementar serviço de sessão

- FastAPI.
- Autenticação.
- Papéis de controlador/observador.
- WebSocket autenticado.
- Heartbeat.
- Limites de requisição.
- Workers separados de inferência.
- Persistência transacional de eventos e comandos.

### 13.2. Implementar captura mobile

- `getUserMedia()`.
- Câmera traseira preferida.
- Preview, calibração e overlays.
- Snapshots/bursts estáveis.
- HTTPS válido inclusive na rede local.
- Upload/entrada manual quando a câmera não estiver disponível.

O `localhost` do computador não é o `localhost` do celular.

### 13.3. Tratar desconexão e suspensão

- Cache apenas do necessário.
- Não reenviar automaticamente comandos mutantes offline.
- Pausar novas ordens ao perder conexão.
- Reconciliar estado ao retomar.
- Usar Wake Lock quando suportado.
- Lidar com suspensão de aba/aplicação.

### 13.4. Implementar voz

- Templates determinísticos em pt-BR.
- Ação, origem, destino e quantidade explícitos.
- `SpeechSynthesis`.
- Teste de disponibilidade de voz.
- Ativação por gesto quando exigida.
- Texto sempre disponível.
- TTS local no servidor como alternativa.

Microfone não é necessário para falar comandos.

### 13.5. Implementar máquina de confirmação

Estados:

`proposed` → `awaiting_execution` → `ack_received` → `verifying` → `committed`

Exceções:

`rejected`, `timed_out`, `paused`, `cancelled`, `needs_reconciliation`.

- Timeout não vira ACK.
- ACK não prova que as peças foram movidas corretamente.
- Cancelamento após possível execução exige reconciliação.
- Repetir áudio não repete a ação.

### 13.6. Oferecer controles mínimos

- Confirmar execução.
- Informar não execução.
- Informar dados.
- Corrigir quantidade/dono.
- Recapturar.
- Repetir fala.
- Pausar.
- Retomar.
- Finalizar fase quando permitido.

### 13.7. Verificar após execução

- Conferir regiões afetadas.
- Aplicar invariantes.
- Mostrar diferenças entre ACK e câmera.
- Invalidar planos dependentes de estado incorreto.
- Não ordenar sequência de conquistas assumindo resultados futuros dos dados.

### 13.8. Homologar aparelhos

- Android/Chrome.
- iOS/Safari.
- Câmera e áudio indisponíveis.
- Modo silencioso.
- Rotação.
- Suspensão.
- Mudança de rede.
- Reinício do servidor.
- ACK duplicado.
- Acessibilidade além de cor e voz.

**Critério de saída:** acompanhar uma partida física do início ao vencedor, com recuperação de falhas.

---

## Fase 14 — Homologação e release

### 14.1. Congelar a versão

Congelar regras, código, modelos, busca, encoder, banca, seeds seladas, budgets e perfis suportados.

Alteração posterior inicia nova tentativa formal.

### 14.2. Executar avaliação científica

Aplicar o protocolo abaixo, sem omitir:

- Adversários difíceis.
- Sementes desfavoráveis.
- Missões difíceis.
- Crashes.
- Timeouts.
- Partidas demoradas.

### 14.3. Validar o artefato implantado

- Paridade com a política avaliada.
- Engine e CLI.
- Mocks.
- Vídeos gravados.
- Site autorizado.
- Câmera real.

Distinguir falha estratégica, erro de percepção e erro de execução.

### 14.4. Executar campanhas reais

- Pelo menos 100 partidas online autorizadas.
- Pelo menos 100 partidas físicas.
- Diferentes tamanhos de mesa.
- Pelo menos 10 setups físicos.
- Ambos os sistemas mobile.
- Jogadores distintos.

Vitória contra humanos será exploratória, salvo criação de protocolo específico.

### 14.5. Injetar falhas

Pelo menos 100 mil cenários envolvendo:

- Mensagens duplicadas ou fora de ordem.
- ACK repetido.
- Desconexão.
- Reinício.
- Estado desatualizado.
- Perda de câmera/voz.
- Reset de inferência.

Exigir ausência de aplicações duplicadas, ações ilegais e vazamentos.

### 14.6. Publicar evidências

- Relatório de regras.
- Resultados com denominadores e intervalos.
- Banca e lineups.
- Seeds após conclusão.
- Replays.
- Hardware e latências.
- Model card e data card.
- Instalação, calibração e recuperação.
- Limitações conhecidas.

### 14.7. Publicar e manter

- Tags por submódulo e agregador.
- Gitlinks consistentes.
- Manifests travados.
- Canário/shadow.
- Rollback.
- Desativação de adaptador incompatível.
- Recertificação após mudanças semânticas.
- Nenhum aprendizado online silencioso após homologação.

**Critério de saída:** todos os critérios obrigatórios aprovados. Caso contrário, permanece candidato.

---

# 6. Protocolo da meta de 80/100

## 6.1. O que significa vitória

Vitória será **ganhar a partida completa pelo objetivo oficial**.

Não serão vitórias:

- Ganhar um combate.
- Eliminar um jogador sem cumprir o objetivo.
- Ter mais territórios ao atingir um limite artificial.
- Sobreviver mais tempo.
- Obter maior recompensa shaped.

## 6.2. Por que não exigir 80% contra clones idênticos

Com $N$ cópias idênticas, posições aleatorizadas e condições simétricas, a vitória esperada de cada participante é aproximadamente:

$$
P(\text{vitória})=\frac{1}{N}
$$

Clones idênticos servirão para **testar equilíbrio, isolamento e ausência de viés**, não para a meta de 80%.

Não existe garantia de 80% contra qualquer IA futura ou adversário igualmente forte.

## 6.3. Banca e cenários

Para cada quantidade de jogadores e perfil certificado:

- Uma instância candidata.
- Pelo menos oito modelos adversários distintos e congelados.
- Sem agentes aleatórios preenchendo a mesa.
- Sem colusão ou compartilhamento de informações.

Dois tipos de cenário:

1. **Homogêneo:** candidata contra $N-1$ instâncias de cada adversário da banca.
2. **Misto:** candidata contra $N-1$ modelos amostrados da banca, sem reposição.

**Cada cenário homogêneo e o cenário misto precisarão atingir pelo menos 80 vitórias em 100 partidas registradas.**

Isso é mais rigoroso do que aprovar apenas uma média que esconda derrotas contra um adversário específico.

## 6.4. Equidade

- Assentos equilibrados na série de 100, com diferença máxima de uma partida.
- Objetivos e preparação conforme a distribuição oficial.
- Informações equivalentes.
- Orçamento de inferência equivalente.
- Hardware/protocolo registrados.
- Memória e RNG resetados por partida.
- Adversários congelados, mas não necessariamente determinísticos.

## 6.5. Validação estatística adicional

Observar 80/100 não demonstra uma taxa verdadeira de pelo menos 80%. Como referência, o intervalo bilateral de Wilson de 95% fica aproximadamente entre **71% e 87%**.

Portanto, acrescentar:

- Amostra **independente** de pelo menos **10.000 partidas por célula**.
- Tamanho definitivo escolhido por análise de potência antes de revelar sementes.
- Potência proposta ≥90% para distinguir $p=0{,}80$ de $p=0{,}82$.
- Limite inferior unilateral exato de Clopper–Pearson **≥0,80 em todas as células**.
- Correção para múltiplas comparações e tentativas.

Com oito adversários, quatro tamanhos de mesa e $P$ pares distintos de regras/configuração de inferência:

$$
m=36P
$$

Para controlar sucessivas tentativas, uma política possível é:

$$
\alpha_j=\frac{0{,}05}{j(j+1)}
$$

Dentro da tentativa, dividir pelo número total de hipóteses confirmatórias registradas. Novas sementes não apagam o efeito de testar candidatos repetidamente.

### Tratamento de falhas

- Crash, timeout e ilegalidade do candidato contam como não vitória.
- Truncamento não é vitória e não desaparece do denominador.
- Falha global de infraestrutura segue regra anterior ao resultado.
- Proibidos: escolher melhores blocos, repetir seed até ganhar ou parar quando o percentual desejado aparecer.
- Jogos pareados/rotações de um cenário exigem análise agrupada; não são tratados ingenuamente como observações independentes.

---

# 7. Métricas adicionais e valores objetivos

| Área | Meta proposta para v1.0 |
|---|---|
| Rastreabilidade | 100% das regras certificadas e ligadas a testes |
| Engine | Zero violação em ≥1 milhão de partidas de stress |
| Cobertura | ≥95% das ramificações do núcleo |
| Mutation testing | ≥90% dos mutantes válidos avaliados |
| Legalidade | Zero ação inválida emitida em 10 milhões de decisões de stress |
| Sigilo | Zero vazamento nos testes de observação, busca, memória, API, logs e replay |
| Força | ≥80/100 por cenário e LCB corrigido ≥80% na campanha independente |
| Robustez por estrato | Limite inferior da diferença contra referência ≥−3 pontos percentuais |
| Resistência empírica | Limite superior da vitória de exploradores testados ≤$1/N+0{,}05$ |
| Screenshot | Dono ≥99,9%; tropas exatas ≥99,5% por território visível |
| Físico | Dono ≥99,5%; tropas exatas ≥98% por território visível |
| Tabuleiro autoaceito | Estado completo correto ≥99,9% |
| Cobertura automática | ≥95% no digital; ≥90% em cenas físicas estáveis do domínio suportado |
| Execução | Zero aplicação duplicada/ilegal em ≥100 mil cenários de falha |
| Recuperação | ≥99% das falhas de conectividade retomam com estado confirmado; restante em pausa segura |
| Operação real | ≥100 partidas por canal e ≥99% das intenções executadas/verificadas sem correção |
| Percepção | p95 ≤2 s por snapshot estável |
| Política sem busca | p95 ≤250 ms no hardware declarado |
| Busca física | p95 ≤10 s por decisão no perfil declarado |
| Voz | Início p95 ≤1 s após decisão pronta, excluído tempo humano |
| Online | Respeitar o prazo real do turno, com margem de transporte/interface |

### Ressalvas necessárias

- Precisão por território não equivale a tabuleiro inteiro correto.
- Alta precisão obtida rejeitando praticamente tudo não satisfaz a cobertura.
- Precisão após correção manual não vale como precisão automática.
- Entrada normal de dados/cartas e ACK será medida separadamente de correção de erros.
- A visão terá pelo menos 10.000 snapshots por canal, provenientes de pelo menos 200 sessões/configurações, com análise agrupada.
- Zero erros observados não prova erro populacional zero.
- Para visão autoaceita, exigir também limite inferior conservador de precisão ≥99,5%; ampliar sessões conforme o protocolo.
- Não usar bootstrap degenerado com zero erros para anunciar certeza.
- As latências dependem de hardware, rede e perfil explicitamente documentados.

### Avaliação de robustez

- Pelo menos 1.000 jogos adicionais por estrato marginal de missão e assento.
- Comparação com a melhor referência previamente escolhida.
- Exploração por pelo menos três abordagens independentes.
- Pelo menos 10.000 jogos inéditos por família exploradora e tamanho de mesa, ajustados por potência.
- Resultado descrito como **resistência aos exploradores testados**, não exploitability exata ou prova de Nash.

---

# 8. Arquivos existentes relevantes

- [README.md](../README.md) — responsabilidades, instalação e índice da documentação.
- [.gitmodules](../.gitmodules) — fronteiras e referências dos três submódulos.
- [doc/war_manual_table_games.pdf](war_manual_table_games.pdf) — fonte normativa a certificar.
- [lib/war_game_engine/README.md](../lib/war_game_engine/README.md) — documentação da engine, runner e certificação.
- [lib/war_AI/README.md](../lib/war_AI/README.md) — treinamento, liga, avaliação e modelos.
- [lib/war_analyzer/src/war_analyzer.py](../lib/war_analyzer/src/war_analyzer.py) — caracterização e migração do protótipo.
- [lib/war_analyzer/src/war_analyzer_gemini.py](../lib/war_analyzer/src/war_analyzer_gemini.py) — captura, OCR, cores e âncora.
- [lib/war_analyzer/src/war_analyzer_resumed.py](../lib/war_analyzer/src/war_analyzer_resumed.py) — comparação entre variantes.
- [lib/war_analyzer/src/anchor_coordinates.py](../lib/war_analyzer/src/anchor_coordinates.py) — referência de calibração.
- [lib/war_analyzer/src/pixel_coordinates.py](../lib/war_analyzer/src/pixel_coordinates.py) — ferramenta de coordenadas.
- [lib/war_analyzer/src/pixel_hsv.py](../lib/war_analyzer/src/pixel_hsv.py) — inspeção de cores.
- [lib/war_analyzer/image/war_reference_ss_1.png](../lib/war_analyzer/image/war_reference_ss_1.png) — fixture digital inicial, não dataset suficiente.

Os destinos novos de pacotes, testes, configurações, documentação e artefatos estão detalhados no plano preservado para execução.

---

# 9. Verificação da entrega documental

Na criação do roadmap solicitado:

1. Preservar as fases, IDs de passos, dependências e critérios de saída.
2. Usar Markdown em português e sumário navegável.
3. Distinguir fatos atuais, propostas e requisitos ainda não certificados.
4. Ajustar links para a localização do documento na pasta de documentação.
5. Não apresentar fases futuras como implementadas.
6. Não afirmar que o manual foi lido nesta sessão.
7. Não alterar código dos submódulos como efeito colateral da criação do documento.
8. Registrar que métricas e premissas são revisáveis antes dos testes, mas não podem ser relaxadas depois para favorecer o resultado.

**Definição final de aprovação:** a v1.0 só será declarada quando a IA vencer a banca especificada com evidência estatística, jogar sob regras certificadas e operar ambos os clientes sem depender de informações indevidas ou de falhas silenciosas.