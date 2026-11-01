"""Settings of the skill: config.json + config.local.json (written by configurar.py on the first run).

config.local.json keeps the channel and the protagonist, and installing a new version never touches it."""
import json, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, 'reconfigure'):
        _s.reconfigure(encoding='utf-8', errors='replace')

SKILL = Path(__file__).resolve().parent.parent
LOCAL = SKILL / 'config.local.json'
EXTRA = SKILL / 'personagem_extra.lua'

# Regex of the "Video language" option in YouTube Studio (Portuguese and English UI).
ROTULOS_YOUTUBE = {
    'pt': r'^(Portugu.s \(Brasil\)|Portuguese \(Brazil\))$',
    'en': r'^(Ingl.s|English)$',
    'es': r'^(Espanhol|Spanish|Espa.ol)$',
}


def config():
    c = json.loads((SKILL / 'config.json').read_text(encoding='utf-8'))
    if LOCAL.exists():
        for k, v in json.loads(LOCAL.read_text(encoding='utf-8')).items():
            if isinstance(v, dict) and isinstance(c.get(k), dict):
                c[k] = {**c[k], **v}
            else:
                c[k] = v
    return c


def idioma():
    """Language of the videos (pt, en, es...): `texto`, falas/ and final-<idioma>/ of every project are in it."""
    return config()['idioma'] or 'en'


def personagem():
    return config()['personagem']


def faltando():
    c = config()
    p = c['personagem']
    faltam = []
    if not c['canal']['nome']:
        faltam.append('canal do YouTube')
    if not c['idioma']:
        faltam.append('idioma dos vídeos')
    if c['feito_para_criancas'] is None:
        faltam.append('público do canal (feito para crianças ou não)')
    if not p.get('nome'):
        faltam.append('protagonista')
    elif not (p.get('voz') or {}).get('nome'):
        faltam.append('voz do protagonista')
    return faltam


def exigir_setup():
    faltam = faltando()
    if faltam:
        raise SystemExit('Skill ainda sem configuração: falta ' + ', '.join(faltam) +
                         '. Faça o setup de references/setup.md antes de produzir.')
