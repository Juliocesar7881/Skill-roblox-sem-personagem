# Lições de cena e edição

Erros já vistos em lotes reais e a correção de cada um. Complementam [production-rules.md](production-rules.md) e [first-time-right.md](first-time-right.md). A auditoria não vê boa parte deles: olhe a folha de quadros.

## O que a auditoria não vê

- Objeto não colidível entre a câmera e o rosto (espuma, maçã na mão, pernas num inserto de chão): olhe a folha.
- `K.inserto(false)` de um corte com `K.cortarPara` vai **dentro** da função da câmera, senão o quadro do corte acusa "rosto fora do quadro".
- Coisa larga no 9:16 (arco-íris, abóbora ao lado da casa) fica fina no meio do quadro: aproxime, ponha em profundidade e use câmera baixa.
- Porta ou janela numa superfície curva (abóbora gigante) precisa ser calculada contra a casca, senão some dentro dela.
- Torre ou objeto balançando: câmera com `cam.seguir` e balanço para longe dos sólidos.
- Objeto preso na mão do personagem **sentado**: não use solda na mão, porque a pose das pernas se desfaz e elas entram no chão. Faça o objeto seguir as mãos a cada quadro.
- Travelling ou zoom cortado antes de terminar: use `c.ate_corte(t)` como duração e alongue o plano se ficar curto. O `escrever()` recusa a cena.
- Efeito sonoro cortado no meio (`dur` curto num som longo, ou som passando do fim do vídeo): toque o som inteiro ou troque por um curto. O `edicao.py` recusa.
- Objeto pendurado (isca, pesca) longe do rosto ou na frente da boca: confira na folha. Linha passando perto da câmera vira uma faixa branca.
- Objeto principal sempre inteiro no quadro nos insertos, e nada cobrindo texto do cenário.

## Causas de colisão já resolvidas

Rode `montar` + `rodar` **sem** `--gravar` e leia as linhas `[auditoria]` (intervalo de tempo, parte do corpo, objeto) e `[auditoria-detalhe]` (posição e orientação no primeiro contato). Corrija a causa até `total 0`.

| Sintoma | Correção |
|---|---|
| Corpo enterrado | Posição em pé sem o piso: use `K.emPe` e marque o chão com `K.piso` |
| Pernas atravessando a rampa | O kit já usa bissetriz e folga; use `K.sentarEm` e confira os pontos do caminho |
| Animação trocando antes de carregar | `K.preCarregar` antes da cena |
| Pose sentada misturando com a em pé | `K.sentarEm` |
| Pernas esticadas na saída da rampa | O voo já troca a pose aos 15%: não force outra animação ali |
| Chegada de corrida em cima de outra peça | Mude o destino |

## Câmera

- Regra medida no quadro final: rosto com pelo menos 8–10% da altura, nunca de costas, perfil só de passagem, rosto inteiro dentro do 9:16 e fora da faixa da legenda.
- `cam.seguir(noob.Head, desl, t, V(0, -1.5, 0))`, na frente ou em três quartos do olhar e mirando abaixo da cabeça, resolve a maioria dos avisos. No pouso de costas, plano de cima com `cima = V(0, 0, 1)`.
- Grave a versão final com `--frente`: com a janela na frente a captura fica perto de 55 fps.
- Confira os tempos dos cortes (`select='gt(scene,0.25)'`) contra a timeline: com as marcas de sincronia eles caem a ±2 quadros.

## Atuação

- No pouso use `idle`. Nunca pare todas as animações: o R15 deitado fica em pose T.
- `K.foco(noob.Head)` deixa o fundo desfocado nos closes.
- Nada de `K.tremer` na contagem: a tensão vem do rosto e do olhar.
- Não imponha corte a cada 1–2 s. Mova a câmera quando a história pedir.

## Edição e som

- Descidas de escorregador com atrito de plástico: `escorregar-trava` em `T['trava'] - 2.0`, com o rangido no instante da parada; `escorregar-rapido` no início da descida de 2,2 s, com lufada no lançamento; apito de desenho descendo até o impacto.
- Tombo: impacto + explosão + zoom-soco + tremida + flash, com BOOM! e estrelas de tontura.
- Contagem: selos `contagem-5..1.png` com clique e batimento de coração, zoom-soco leve por número e nenhuma tremida.
- Vinheta de trombone no final, whoosh nos cortes, "erro" e `?!` quando algo dá errado.
- Velocidade se mostra com tremida leve e zoom. **Não use o sticker `linhas-velocidade`**: foi reprovado.
- Suor só da careta, sem sticker de gotas.
- Por trecho, atrito e apito ficam 4–6 LU abaixo da voz.
- Se uma fala sair errada no arquivo inteiro, transcreva só o trecho dela antes de concluir que há mascaramento.
- Apague gravações intermediárias grandes que não forem mais úteis.
