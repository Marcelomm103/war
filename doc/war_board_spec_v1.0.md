# Inventário do tabuleiro e componentes — WAR 1 clássico

**Passo do roadmap:** 0.4 — certificar mapa e componentes  
**Data:** 2026-10-02  
**Estado:** inventário visual T01–T42 e lista de adjacências fornecida pelo usuário registrados; a reciprocidade da lista foi verificada. Este documento não é uma implementação de regras. O mapa não foi auditado independentemente aresta a aresta.

## Precedência e procedência

- Fonte visual disponibilizada pelo usuário: [mapa_war_classico.webp](images/mapa_war_classico.webp) e folhas [war_cartas1.png](images/war_cartas1.png) a [war_cartas8.png](images/war_cartas8.png). O usuário identificou o alvo como WAR 1 clássico e definiu as cartas/mapa físicos como referência normativa para objetivos e identidade dos territórios.
- A imagem do mapa é uma fotografia do tabuleiro, com perspectiva, vincos/reflexos e resolução limitada; os nomes, regiões coloridas, bônus e rotas assinaladas são legíveis em boa parte. As folhas de cartas são imagens dos cartões, não fotos independentes dos componentes recortados.
- A identificação normativa do usuário prevalece sobre nomes e listas hardcoded dos protótipos de `war_analyzer`. Não se adotou informação de outra edição nem se presumiu uma regra por familiaridade com Risk.
- Os IDs `T01`–`T42` abaixo são **chaves internas deste inventário**, atribuídas na ordem de leitura das cartas. Não são números impressos no jogo, não derivam dos nomes nem de coordenadas; não devem ser renumerados quando se alterarem traduções ou aliases.
- Os assets estão presentes no workspace, mas ainda aparecem como não versionados no agregador. Os SHA-256 registrados abaixo identificam exatamente as imagens examinadas.

| Asset | SHA-256 |
|---|---|
| [mapa_war_classico.webp](images/mapa_war_classico.webp) | `6877a96fa88616202eb9448e494ccb82f9c2dc2edf207daf2c33cfe6584548b8` |
| [war_cartas1.png](images/war_cartas1.png) | `96e7e9eb60f894ec931b716c35d47c4a22922c25ce1ede28ac3f01ef965adde3` |
| [war_cartas2.png](images/war_cartas2.png) | `b7b8aa7fed5fc40bcb5d0b3e48a707501d7ca793641a4ca40de66b6ce888ced9` |
| [war_cartas3.png](images/war_cartas3.png) | `a30f23c9c74501cb884270e0043e58f7e5c344aa726c84fb8a21934816ee958a` |
| [war_cartas4.png](images/war_cartas4.png) | `3eca1085759d76a5d851832ac32a9a24f7681f2c17819faade31d0445beb8b04` |
| [war_cartas5.png](images/war_cartas5.png) | `ec7721e82d16eea729a67476e9b3e3923d28a5c11f0acc64b9a52d971bcba3d3` |
| [war_cartas6.png](images/war_cartas6.png) | `31f68045e7ce16d6f38443654a1c22d431bc03e0d9b0402c7bd911532c12486f` |
| [war_cartas7.png](images/war_cartas7.png) | `8df2cedb06784e97c7896d15689c15fb940d8f5ef7d5ed79672db0587d56c6b9` |
| [war_cartas8.png](images/war_cartas8.png) | `bcfe2c7719b208012def366fe19895074cb727bdc32eb999211ee978bd5242bf` |

## Catálogo de territórios

A coluna “símbolo” registra a figura impressa na carta: triângulo (`△`), círculo (`○`) ou quadrado (`□`). Os dois aliases compostos explicitados pelo usuário são Colômbia/Venezuela e Bolívia/Peru/Chile: em cada caso, o nome da carta é o ID canônico. Sub-rótulos geográficos menores impressos dentro de outras áreas do mapa (por exemplo, Uruguai, Portugal/Espanha/Itália e Iugoslávia) permanecem dentro do território nomeado pela carta e não criam IDs adicionais.

| ID interno | Nome canônico da carta | Continente do mapa | Alias/rótulo cartográfico | Símbolo | Folha |
|---|---|---|---|---|---|
| T01 | Austrália | Oceania | — | △ | [war_cartas1.png](images/war_cartas1.png) |
| T02 | Nova Guiné | Oceania | — | ○ | [war_cartas1.png](images/war_cartas1.png) |
| T03 | Sumatra | Oceania | — | □ | [war_cartas1.png](images/war_cartas1.png) |
| T04 | Bornéu | Oceania | — | □ | [war_cartas1.png](images/war_cartas1.png) |
| T05 | Alaska | América do Norte | — | △ | [war_cartas1.png](images/war_cartas1.png) |
| T06 | Groenlândia | América do Norte | — | ○ | [war_cartas1.png](images/war_cartas1.png) |
| T07 | Nova York | América do Norte | — | △ | [war_cartas1.png](images/war_cartas1.png) |
| T08 | Califórnia | América do Norte | — | □ | [war_cartas1.png](images/war_cartas1.png) |
| T09 | Vancouver | América do Norte | — | △ | [war_cartas2.png](images/war_cartas2.png) |
| T10 | Mackenzie | América do Norte | — | ○ | [war_cartas2.png](images/war_cartas2.png) |
| T11 | Labrador | América do Norte | — | □ | [war_cartas2.png](images/war_cartas2.png) |
| T12 | México | América do Norte | — | □ | [war_cartas2.png](images/war_cartas2.png) |
| T13 | Ottawa | América do Norte | — | ○ | [war_cartas2.png](images/war_cartas2.png) |
| T14 | África do Sul | África | — | △ | [war_cartas2.png](images/war_cartas2.png) |
| T15 | Egito | África | — | △ | [war_cartas2.png](images/war_cartas2.png) |
| T16 | Congo | África | — | □ | [war_cartas2.png](images/war_cartas2.png) |
| T17 | Madagascar | África | — | ○ | [war_cartas3.png](images/war_cartas3.png) |
| T18 | Argélia | África | — | ○ | [war_cartas3.png](images/war_cartas3.png) |
| T19 | Sudão | África | — | □ | [war_cartas3.png](images/war_cartas3.png) |
| T20 | Índia | Ásia | — | □ | [war_cartas3.png](images/war_cartas3.png) |
| T21 | Sibéria | Ásia | — | △ | [war_cartas3.png](images/war_cartas3.png) |
| T22 | Tchita | Ásia | — | △ | [war_cartas3.png](images/war_cartas3.png) |
| T23 | Vietnã | Ásia | — | △ | [war_cartas3.png](images/war_cartas3.png) |
| T24 | Japão | Ásia | — | □ | [war_cartas3.png](images/war_cartas3.png) |
| T25 | Argentina | América do Sul | Uruguai (sub-rótulo geográfico dentro do território da carta) | □ | [war_cartas4.png](images/war_cartas4.png) |
| T26 | Brasil | América do Sul | — | ○ | [war_cartas4.png](images/war_cartas4.png) |
| T27 | Colômbia | América do Sul | Venezuela | △ | [war_cartas4.png](images/war_cartas4.png) |
| T28 | Alemanha | Europa | — | ○ | [war_cartas4.png](images/war_cartas4.png) |
| T29 | França | Europa | Portugal / Espanha / Itália (sub-rótulos geográficos dentro do território da carta) | □ | [war_cartas4.png](images/war_cartas4.png) |
| T30 | Inglaterra | Europa | — | ○ | [war_cartas4.png](images/war_cartas4.png) |
| T31 | Suécia | Europa | — | ○ | [war_cartas4.png](images/war_cartas4.png) |
| T32 | Islândia | Europa | — | △ | [war_cartas4.png](images/war_cartas4.png) |
| T33 | Polônia | Europa | Iugoslávia (sub-rótulo geográfico dentro do território da carta) | □ | [war_cartas6.png](images/war_cartas6.png) |
| T34 | Moscou | Europa | — | △ | [war_cartas6.png](images/war_cartas6.png) |
| T35 | China | Ásia | — | ○ | [war_cartas7.png](images/war_cartas7.png) |
| T36 | Dudinka | Ásia | — | ○ | [war_cartas7.png](images/war_cartas7.png) |
| T37 | Mongólia | Ásia | — | ○ | [war_cartas7.png](images/war_cartas7.png) |
| T38 | Omsk | Ásia | — | □ | [war_cartas7.png](images/war_cartas7.png) |
| T39 | Oriente Médio | Ásia | — | □ | [war_cartas7.png](images/war_cartas7.png) |
| T40 | Vladvostok | Ásia | — | ○ | [war_cartas7.png](images/war_cartas7.png) |
| T41 | Aral | Ásia | — | △ | [war_cartas7.png](images/war_cartas7.png) |
| T42 | Bolívia | América do Sul | Peru / Chile | △ | [war_cartas7.png](images/war_cartas7.png) |

### Contagem e bônus continentais

| Continente | Territórios nesta transcrição | Contagem | Bônus por controle integral (Tabela I) |
|---|---|---:|---:|
| América do Norte | T05–T13 | 9 | +5 exércitos |
| América do Sul | T25–T27, T42 | 4 | +2 exércitos |
| Europa | T28–T34 | 7 | +5 exércitos |
| África | T14–T19 | 6 | +3 exércitos |
| Ásia | T20–T24, T35–T41 | 12 | +7 exércitos |
| Oceania | T01–T04 | 4 | +2 exércitos |
| **Total** | **T01–T42** | **42** | — |

Os bônus coincidem com a Tabela I impressa no tabuleiro e com a regra do manual, p. 3, de colocação do bônus nos territórios do próprio continente. O grafo de adjacências deve usar os IDs acima, e não o texto dos nomes nem posição em pixels.

### Baralho de territórios e peças

| Componente | Quantidade/valor verificado | Evidência |
|---|---|---|
| Cartas territoriais | 42, uma por ID T01–T42 | Oito folhas de cartas; nomes/símbolos conferidos visualmente |
| Curingas | 2; cada carta mostra as três figuras possíveis | [war_cartas6.png](images/war_cartas6.png); manual, p. 2 e 8 |
| Triângulos | 14 cartas | Contagem visual do catálogo acima |
| Círculos | 14 cartas | Contagem visual do catálogo acima |
| Quadrados | 14 cartas | Contagem visual do catálogo acima |
| Cartas de objetivo | 14 | [war_cartas5.png](images/war_cartas5.png), [war_cartas6.png](images/war_cartas6.png), [war_cartas8.png](images/war_cartas8.png); detalhes em [war_rules_traceability_v1.0.md](war_rules_traceability_v1.0.md) |
| Conjuntos de exércitos | 6 cores: branca, vermelha, preta, azul, amarela e verde | Manual, p. 2; confirmação do usuário |
| Denominações de fichas | Ficha pequena = 1 exército; ficha grande = 10 exércitos | Manual, p. 2 |
| Quantidade de fichas físicas por cor | Não determinada pela evidência disponível | Sem inventário visual/fotografia dos conjuntos físicos |
| Dados de combate | 3 vermelhos para ataque e 3 amarelos para defesa | Manual, p. 2 |

## Adjacências — lista corrigida e reciprocidade verificada

O usuário forneceu a tabela completa de vizinhanças corrigidas em [war_adjacency_review_v1.0.md](war_adjacency_review_v1.0.md). Após a correção mais recente — T21–T37 removido e T36–T37 mantido — ela foi sincronizada no [JSON de adjacências](war_adjacency_candidate_v1.0.json): 42 territórios, 79 pares não direcionados (158 declarações recíprocas). O JSON não atribui tipo de ligação (fronteira/rota), pois a tabela corrigida do usuário não fez essa distinção.

**Resultado da checagem solicitada:** a tabela final contém T01–T42 uma vez cada; todos os destinos são IDs válidos; não há auto-adjacências, vizinhos repetidos, territórios isolados ou componentes desconexos; cada ligação aparece nas duas listas. A correção final do usuário removeu T21–T37 em ambos os sentidos e confirmou T36–T37. O resultado contém 79 pares únicos e 158 declarações recíprocas.

Esta validação comprova a consistência recíproca da lista fornecida pelo usuário, que é a referência do projeto; **não** é uma auditoria visual independente da fotografia. As antigas arestas inferidas pelo assistente e suas alternativas foram substituídas, não misturadas à lista corrigida. Não se deve voltar a usar as hipóteses do rascunho anterior nem importar ligações de outra edição/variante.

### Verificação suplementar (não bloqueadora)

Não há pendências de reciprocidade na lista entregue pelo usuário. Uma inspeção física/fotográfica independente dos endpoints pode ser realizada como evidência suplementar se o projeto exigir prova visual além da regra fornecida pelo usuário; ela não altera silenciosamente esta lista.

**Observação suplementar, não bloqueadora:** a quantidade de fichas físicas de cada denominação/cor não está inventariada; o manual confirma as cores e os valores pequena=1/grande=10. Essa contagem pode ser feita se for necessária para especificação de visão ou logística, mas não substitui nem altera o checklist normativo do passo.

**Conclusão do passo 0.4:** inventário de territórios, continentes, cartas/símbolos, bônus e denominações documentado; lista completa de adjacências fornecida/corrigida pelo usuário e checada para reciprocidade, cobertura e integridade estrutural. **Passo 0.4 concluído no escopo especificado**, com ressalva de que não foi feita auditoria fotográfica independente da topologia.
