# Contratos de transporte WAR v1.0

Este documento formaliza os contratos da seção 3.2 do roadmap. Os modelos
validados em Python são a fonte das JSON Schemas; o TypeScript é gerado dessas
schemas. Os contratos definem formatos e fronteiras de informação, não
certificam regras de jogo ou uma implementação da engine.

## Versionamento e envelope

Toda mensagem de transporte usa `ContractEnvelope`:

```json
{
  "schema_version": "1.0",
  "api_version": "1.0.0",
  "payload": {
    "contract_type": "public_game_state"
  }
}
```

`schema_version` identifica o formato do envelope; `api_version` identifica a
API. Ambos são obrigatórios e incompatibilidades são recusadas explicitamente
por `parse_contract_json`; campos desconhecidos também são recusados.

O envelope atual usa `schema_version: "1.0"` e `api_version: "1.0.0"`. Cada
dimensão semântica tem uma versão independente `MAJOR.MINOR.PATCH`: regras,
observação e seu encoder, ação e seu encoder, replay, dataset, modelo,
configuração de inferência e geometria visual. O `SemanticVersionVector`
registra essas dimensões; `contract_schema_version` permanece separado.

`RulesetSpec.rules_version`, `PlayerObservation.observation_schema_version` e
`Action.action_schema_version` identificam seus contratos específicos.
`parse_contract_json` recusa versões de API, observação e ação não suportadas;
`ReplayManifest`, `DatasetManifest`, `PolicyManifest` e `InferenceConfig`
preservam suas próprias versões para auditoria e compatibilidade.

`CertificateManifest` guarda o vetor vigente no momento da aprovação. A
função `certificate_invalidation_reasons` compara somente as dimensões de que
o escopo depende; resultado não vazio significa que o certificado histórico
não pode mais ser usado como evidência atual.

| Escopo do certificado | Dimensões que o invalidam |
|---|---|
| `engine` | Regras |
| `policy` | Regras, schemas e encoders de observação/ação, replay, dataset, modelo e inferência |
| `client` | Regras, API, schema do envelope, schemas de observação/ação e geometria |
| `replay` | Regras, API, schema do envelope, schema de ação e replay |
| `dataset` | Regras, schema do envelope, schemas e encoders de observação/ação, replay e dataset |

## Isolamento de informação

- `FullGameState` é privilegiado: inclui mãos/objetivos privados, ordem do
  baralho e estado aleatório interno. Não deve ser enviado ao agente.
- `PublicGameState` contém apenas dados públicos. Seus modelos recusam campos
  privados desconhecidos.
- `PlayerObservation` combina o estado público com a informação privada do
  próprio jogador, ações legais e eventos visíveis a ele. A validação recusa
  estado privado de outro jogador, eventos internos e versões de estado
  inconsistentes.
- `PlayerKnowledgeState` guarda fatos conhecidos; `BeliefState` guarda
  hipóteses com probabilidades. Uma hipótese não se torna fato por estar
  presente no estado de conhecimento.
- `ObservedBoard` representa evidência visual, não um estado lógico completo.
  Cada leitura é `known`, `unknown` ou `ambiguous`; valores ausentes não são
  inventados.

## Estado lógico e geometria

`TerritoryState` contém apenas ID canônico, proprietário e quantidade de
exércitos. Topologia do jogo fica em `MapSpec`; posição, âncora e polígono
visual ficam em `BoardGeometry`; recortes de pixels ficam em `ImageRegion`.
Nenhuma coordenada visual participa da identidade ou das regras de um
território.

`BoardSpec` é o catálogo validado do perfil WAR 1 clássico. Seu `MapSpec`
recusa IDs duplicados de territórios/continentes, colisões de nomes e aliases
(ignorando caixa, acentos e espaços), referências a continentes ou territórios
inexistentes, auto-arestas, arestas não direcionadas duplicadas, territórios
isolados e grafos desconexos. A validação do tabuleiro exige uma carta para
cada território e exatamente dois curingas; o baralho de objetivos deve
referenciar cada objetivo exatamente uma vez. O catálogo canônico contém 42
territórios, 79 adjacências não direcionadas, 44 cartas territoriais e 14
objetivos.

Cada território, continente, adjacência, baralho e objetivo canônico conserva
`source_references` com caminho e localização na fonte; referências às imagens
físicas também registram SHA-256. A instância está disponível como
[`WAR1_BOARD_SPEC`](../lib/war_game_engine/src/war_game_engine/board_spec.py),
e os validadores ficam em
[`contracts.py`](../lib/war_game_engine/src/war_game_engine/contracts.py).

`FullGameState` preserva mãos, objetivos, baralho e `random_streams_state`;
`PublicGameState` nunca inclui esses dados privados. `turn_player_id` identifica
quem está na vez e `decision_player_id` quem responde à decisão atual; os
campos antigos `active_player_id` continuam aceitos como alias de
compatibilidade do jogador da vez. Pools de reforço retêm a origem e as
restrições de destino; `MovementControl` mantém o registro de transferências
da vez. Validadores relacionam proprietários, contagens de territórios/exércitos,
participantes eliminados, pools e referências de movimento. Os contadores
inteiros não têm teto artificial.

[`to_public_game_state`](../lib/war_game_engine/src/war_game_engine/state.py) e
[`observe_player`](../lib/war_game_engine/src/war_game_engine/state.py) projetam
o estado sem expor RNG, mãos ou objetivos de outros jogadores. O motor fornece
[`validate_action`](../lib/war_game_engine/src/war_game_engine/engine.py),
`legal_actions()` e transições puras para reivindicação e colocação de reforços;
fases de combate e demais regras de turno permanecem no escopo da Fase 3.

Snapshots usam JSON canônico (UTF-8, chaves ordenadas, sem espaços variáveis e
sem NaN) e SHA-256 do estado. A restauração confere hash e `replay_version`;
snapshots completos exigem streams tipados restauráveis, enquanto snapshots
públicos/individuais não contêm a semente. `FullReplay` e `PublicReplay` são
contratos distintos. A sanitização pública remove outcomes privados, limpa
destinatários restritos e renumera os eventos; a reprodução rejeita versões
incompatíveis ou divergências no hash final. Implementação em
[`replay.py`](../lib/war_game_engine/src/war_game_engine/replay.py) e
[`serialization.py`](../lib/war_game_engine/src/war_game_engine/serialization.py).

## Exemplos validados

- [Estado público](../lib/war_game_engine/tests/fixtures/contracts/public_game_state.json)
- [Observação privada de um jogador](../lib/war_game_engine/tests/fixtures/contracts/player_observation_private.json)
- [Tabuleiro incompleto com leituras desconhecidas e ambíguas](../lib/war_game_engine/tests/fixtures/contracts/observed_board_incomplete.json)

## Artefatos gerados

- JSON Schema: [contract-envelope-v1.json](../lib/war_game_engine/src/war_game_engine/schemas/contract-envelope-v1.json)
- Tipos TypeScript: [contracts.generated.ts](../lib/war_analyzer/pwa/src/contracts.generated.ts)

Para regenerar as schemas, instale o pacote engine no ambiente Python ativo e
execute `python3 scripts/export_contract_schema.py` a partir do submódulo
`war_game_engine`. Depois, em `lib/war_analyzer/pwa/`, execute
`npm run generate:contracts`.
