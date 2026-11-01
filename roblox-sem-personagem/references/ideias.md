# Como criar as ideias de um lote

Antes de escrever, rode `python scripts/lote.py historico`: ele mostra o registro da skill e os roteiros de `entregas/`. Nenhuma ideia pode repetir premissa, objetivo, mecânica, sequência de tentativas ou reviravolta de um vídeo anterior, de um exemplo da skill ou de outro vídeo do mesmo lote. Trocar cor, objeto, nome ou título da mesma brincadeira **não** é ideia nova.

## O que todas têm em comum

- O protagonista da ficha, na voz e no idioma do canal.
- Gancho em até 2 s com uma pergunta ou situação absurda; falas curtas; 25–35 s.
- Uma escolha com cortes secos nas opções e contagem 5-4-3-2-1 em boa parte dos vídeos, não em todos.
- Reviravolta boba e leve no fim. Humor físico, caretas e efeitos sonoros exagerados.
- **Muitas cores**: céu azul, gramado vivo, objetos saturados (vermelho, amarelo, azul, verde, rosa, roxo), confete, balões, luzes neon. Nada de cenário cinza ou vazio.
- Sem violência, sustos pesados, humilhação, palavrões, Robux grátis, links ou pedidos de dados; sem personagens, marcas ou músicas de terceiros.

## Variar dentro do lote

Distribua os vídeos por eixos diferentes e não repita eixo no mesmo lote enquanto houver outro livre:

- **Clima e natureza**: chuva, vento, neve, arco-íris, vulcão de brinquedo.
- **Comida e cozinha**: bolo gigante, pizza, sorvete que derrete, pipoca.
- **Esporte e brincadeira**: chute a gol, basquete, pula-corda, esconde-esconde, cabo de guerra.
- **Escola e casa**: lição, despertador, banho, arrumar o quarto, mochila.
- **Animais e pets**: cachorro, gato, pato, peixinho, sempre feitos de blocos.
- **Objetos mágicos**: botão misterioso, controle remoto, caixa surpresa, lâmpada.
- **Transporte**: carrinho, balão, foguete de papelão, skate, trem.
- **Festa e música**: aniversário, dança, show, presente.
- **Tamanho e física**: encolher e crescer, gravidade, ímã, mola.
- **Profissões de faz de conta**: cozinheiro, bombeiro, astronauta, mágico.

Formatos de história (alterne):

1. "Qual X ...?" com 3 opções, contagem e a escolhida dando errado de um jeito bobo.
2. Tentativas em sequência: a 1ª falha, a 2ª falha, a 3ª funciona do jeito mais inesperado.
3. Um problema persegue o protagonista e ele tenta fugir.
4. Desafio cronometrado com números na tela.
5. Antes e depois: ele faz algo e o resultado é exagerado.

## Registro

Para cada vídeo, `originalidade.json` com `premissa`, `objetivo`, `mecanica`, `tentativas`, `reviravolta`, `projetos_comparados` e `diferenca_dos_anteriores`. Confira de novo antes de gerar as vozes e antes de gravar. Depois da produção, `lote.py produzir` anota cada vídeo no registro. Confira se todos entraram.

## Cenas que a skill já faz bem

Use para variar sem inventar mecânica impossível: correr e andar (`K.mover`), cortes de lugar (`K.cortarPara`), escorregar (`K.deslizar`), voar e cair (`K.voar` + `K.deitado`), gesto com as mãos (`K.sixSeven`), objetos voando com tween, partículas (chuva, brilho, confete), portas, placas e medidores com SurfaceGui, caretas (`K.rosto`). Uma ideia que precisa de algo novo, como nadar ou dirigir de verdade, custa muito mais tempo de cena: prefira representar com cortes e objetos.

Mostre a lista curta de ideias ao usuário antes de gastar crédito de voz, para ele poder trocar alguma.
