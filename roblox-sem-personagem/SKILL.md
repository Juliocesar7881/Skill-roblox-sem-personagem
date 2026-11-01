---
name: roblox-sem-personagem
description: "Cria Shorts animados de Roblox (9:16, ~25-35 s) com um protagonista próprio: no primeiro uso a skill pergunta o canal e monta o personagem com o usuário. Depois faz roteiro original, voz no ElevenLabs, cena animada no Roblox Studio pela linha de comando oficial (sem cliques), gravação só da janela do Studio e edição final com legendas palavra a palavra, efeitos sonoros e música. Use para 'faz um short', 'fazer vídeos da semana', 'agendar os shorts', 'configurar meu canal' ou 'criar meu personagem'."
---

# Roblox sem personagem

Transforma uma ideia ("faz um de qual escorregador é o mais rápido") em um Short vertical **pronto para postar**, animado no Roblox Studio. A skill vem **sem canal e sem protagonista**: quem usa define os dois no primeiro uso.

## Primeiro uso: setup obrigatório

Rode antes de qualquer outra coisa:

```bash
python scripts/configurar.py status
```

Se sair `FALTA: ...`, siga [references/setup.md](references/setup.md) antes de escrever roteiro ou gastar crédito de voz. Enquanto faltar algo, `lote.py novo`, `fazer_short.py` e `studio_runscript.py montar --kit` recusam rodar. Pergunte só o que falta e não invente canal, nome, visual ou voz: isso é escolha do usuário.

Com `Setup completo.`, o `status` mostra o canal, o idioma, o público e o protagonista. Tudo fica em `config.local.json`. Para ler a ficha inteira, abra esse arquivo. Depois disso, valem estes termos no resto da skill:

- **Protagonista:** o personagem da ficha. Nas cenas o modelo se chama sempre `Protagonista`, e no Lua a variável é `noob` (nome herdado do kit).
- **Idioma do canal:** `idioma` da configuração. Roteiro, voz, legendas, placas no cenário, título, descrição, tags e nomes de arquivo saem nele, sempre.
- **Voz:** `personagem.voz` da ficha. Não troque sem o usuário pedir.
- **Assinatura:** `personagem.assinatura`, a expressão que marca o personagem no fim dos vídeos.
- **Personalidade:** `personagem.personalidade` guia as falas e as reações.

Leia [references/production-rules.md](references/production-rules.md), [references/format.md](references/format.md) e [references/animkit.md](references/animkit.md) antes de produzir, e [references/youtube-studio.md](references/youtube-studio.md) antes de postar. Depois das falas prontas, rode `scripts/fazer_short.py PROJETO`: ele faz auditoria, gravação, edição, revisão de legendas e render, e só termina com o MP4 final. `--so-conferir` só confere a entrega.

A skill depende da pasta irmã `roblox-video-editor` (renderizador, biblioteca de efeitos e músicas, stickers), que o `install.py` deste repositório instala junto.

## Voz (ElevenLabs)

- Use a cópia da voz em **Voices → My Voices**, modelo **Eleven v4**, idioma Automático. As cópias da aba Explorar podem pedir plano pago. Nunca sugira pagar: a escolha é do usuário.
- Escreva cada fala no idioma do canal com uma tag de emoção no início: `[excited]`, `[giggles]`, `[gasps]`, `[whispers]`. Se a ficha tiver `voz.sotaque`, comece toda fala com ele (por exemplo `[Brazilian Portuguese accent]`, sem o qual a voz às vezes muda de sotaque).
- No `roteiro.json`: `"vozes": {"ID": "NOME DA VOZ"}`, com o `id` da ficha.
- Como gerar:
  - Com chave em `ELEVENLABS_API_KEY` (o próprio usuário define): `python scripts/tts_elevenlabs.py roteiro.json --out falas`.
  - Sem chave, no navegador logado do usuário: gere **uma tomada por vídeo** com todas as falas, uma por parágrafo (digite com teclas reais e Enter entre as falas; nunca `execCommand` no editor, ele trava a aba). Das duas versões que o site cria, fique com a `eleven_v4` (confira `model_id` no JSON do histórico, não a ordem). Mova os arquivos com `scripts/receptor_falas.py PASTA` (servidor local em 127.0.0.1) e `postMessage`: abra a janela do receptor uma vez com clique real e mande cada tomada para ela. Depois `python scripts/dividir_falas.py PROJETO TOMADA.mp3` corta em `falas/fala-NN.mp3`, e `python scripts/alinhar_falas.py roteiro.json falas` confere cada fala contra o roteiro. Os ajudantes estão em `scripts/elevenlabs_helpers.js`.
  - Nunca digite senha nem chave do usuário.
- Uso comercial no ElevenLabs depende do plano da conta: avise uma vez, sem insistir.

## Originalidade em cada vídeo

Todo vídeo novo precisa de **ideia e roteiro inéditos**. Antes de escrever, rode `python scripts/lote.py historico` e compare premissa, objetivo, mecânica, tentativas e reviravolta com tudo o que já foi feito. Trocar cor, nome ou objeto do mesmo desafio não faz uma ideia nova. Salve `originalidade.json` no projeto (`premissa`, `objetivo`, `mecanica`, `tentativas`, `reviravolta`, `projetos_comparados`, `diferenca_dos_anteriores`). Depois de produzir, registre com `python scripts/registrar_roteiro.py PROJETO`.

## Como o Studio é controlado (sem MCP, sem cliques)

A tarefa de linha de comando do Roblox Studio roda um script no place em modo edição e inicia o Play: `RobloxStudioBeta.exe -task RunScript -localPlaceFile place.rbxlx -runScriptFile script.lua -outputFile out.log -quitAfterExecution`.

- `scripts/studio_runscript.py montar --kit --cenario studio/cenario.lua --cena studio/cena.lua --play --saida studio/pipeline.lua` instala o AnimKit com o protagonista da ficha, monta o cenário, instala a cena e roda o Play.
- `scripts/studio_runscript.py rodar studio/pipeline.lua --place studio/base.rbxlx --gravar viewport.mp4` abre uma janela nova do Studio atrás das janelas do usuário e grava **só essa janela**. Nunca grave a área de trabalho inteira.
- As janelas do Studio do próprio usuário nunca são tocadas.
- **A tela precisa estar ligada para gravar.** Com o monitor desligado, o Studio não desenha o viewport 3D e o Play também congela movimentos. Escreva as cenas e grave com a tela ligada.

## Fluxo

1. **Lote**: `python scripts/lote.py novo` cria `entregas/lote-AAAAMMDD/` com a base comum (`comum.py`, `edicao.py`, `cenario_comum.lua`) e as pastas `NN-to-define`. Renomeie para `NN-<tema>`. Cada projeto tem `gerar_cena.py`, `montar_edicao.py`, `studio/cenario_corpo.lua` e `roteiro.json`.
2. **Roteiro** (`roteiro.json`): `texto` de cada fala no idioma do canal, `titulo`, `arquivo` (nome do MP4), `"idiomas": ["IDIOMA"]`, `vozes`, `destaques` (palavras em amarelo) e plano por fala. Falas curtas, uma ideia por fala, com tag de emoção. Formato em [references/format.md](references/format.md).
3. **Voz**: como acima.
3b. **Planeje cada plano antes de escrever Lua** ([references/first-time-right.md](references/first-time-right.md)): tabela de batidas na docstring do `gerar_cena.py` (onde estão o protagonista, o objeto principal e a câmera, e o que precisa aparecer). A meta é uma gravação por vídeo. `scripts/lint_cena.py`, rodado por `auditar.py` e `fazer_short.py`, bloqueia os erros conhecidos antes do Studio.
4. **Cenário** (`studio/cenario_corpo.lua`):
   - Colorido e vivo, com objetos em volta.
   - Marque todo chão com `K.piso(...)`.
   - Crie o protagonista com `K.criarProtagonista("Protagonista", K.emPe(pos, olharPara))`.
5. **Cena** (`gerar_cena.py` → `studio/cena.lua`):
   - A timeline vem dos tempos reais da voz, e toda fala tem `K.falar` com o envelope do MP3.
   - As expressões seguem a emoção: `happy`, `smile`, `surprised`, `scared`, `scream`, `nervous`, `confident`, `angry`, `doubt`, `dizzy`, `squint`, `knockout` e `wink`.
   - Use cortes secos e `K.cortarPara` quando o personagem muda de lugar.
   - Movimentos de câmera terminam antes do próximo corte (`c.ate_corte`).
6. **Auditoria automática e correção (obrigatória)**: `K.auditar(noob)` (colisões) e `K.auditarCamera(noob)` (regra do rosto) têm de terminar com `total 0`. Cabelo, acessórios, roupa por cima e saia são partes moles (`Visual`) e ficam fora da auditoria. No lote, `python auditar.py NN-projeto ...` roda `gerar_cena.py`, monta e dá Play em cada cena sem gravar e imprime só as linhas da auditoria. Depois revise os quadros em volta de cada corte, inclusive todos os quadros de 60 fps de 0,05 s antes a 0,1 s depois.
7. **Edição** (`montar_edicao.py` → renderizador da `roblox-video-editor`, `"entrega": "shorts"`):
   - Legendas karaokê no idioma do canal, uma ideia por vez.
   - Um grupo nunca termina em artigo ou preposição, e as negações saem em coral (listas por idioma em `scripts/legendas.py`; para outro idioma, acrescente as listas lá).
   - Efeito sonoro em toda ação.
   - Nunca corte um efeito no meio nem um zoom antes do fim.
   - Música curta licenciada a −24 dB sob a voz.
   - **Nenhum efeito por cima de palavra falada**: `python conferir_sfx.py NN-projeto` lista os que tocam sobre a voz. Corrija todos (mova a ação para uma pausa, use um som mais curto).
   - Stickers com palavra no idioma do canal: em português `wow`, `oops`, `kkkk`, `tum`; nos outros idiomas `wow-en`, `oops-en`, `haha-en`. `confete`, `interrogacao`, `estrelas-tontas` e `check` servem para todos.
8. **Revisão final**: `revisar_legendas.py` total 0, cerca de −14 LUFS com pico abaixo de −1,5 dBTP, transcrição do áudio final no idioma do canal com Whisper e conferência dos quadros.
9. **Entrega** (`fazer_short.py PROJETO --so-conferir`): o MP4 final mais `publicacao.txt` com título, descrição, hashtags, créditos das músicas e crédito da voz, no idioma do canal.

## Postagem

- Canal: o da configuração. Um lote pode indicar outro canal do usuário em `lote.json` (`"canal"`), só quando ele pedir. Horários e quantidade por dia vêm de `horarios` (`lote.py agenda`).
- Público: `feito_para_criancas` da configuração, salvo se `lote.json` ou `roteiro.json` disserem outra coisa. Categoria Jogos com o título de jogo Roblox.
- `lote.py metadados` escreve título, descrição e tags com SEO e os créditos. As thumbnails ficam com o dono do canal.
- Envio e agendamento no YouTube Studio em [references/youtube-studio.md](references/youtube-studio.md).
- TikTok (opcional, se a configuração tiver `tiktok.handle`): cada vídeo vai também para esse perfil, na mesma data e hora, com o mesmo título, descrição e tags (`lote.py tiktok`, `lote.py pacote`). O TikTok só agenda 30 dias à frente. Passos em [references/tiktok-studio.md](references/tiktok-studio.md).
- Pedir para fazer os vídeos não autoriza postar. Só agende ou publique quando o usuário pedir, e só o que ele pedir, no canal dele. Nunca poste em outro canal, nunca digite senhas, e nunca aceite termos ou permissões de uma conta sem o ok do usuário no chat.

## Regras de conteúdo

- Roteiros originais. Referências do usuário valem só como formato.
- Sem Robux de verdade, links, pedido de dados pessoais, sustos pesados, humilhação ou palavrões. Reviravoltas bobas e leves.
- Sem personagens, logos ou músicas de terceiros.
- O protagonista segue a personalidade da ficha. Ele pode errar e rir disso, sem maldade.
- Varie cenários, piadas e ângulos entre os vídeos: vozes de IA e roteiros em série podem ser vistos como conteúdo repetitivo.
