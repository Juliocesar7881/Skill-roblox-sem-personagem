"""First-run setup: the channel and the protagonist of this install (references/setup.md).

  python configurar.py status                     what is set and what is missing (exit 1 if something is missing)
  python configurar.py canal --nome N --id UC... --idioma pt --criancas sim|nao
                             [--handle @x] [--idioma-video "Portuguese (Brazil)"] [--tiktok @x]
                             [--horarios 09:00 18:00] [--videos-por-lote 2] [--fuso America/Sao_Paulo]
  python configurar.py personagem FICHA.json      checks the character sheet and saves it
  python configurar.py previa [--pasta DIR]       renders previa.png in Roblox Studio for the user to approve

Everything goes to config.local.json, next to config.json. A new install keeps that file.
"""
import argparse, json, re, subprocess, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ajustes import EXTRA, LOCAL, ROTULOS_YOUTUBE, SKILL, config, faltando  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CORES = ('pele', 'camisa', 'calca', 'saia', 'tenis', 'sola', 'cabelo', 'acessorio', 'iris', 'sobrancelha', 'labio', 'bochecha')
OPCOES = {'inferior': ('calca', 'bermuda', 'saia'), 'manga': ('curta', 'comprida', 'regata', 'bufante'),
          'cabelo': ('curto', 'comprido', 'rabo', 'espetado', 'afro', 'careca')}
ACESSORIOS = ('laco', 'bone', 'oculos')
SOBRANCELHAS = ('finas', 'grossas')
EXPRESSOES = ('wink', 'happy', 'smile', 'confident', 'surprised', 'dizzy')
IDIOMA_VIDEO = {'pt': 'Portuguese (Brazil)', 'en': 'English', 'es': 'Spanish'}


def salvar(novo):
    atual = json.loads(LOCAL.read_text(encoding='utf-8')) if LOCAL.exists() else {}
    for k, v in novo.items():
        if isinstance(v, dict) and isinstance(atual.get(k), dict) and k != 'personagem':
            atual[k] = {**atual[k], **v}
        else:
            atual[k] = v
    LOCAL.write_text(json.dumps(atual, ensure_ascii=False, indent=1), encoding='utf-8')


def cmd_status(a):
    c = config()
    canal, p = c['canal'], c['personagem']
    print(f'Canal: {canal["nome"] or "-"} {canal["id"]} {canal["handle"]}'.rstrip())
    print(f'Idioma: {c["idioma"] or "-"} | feito para crianças: {c["feito_para_criancas"]} | '
          f'{c["videos_por_lote"]} vídeos por lote, {" e ".join(c["horarios"])} ({c["fuso"]})')
    print(f'TikTok: {c["tiktok"]["handle"] or "não usa"}')
    print(f'Protagonista: {p.get("nome", "-")}, voz {(p.get("voz") or {}).get("nome", "-")}, '
          f'peças extras: {"sim" if EXTRA.exists() else "não"}')
    faltam = faltando()
    if faltam:
        print('FALTA:', ', '.join(faltam))
        sys.exit(1)
    print('Setup completo.')


def cmd_canal(a):
    idioma = a.idioma.lower()
    video = a.idioma_video or IDIOMA_VIDEO.get(idioma)
    if not video:
        raise SystemExit(f'idioma {idioma}: informe --idioma-video com o nome da língua no YouTube')
    if a.id and not re.fullmatch(r'UC[\w-]{22}', a.id):
        raise SystemExit(f'--id {a.id}: o ID do canal começa com UC e tem 24 caracteres (está na URL do Studio)')
    for h in a.horarios or []:
        if not re.fullmatch(r'\d\d:\d\d', h):
            raise SystemExit(f'horário {h}: use HH:MM')
    novo = {'idioma': idioma, 'feito_para_criancas': a.criancas == 'sim',
            'canal': {'nome': a.nome, 'id': a.id or '', 'handle': a.handle or '', 'idioma_video': video}}
    if a.tiktok is not None:
        novo['tiktok'] = {'handle': a.tiktok}
    if a.horarios:
        novo['horarios'] = sorted(a.horarios)
    if a.videos_por_lote:
        novo['videos_por_lote'] = a.videos_por_lote
    if a.fuso:
        novo['fuso'] = a.fuso
    salvar(novo)
    print(f'Canal salvo em {LOCAL.name}.')


def slug(nome):
    s = unicodedata.normalize('NFKD', nome)
    return re.sub(r'[^a-z0-9]+', '', ''.join(ch for ch in s if not unicodedata.combining(ch)).lower())


def checar_ficha(f):
    erros = []
    if not str(f.get('nome') or '').strip():
        erros.append('falta "nome"')
    if not str(f.get('personalidade') or '').strip():
        erros.append('falta "personalidade" (uma frase: como ele fala e age nos vídeos)')
    voz = f.get('voz') or {}
    if not voz.get('nome'):
        erros.append('falta "voz": {"nome": ...} (voz grátis de Minhas vozes no ElevenLabs)')
    for k, ops in OPCOES.items():
        if f.get(k, ops[0]) not in ops:
            erros.append(f'"{k}" deve ser um de: {", ".join(ops)}')
    for k, v in (f.get('cores') or {}).items():
        if k not in CORES:
            erros.append(f'cor desconhecida "{k}" (use: {", ".join(CORES)})')
        elif not re.fullmatch(r'#[0-9A-Fa-f]{6}', str(v)):
            erros.append(f'cor "{k}": use #RRGGBB')
    for k in ('pele', 'camisa', 'cabelo', 'iris'):
        if k not in (f.get('cores') or {}) and not (k == 'cabelo' and f.get('cabelo') == 'careca'):
            erros.append(f'falta a cor "{k}"')
    for x in f.get('acessorios') or []:
        if x not in ACESSORIOS:
            erros.append(f'acessório "{x}" não existe no kit (use {", ".join(ACESSORIOS)} ou personagem_extra.lua)')
    rosto = f.get('rosto') or {}
    if rosto.get('sobrancelhas', 'finas') not in SOBRANCELHAS:
        erros.append(f'"rosto.sobrancelhas" deve ser um de: {", ".join(SOBRANCELHAS)}')
    if f.get('assinatura', 'wink') not in EXPRESSOES:
        erros.append(f'"assinatura" deve ser um de: {", ".join(EXPRESSOES)}')
    return erros


def cmd_personagem(a):
    f = json.loads(a.ficha.read_text(encoding='utf-8'))
    erros = checar_ficha(f)
    if erros:
        raise SystemExit('Ficha com problema:\n  ' + '\n  '.join(erros))
    f['id'] = slug(f['nome'])
    f.setdefault('inferior', 'calca')
    f.setdefault('manga', 'curta')
    f.setdefault('cabelo', 'curto')
    f.setdefault('acessorios', [])
    f.setdefault('assinatura', 'wink')
    f.setdefault('rosto', {'cilios': False, 'sobrancelhas': 'finas'})
    salvar({'personagem': f})
    print(f'Protagonista {f["nome"]} salvo (id "{f["id"]}" nos roteiros, voz {f["voz"]["nome"]}).')
    print('Próximo passo: python configurar.py previa')


CENARIO = '''local RS = game:GetService("ReplicatedStorage")
local K = require(RS:WaitForChild("AnimKit"):Clone())
local V = Vector3.new
for _, o in ipairs(workspace:GetChildren()) do
	if o:GetAttribute("DoLote") or o.Name == "Protagonista" then o:Destroy() end
end
K.visual()
local chao = K.bloco({ Name = "Chao", Size = V(120, 2, 120), CFrame = CFrame.new(0, -1, 0), Color = Color3.fromRGB(120, 200, 120) })
chao:SetAttribute("DoLote", true)
K.piso(chao)
K.criarProtagonista("Protagonista", K.emPe(V(0, 0, 0), V(0, 0, -10)))
print("cenario ok")
'''

CENA = '''local RS = game:GetService("ReplicatedStorage")
local K = require(RS:WaitForChild("AnimKit"))
local noob = workspace:WaitForChild("Protagonista")
local raiz = noob:WaitForChild("HumanoidRootPart")
local cam = K.camera
local V = Vector3.new
local C0 = raiz.CFrame
K.preCarregar(noob)
K.foco(noob.Head)
local function olhando(graus)
	raiz.CFrame = C0 * CFrame.Angles(0, math.rad(graus), 0)
end
local ev = {}
local function E(t, f) ev[#ev + 1] = { t = t, f = f } end
E(0, function() K.anim(noob, "idle", { loop = true }) K.rosto(noob, "normal", 0.01) cam.corte(V(0, 5.6, -13), V(0, 3.4, 0), 42) end)
E(1.5, function() cam.corte(V(-7.5, 5.2, -10.5), V(0, 3.4, 0), 42) olhando(0) end)
E(3, function() cam.rosto(noob, 3.6, 42) K.rosto(noob, "feliz", 0.01) end)
E(4.5, function() K.rosto(noob, "surpreso", 0.01) end)
E(6, function() K.rosto(noob, "medo", 0.01) end)
E(7.5, function() K.rosto(noob, "piscadinha", 0.01) end)
K.rodar(ev, 9)
'''

QUADROS = (0.9, 2.3, 3.8, 5.3, 6.8, 8.3)


def cmd_previa(a):
    exe = sys.executable
    rs = str(SKILL / 'scripts' / 'studio_runscript.py')
    pasta = (a.pasta or Path.home() / 'Documents' / 'entregas' / 'roblox-sem-personagem' / 'previa').resolve()
    st = pasta / 'studio'
    st.mkdir(parents=True, exist_ok=True)
    (st / 'cenario.lua').write_text(CENARIO, encoding='utf-8')
    (st / 'cena.lua').write_text(CENA, encoding='utf-8')
    (st / 'base.rbxlx').write_bytes((SKILL / 'assets' / 'base.rbxlx').read_bytes())
    subprocess.run([exe, rs, 'montar', '--kit', '--cenario', 'studio/cenario.lua', '--cena', 'studio/cena.lua', '--play',
                    '--saida', 'studio/pipeline.lua'], cwd=pasta, check=True, capture_output=True)
    subprocess.run([exe, rs, 'rodar', 'studio/pipeline.lua', '--place', 'studio/base.rbxlx', '--gravar', 'studio/viewport.mp4',
                    '--frente'], cwd=pasta, check=True, capture_output=True, timeout=300)
    import captura_janela
    from media_utils import ffmpeg
    captura_janela.processar(str(st / 'viewport.mp4'), str(pasta / 'previa.mp4'), 0.8, 9.0)
    nomes = []
    for i, t in enumerate(QUADROS):
        nome = pasta / f'quadro-{i}.png'
        subprocess.run([ffmpeg(), '-v', 'error', '-y', '-ss', str(t), '-i', str(pasta / 'previa.mp4'), '-frames:v', '1',
                        '-vf', 'scale=360:-2', str(nome)], check=True)
        nomes.append(nome)
    from PIL import Image
    fotos = [Image.open(n) for n in nomes]
    w, h = fotos[0].size
    folha = Image.new('RGB', (w * len(fotos), h))
    for i, f in enumerate(fotos):
        folha.paste(f, (i * w, 0))
    folha.save(pasta / 'previa.png')
    for f, n in zip(fotos, nomes):
        f.close()
        n.unlink()
    print(pasta / 'previa.png')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('status')
    s = sub.add_parser('canal')
    s.add_argument('--nome', required=True); s.add_argument('--id'); s.add_argument('--handle')
    s.add_argument('--idioma', required=True); s.add_argument('--idioma-video')
    s.add_argument('--criancas', required=True, choices=['sim', 'nao'])
    s.add_argument('--tiktok'); s.add_argument('--horarios', nargs='+'); s.add_argument('--videos-por-lote', type=int)
    s.add_argument('--fuso')
    s = sub.add_parser('personagem'); s.add_argument('ficha', type=Path)
    s = sub.add_parser('previa'); s.add_argument('--pasta', type=Path)
    a = ap.parse_args()
    globals()['cmd_' + a.cmd](a)


if __name__ == '__main__':
    main()
