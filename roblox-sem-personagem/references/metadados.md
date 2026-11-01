# Título, descrição e tags com SEO (YouTube Shorts)

Escreva no `roteiro.json` de cada vídeo, no idioma do canal. O padrão abaixo veio dos Shorts de Roblox que mais tiveram visualizações em um canal real. Depois que o canal tiver vídeos, confira quais foram melhor no Studio (Conteúdo → Shorts, ordene por visualizações) e siga o que funcionou.

Títulos que seguem o padrão: "QUAL ESCORREGADOR É O MAIS RÁPIDO?", "NÃO PISE NA COR ERRADA NO ROBLOX! 😱🌈", "O CHÃO VIROU LAVA NO ROBLOX!", "APERTEI OS 5 BOTÕES DO ROBLOX… DEU RUIM! 😱".

| Campo | Onde | Regra |
|---|---|---|
| Título | `titulo_youtube` | CAIXA ALTA; a palavra-chave **ROBLOX** no título ("... NO ROBLOX?!", "... DO ROBLOX… DEU RUIM!"); pergunta ou exclamação curiosa ("QUAL...?!", "QUANTOS...?!", "... DEU RUIM!"); 2 emojis; termina com `#shorts #roblox`; até ~70 caracteres antes das hashtags (máximo de 100 no total); sem clickbait falso: o vídeo entrega o que o título promete |
| Descrição | `descricao` | 1ª linha: gancho com as opções ou tentativas e emojis (é o que aparece no feed). 2ª: o que acontece sem contar o final, com "Roblox" e o nome do protagonista escritos. 3ª: pergunta para comentar ("Comenta qual você escolheria! 👇"). 4ª: convite para se inscrever no canal. Sem links |
| Hashtags | `hashtags` | `#Roblox #Shorts`, o nome do protagonista, uma do país ou idioma (`#RobloxBrasil`) e uma do tema (`#CasteloDeAreia`) |
| Tags | `tags` | 15–20: amplas (`roblox`, `roblox shorts`, `roblox brasil`, `roblox engraçado`, `humor roblox`, `animação roblox`, `shorts`, o nome do protagonista) + 6–8 do tema, o que a pessoa digitaria ("castelo de areia", "qual castelo aguenta a onda", "onda gigante") + `desafio roblox`. O script corta em ~480 caracteres |

`python scripts/lote.py metadados LOTE` monta `publicacao.json` e `publicacao.txt` com:

- título, acrescentando `#shorts #roblox` se faltar;
- descrição, hashtags, créditos da música (lidos de `final-<idioma>/…-creditos.txt`, gerados pelo renderizador; a licença CC BY exige o crédito) e crédito da voz;
- tags validadas: sem `<` `>`, sem repetir, dentro do limite;
- público, categoria e idioma da configuração.

O comando sai com erro e lista o que falta se não houver MP4, descrição ou créditos, se faltar "ROBLOX" no título, se houver menos de 12 tags ou se o título passar de 100 caracteres.

A thumbnail não é feita pela skill: o dono do canal coloca depois.
