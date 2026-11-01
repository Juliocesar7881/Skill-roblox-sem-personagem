# AnimKit — quick reference

`ReplicatedStorage.AnimKit` (ModuleScript; source in `luau/AnimKit.lua`, installed by `studio_runscript.py montar --kit`). Function names are kept from the original kit (some are Portuguese); the English aliases below work everywhere.

## Constants

| Name | Default | Use |
|---|---|---|
| `K.VERTICAL` | `true` | Camera rolled 90°: the 9:16 frame uses the whole viewport; `captura_janela.processar` turns it back. |
| `K.FOV` | 50 | **Horizontal** field of view of the final vertical video. |
| `K.CABECA` | 1.0 | R15 `HeadScale` (standard proportions). |
| `K.PERSONAGEM` | sheet of `configurar.py` | The protagonist's sheet (`inferior`, `manga`, `cabelo`, `acessorios`, `rosto`, `cores`...). `studio_runscript.py montar --kit` writes it into the kit. |
| `K.CORES` | colors of the sheet | `pele`, `camisa` (top), `calca` (pants/shorts), `saia`, `tenis`, `sola`, `cabelo`, `acessorio`, `iris`, `sobrancelha`, `labio`, `bochecha`. |
| `K.ALTURA_RAIZ` / `ALTURA_SENTADO` / `ALTURA_DEITADO` | 3.41 / 1.32 / 0.95 | Measured R15 heights of the HumanoidRootPart above the floor (idle), the seat (sitting) and the floor (lying). |
| `K.ATRASO` | 0.8 | Seconds between the magenta flash and timeline t=0. |
| `K.MARCAS` | 5 | Seconds between sync marks (magenta strip at the top of the viewport, cropped by the recording). |
| `K.ROSTO_TAM` / `ROSTO_LUZ` / `ROSTO_FAIXA` | 1.0 / 0.6 / {0.06, 0.97} | Face plate size, how much scene light affects the drawing, and the drawn vertical band (used by the camera audit). |
| `K.MARGEM_TOPO` | 0.075 | Top strip of the viewport cropped by the recording. |
| `K.FAIXA_LEGENDA` | {0.665, 0.75} | Video band used by the karaoke caption; their face must stay out of it. |

## Building (edit mode, in `cenario.lua`)

| Function | Use |
|---|---|
| `K.visual()` | Saturated colors, bloom, atmosphere, background blur; turns off `CharacterAutoLoads`. |
| `K.bloco{Size=, CFrame=, Color=, Material=, Name=, Parent=}` | Smooth anchored part. |
| `K.piso(part)` | Marks the part as floor (attribute `Piso`). **Mark every floor and platform anyone stands on.** |
| `K.chao(pos)` | Height of the marked floor at (x, z). |
| `K.emPe(pos, lookAt)` | CFrame standing exactly on the floor (y of `pos` is ignored). |
| `K.deitado(pos, headDir)` | Lying on the back on the floor, face up. |
| `K.criarProtagonista("Protagonista", CFrame, colors)` | The protagonist of the sheet: R15 standard proportions, cartoon face plate (big eyes with colored iris and two highlights, brows, blush, sweat drop), and the hair, clothes and accessories of the sheet. Soft parts (`enfeite`) are welded to the body. Always name the model `"Protagonista"` (the base `comum.py` waits for it). `colors` overrides sheet colors for a costume change. `K.criarNoob` and `K.criarGarota` are aliases. |
| `K.enfeite(name, part, size, color, relativeCFrame, shape)` | A soft welded part with no collision (`personagem_extra.lua` uses it). `shape`: `"bola"` or nil for a block. |
| `K.escorregador(name, {topo=, dir=, comprimento=, queda=, cor=, corBorda=, largura=, segmentos=, curva=})` | Stairs, platform, straight or spiral slide and rails; stores the **seat points** in `Caminho`. |

## Acting (play mode, in `cena.lua`)

| Function | Use |
|---|---|
| `K.rosto(noob, expr, t)` | Expressions: `normal` (small smile), `happy`, `smile`, `surprised`, `scared` (+ sweat), `scream` (+ sweat), `nervous`, `confident`, `angry`, `doubt`, `dizzy`, `squint` (>_<), `knockout` (X eyes) and `wink` (one eye closed "^" with an open smile). Portuguese names (`feliz`, `sorrindo`, `surpreso`, `medo`, `grito`, `piscadinha`…) also work. One controller per frame merges expression, blink, gaze and speech. |
| `K.olhar(noob, dx, dy, t)` | Iris direction, −1 to 1. |
| `K.piscar(noob)` | Automatic blinks (the eye squashes and returns in 0.16 s; the lashes follow). |
| `K.anim(noob, name, {loop=, velocidade=, fade=, manter=})` | Cartoony (`idle`, `idle2`, `walk`, `run`, `jump`, `fall`, `climb`, `swim`), Levitation (`float`, `flyPose`, `superJump`) and R15 emotes (`sit`, `wave`, `point`, `laugh`, `cheer`, `dance`). Portuguese names also work. Call `K.preCarregar(noob)` before the scene. |
| `K.falar(noob, envelope, fps)` | Lip sync from the real voice volume (`scripts/envelope_boca.py`): closed mouth + 3 open ovals with tongue, each held ≥ 60 ms; brows lift on emphasis. |
| `K.bracos(noob, pose, t)` | Arm poses (`segurarFrente` hold in front, `segurarAcima` hold above, `arremesso` throw, `esticarCima` reach up, or your own table). |
| `K.pose(noob, name)` | Fixed pose on top of the animation (`sentadoReto` sit straight, `bracosPraCima` arms up, or your own table); `nil` clears it. |
| `K.sentarEm(noob, point, front)` | Sit at a seat point with the sit pose already in place (use before `K.deslizar`). |
| `K.sixSeven(noob, side, t)` | Hand gesture with the arms. |
| `K.mover(noob, Vector3, t, anim)` | Walk/run to the target with feet on the floor. |
| `K.deslizar(noob, K.caminho(model), t, anim, onEnd)` | Slide down sitting, tilted with the ramp, clock-driven (ends exactly at `t`). |
| `K.voar(noob, target, height, t, turns, anim, onLand)` | Arc with side rolls (the face keeps facing the front camera); with a `CFrame` target (`K.deitado`) it ends in the landing pose. On landing switch to `idle` and cut with `K.cortarPara`. |
| `K.tremer(noob, t, amp)` / `K.poeira(pos, n)` | Shake and a dust puff. |
| `K.camera.rosto(noob, dist, fovH, {lado=, altura=, queixo=, t=})` | Close-up from the real head: head in the upper third. `t` makes it a dolly. For objects held in front of them, use a telephoto (larger `dist`, smaller `fovH`). |
| `K.camera.corte(pos, target, fovH, up)` / `K.camera.mover(pos, target, t, fovH, style, up)` | Cut and dolly; `up` sets the frame's up vector (e.g. `V(0,0,1)` to film their lying from above). |
| `K.camera.seguir(part, offset, t, aim)` | Follow keeping the offset; following `noob.Head` use `aim = V(0, -1.5, 0)`. |
| `K.camera.tremor(i, t)` / `K.camera.soco(i, t)` | Camera shake and punch-zoom. |
| `K.cortarPara(noob, cf, anim, camera, {pose=})` | Cut with teleport and no frame of their "old pose in the new place". Use it on every cut that moves them. |
| `K.foco(part)` | Background-blur focus follows the part every frame. |
| `K.rodar(events, duration)` | Hides the UI, prepares the first frame (events with t ≤ 0), magenta flash, fires the events, final flash and `K.encerrar()`. |

Events with t ≤ 0 only prepare the first frame; movement starts at t ≥ 0.05.

## Skirt

Only when the sheet says `"inferior": "saia"`. The skirt is 18 pleat panels welded to `LowerTorso` with adjustable welds. In play mode `AnimKit` updates them every frame:
- each pleat opens just enough to keep every leg corner inside it, plus 0.1 stud;
- it opens instantly and falls back with a 0.12 s ease;
- neighbouring pleats differ by at most ~13°.

The parameters live in model attributes (`SaiaRx`, `SaiaRz`, `SaiaTopo`, `SaiaAlt`, `SaiaAbre`, `SaiaLarg`).

## Audits (mandatory before recording)

| Function | Use |
|---|---|
| `K.auditar(noob)` | Collisions: body parts inside the floor/objects, with time and part (`[auditoria]`). Soft parts (`Visual`: hair, accessories, sleeves, sneakers, skirt) are skipped. |
| `K.auditarCamera(noob, min)` | Camera rule no. 1 measured on the final 9:16 frame (`[camera]`): face too small, back to camera, profile (> 0.5 s), off frame, cut at the edge (> 0.2 s) or in the caption band (> 0.3 s). |
| `K.inserto(true/false)` | Marks shots without the protagonist (showing the options). |
