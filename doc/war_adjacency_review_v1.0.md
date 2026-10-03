# Revisão do grafo de adjacências — WAR 1 clássico

**Estado:** lista corrigida pelo usuário; consistência recíproca verificada em 2026-10-02. Não houve auditoria visual independente aresta a aresta.  
**Fonte:** [mapa WAR 1](images/mapa_war_classico.webp), SHA-256 `6877a96fa88616202eb9448e494ccb82f9c2dc2edf207daf2c33cfe6584548b8`.  
**Dados editáveis/máquina:** [grafo JSON](war_adjacency_candidate_v1.0.json).  
**IDs e continentes:** [inventário T01–T42](war_board_spec_v1.0.md).

## Como ler e corrigir

- Os pares são **não direcionados**: se `T01 — T02` aparece, significa ligação nos dois sentidos.
- A tabela abaixo reproduz a lista corrigida pelo usuário. Como ela não classifica as ligações como fronteiras ou rotas marítimas, não atribuo tipo de aresta.
- Correção mais recente do usuário: T21–T37 **não** é adjacência; T36–T37 **é** adjacência. O par T21–T37 foi retirado das duas listas, mantendo T36–T37 nos dois sentidos.
- As hipóteses visuais e alternativas do rascunho anterior foram substituídas pela lista corrigida completa do usuário e não fazem parte do grafo atualizado.

## Vizinhanças corrigidas

| ID | Território | Vizinhos corrigidos |
|---|---|---|
| T01 | Austrália | T02; T03; T04 |
| T02 | Nova Guiné | T01; T04 |
| T03 | Sumatra | T01; T20 |
| T04 | Bornéu | T01; T02; T23 |
| T05 | Alaska | T09; T10; T40 |
| T06 | Groenlândia | T10; T11; T32 |
| T07 | Nova York | T08; T11; T12; T13 |
| T08 | Califórnia | T07; T09; T12; T13 |
| T09 | Vancouver | T05; T08; T10; T13 |
| T10 | Mackenzie | T05; T06; T09; T13 |
| T11 | Labrador | T06; T07; T13 |
| T12 | México | T07; T08; T27 |
| T13 | Ottawa | T07; T08; T09; T10; T11 |
| T14 | África do Sul | T16; T17; T19 |
| T15 | Egito | T18; T19; T29; T33; T39 |
| T16 | Congo | T14; T18; T19 |
| T17 | Madagascar | T14; T19 |
| T18 | Argélia | T15; T16; T19; T26; T29 |
| T19 | Sudão | T14; T15; T16; T17; T18 |
| T20 | Índia | T03; T23; T35; T39; T41 |
| T21 | Sibéria | T22; T36; T40 |
| T22 | Tchita | T21; T35; T36; T37; T40 |
| T23 | Vietnã | T04; T20; T35 |
| T24 | Japão | T35; T40 |
| T25 | Argentina | T26; T42 |
| T26 | Brasil | T18; T25; T27; T42 |
| T27 | Colômbia | T12; T26; T42 |
| T28 | Alemanha | T29; T30; T33 |
| T29 | França | T15; T18; T28; T30; T33 |
| T30 | Inglaterra | T28; T29; T31; T32 |
| T31 | Suécia | T30; T34 |
| T32 | Islândia | T06; T30 |
| T33 | Polônia | T15; T28; T29; T34; T39 |
| T34 | Moscou | T31; T33; T38; T39; T41 |
| T35 | China | T20; T22; T23; T24; T37; T38; T40; T41 |
| T36 | Dudinka | T21; T22; T37; T38 |
| T37 | Mongólia | T22; T35; T36; T38 |
| T38 | Omsk | T34; T35; T36; T37; T41 |
| T39 | Oriente Médio | T15; T20; T33; T34; T41 |
| T40 | Vladvostok | T05; T21; T22; T24; T35 |
| T41 | Aral | T20; T34; T35; T38; T39 |
| T42 | Bolívia | T25; T26; T27 |

## Alternativas do rascunho visual anterior — superadas

Os pares abaixo foram sugestões de baixa confiança do primeiro rascunho visual. A lista corrigida pelo usuário substitui essas hipóteses; elas são mantidas apenas como histórico e **não** fazem parte do grafo atual.

| ID A | ID B | Motivo de revisão |
|---|---|---|
| T10 | T11 | Mackenzie–Labrador: possível fronteira sob a costa/baía; verificar se Ottawa separa completamente as regiões. |
| T13 | T06 | Ottawa–Groenlândia: rota na região, mas o endpoint norte-americano pode ser Ottawa ou Labrador. |
| T15 | T33 | Egito–Polônia: endpoint europeu próximo à zona Polônia/Bálcãs; atribuição incerta. |
| T15 | T29 | Egito–França: possível rota mediterrânea; confirmar o endpoint europeu. |
| T18 | T33 | Argélia–Polônia: verificar se o endpoint europeu da rota corresponde à região da Polônia. |
| T19 | T33 | Sudão–Polônia: possível rota/endpoint na região dos Bálcãs. |
| T16 | T17 | Congo–Madagascar: a rota visível para Madagascar pode sair do Congo ou do Sudão. |
| T28 | T31 | Alemanha–Suécia: conferir possível ligação direta na área meridional da Suécia. |
| T24 | T37 | Japão–Mongólia: não identifiquei endpoint claro; incluído para revisão da área Ásia-Pacífico. |
| T24 | T02 | Japão–Nova Guiné: possível rota oceânica, sem endpoints suficientemente distinguíveis. |
| T03 | T04 | Sumatra–Bornéu: proximidade visual, mas não identifiquei arco direto inequívoco. |

## Validações estruturais executadas

A tabela após a correção final foi checada: 42 IDs T01–T42 presentes exatamente uma vez; destinos válidos; nenhuma auto-adjacência ou vizinho duplicado; nenhum vínculo unilateral; **158 declarações recíprocas correspondentes a 79 pares não direcionados únicos**; nenhum território isolado; grafo conexo. A validação confirma consistência da lista corrigida pelo usuário. O JSON deve representar exatamente esses 79 pares.

Esta verificação não classifica arestas em fronteiras/rotas nem constitui auditoria fotográfica independente da topologia física.
