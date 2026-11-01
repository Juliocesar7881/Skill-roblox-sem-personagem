# Setup do primeiro uso

Faça isto uma vez, conversando com o usuário. Pergunte em blocos curtos, na língua dele, e só o que `configurar.py status` disser que falta. Quando ele não souber responder, sugira uma opção e deixe a decisão com ele.

## 1. O canal

Pergunte:

1. Nome do canal no YouTube e o ID, que começa com `UC` e aparece na URL do YouTube Studio. Se ainda não tiver canal, siga sem o ID e peça antes de postar.
2. Em que idioma serão os vídeos (`pt`, `en`, `es` ou outro).
3. O canal é feito para crianças? Isso muda o que o YouTube permite, então a resposta é do dono do canal.
4. Quantos vídeos por dia e em que horários. Padrão: dois, às 09:00 e 18:00.
5. Fuso horário. Padrão: `America/Sao_Paulo`.
6. Vai postar também no TikTok? Se sim, qual o perfil.

```bash
python scripts/configurar.py canal --nome "NOME" --id UCxxxx --handle @canal --idioma pt --criancas sim --horarios 09:00 18:00 --videos-por-lote 2 --tiktok @perfil
```

Para outro idioma além de `pt`, `en` e `es`, informe `--idioma-video` com o nome da língua no YouTube e acrescente as listas de palavras em `scripts/legendas.py`.

## 2. O protagonista

Pergunte:

1. Nome.
2. Como ele é e como age: criança, adulto, robô, bicho, herói. Peça uma frase de personalidade.
3. Visual: pele, cabelo, olhos, roupa, acessórios. Aceite descrição livre ou imagem de referência e traduza para a ficha.
4. A expressão de assinatura, que fecha os vídeos.
5. A voz. Mostre as vozes grátis em **Voices → My Voices** do ElevenLabs e deixe o usuário ouvir e escolher. Duas já usadas em canais reais: **Roger** (masculina, ID `CwhRBWXzGAHq8TQ4Fs17`) e **Jessica** (feminina, ID `cgSgspJ2msm6clMCkdW9`). Confira o ID, não só o nome: existe outra voz chamada Roger, e as cópias da aba Explorar podem pedir plano pago. Em português do Brasil, coloque `"sotaque": "[Brazilian Portuguese accent]"`.

Escreva a ficha num arquivo JSON:

```json
{
  "nome": "Téo",
  "personalidade": "Menino animado e curioso que se mete em confusão e ri de si mesmo.",
  "voz": {"nome": "Roger", "sotaque": "[Brazilian Portuguese accent]"},
  "inferior": "bermuda",
  "manga": "curta",
  "cabelo": "curto",
  "acessorios": ["bone"],
  "assinatura": "confident",
  "rosto": {"cilios": false, "sobrancelhas": "grossas"},
  "cores": {
    "pele": "#8D5A3B", "camisa": "#FF8A1F", "calca": "#2A5BD7", "cabelo": "#1E1410", "iris": "#3A2414",
    "acessorio": "#E5322D", "sobrancelha": "#1E1410", "tenis": "#FFFFFF", "sola": "#E5322D"
  }
}
```

```bash
python scripts/configurar.py personagem ficha.json
```

| Campo | Opções |
|---|---|
| `inferior` | `calca`, `bermuda`, `saia` (a saia abre com as pernas) |
| `manga` | `curta`, `comprida`, `regata`, `bufante` |
| `cabelo` | `curto`, `comprido`, `rabo`, `espetado`, `afro`, `careca` |
| `acessorios` | `laco`, `bone`, `oculos` (com `bone`, o `espetado` vira `curto`) |
| `assinatura` | `wink`, `happy`, `smile`, `confident`, `surprised`, `dizzy` |
| `rosto.cilios` | `true`, `false` |
| `rosto.sobrancelhas` | `finas`, `grossas` |
| `cores` | `pele`, `camisa`, `calca`, `saia`, `tenis`, `sola`, `cabelo`, `acessorio`, `iris`, `sobrancelha`, `labio`, `bochecha`, em `#RRGGBB`. Obrigatórias: `pele`, `camisa`, `iris` e `cabelo` (menos em `careca`) |

### Peças que a ficha não cobre

Antena, chifres, orelhas de bicho, capa, rabo: crie `personagem_extra.lua` na pasta da skill, ao lado do `config.json`. O código roda no fim da montagem do personagem e vê `model`, `head`, `hx`, `hy`, `hz`, `enfeite`, `cor`, `C` (`CFrame.new`) e `A` (ângulos em graus):

```lua
-- enfeite(nome, parte, tamanho, cor, posição relativa, forma), forma "bola" ou nil para bloco
enfeite("Antena", head, Vector3.new(0.12, hy * 0.6, 0.12), Color3.fromRGB(60, 60, 70), C(0, hy * 0.75, 0))
enfeite("AntenaBola", head, Vector3.new(0.32, 0.32, 0.32), Color3.fromRGB(255, 60, 60), C(0, hy * 1.08, 0), "bola")
```

As peças ficam soldadas ao corpo, sem colisão, e a auditoria as ignora. Para mudar a forma do corpo ou do rosto além disso, ajuste `luau/AnimKit.lua`. Um novo `install.py` substitui esse arquivo, mas mantém `personagem_extra.lua` e `config.local.json`.

## 3. Prévia

Com a tela ligada e o Roblox Studio instalado:

```bash
python scripts/configurar.py previa
```

Sai `previa.png` com seis quadros: corpo inteiro de frente, de lado e quatro expressões em close. Mostre a imagem ao usuário e ajuste a ficha até ele aprovar. Cada rodada leva menos de um minuto e não gasta crédito.

## 4. Fim

Rode `python scripts/configurar.py status`. Com `Setup completo.`, siga o pedido do usuário pelo fluxo do `SKILL.md`.

Para trocar o canal ou o protagonista depois, rode de novo o comando da parte que muda. O registro de roteiros continua valendo.
