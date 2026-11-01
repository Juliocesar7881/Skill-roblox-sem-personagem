# Skill Roblox sem personagem

Skill do Claude Code que faz Shorts animados de Roblox do início ao fim, com o **seu** canal e o **seu** protagonista.

Ela já vem com tudo: animação, câmera, legendas, efeitos sonoros, músicas, stickers e o passo a passo para agendar no YouTube e no TikTok. Só faltam duas coisas, que ela pergunta no primeiro uso:

1. **O canal:** qual é, em que idioma, se é feito para crianças e em que horários postar.
2. **O protagonista:** nome, jeito, visual e voz. Ela mostra uma prévia no Roblox Studio e ajusta até você aprovar.

## O que ela faz

A partir de uma ideia ("faz um de qual escorregador é o mais rápido"):

1. Escreve um roteiro original e confere se a ideia não repete um vídeo seu.
2. Gera a voz no ElevenLabs.
3. Monta e anima a cena no Roblox Studio pela linha de comando, sem cliques, e confere colisões e enquadramento antes de gravar. Grava só a janela do Studio.
4. Edita o Short 1080×1920 com legendas palavra a palavra, efeitos e música, e confere volume, transcrição e quadros.
5. Prepara título, descrição e tags. Agenda no YouTube Studio e, se você quiser, no TikTok, só quando você pedir.

## Antes de instalar

- Windows 10 ou 11.
- [Claude Code](https://claude.com/claude-code).
- Python 3.11 ou mais novo.
- [Roblox Studio](https://create.roblox.com/) instalado e logado.
- Conta no [ElevenLabs](https://elevenlabs.io) para a voz.
- Google Chrome com a extensão Claude in Chrome, se quiser que a skill use o ElevenLabs, o YouTube Studio e o TikTok por você.

## Instalar

```bash
git clone https://github.com/Juliocesar7881/Skill-roblox-sem-personagem.git
```

```bash
cd Skill-roblox-sem-personagem
```

```bash
python install.py
```

O download tem cerca de 330 MB por causa das músicas. O instalador copia as duas pastas do repositório para `~/.claude/skills`.

## Usar

No Claude Code, digite `/roblox-sem-personagem`. Da primeira vez ela faz as perguntas e mostra a prévia do personagem. Depois é só pedir:

- "faz um Short de quem constrói a maior torre"
- "faz 7 vídeos para a semana"
- "agenda esse lote no meu canal"

**Deixe a tela ligada enquanto ela grava:** com o monitor desligado, o Roblox Studio não desenha a cena.

## O que tem aqui

- `roblox-sem-personagem/`: a skill. `SKILL.md` é o fluxo, `references/` tem as regras de produção, as lições de cena e edição, o guia de ideias e o de SEO, `luau/AnimKit.lua` é o kit de animação, `scripts/` tem a produção e `modelos/exemplos/` tem dois Shorts completos para consulta.
- `roblox-video-editor/`: o renderizador, com 127 efeitos, 94 músicas, stickers e fontes.

Sua configuração fica em `config.local.json`, seu histórico em `historico/roteiros.md`, e rodar `install.py` de novo não apaga nenhum dos dois.

## Direitos dos sons e músicas

Leia antes de monetizar. Detalhes em `roblox-video-editor/references/audio-licencas.md` e em [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

- **Músicas de Kevin MacLeod:** CC BY 4.0. Pedem crédito, que a skill já coloca na descrição.
- **Efeitos originais:** feitos para este projeto, uso comercial liberado.
- **Efeitos do CapCut:** liberados só por declaração do dono deste repositório, sem comprovação de licença.
- **38 áudios marcados como não verificados** (memes e músicas pessoais em pastas `fornecidos` e `fornecidas`): a licença não foi comprovada e alguns podem ser de terceiros. A skill não os escolhe para vídeos comerciais. Não use sem conferir os direitos.

O uso comercial das vozes depende do seu plano no ElevenLabs.

## Licença

Código sob licença MIT. Os áudios seguem as licenças descritas acima.
