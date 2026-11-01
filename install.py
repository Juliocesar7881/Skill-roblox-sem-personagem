"""Instala a skill no Claude Code (Windows, sem precisar de credenciais do GitHub).

    python install.py              # em ~/.claude/skills
    python install.py --project .  # em ./.claude/skills

Copia as duas pastas do repositório: roblox-sem-personagem (a skill) e roblox-video-editor (renderizador, sons,
músicas e stickers). Atualizar não apaga o canal, o protagonista nem o registro de roteiros.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILLS = ('roblox-sem-personagem', 'roblox-video-editor')
MARCA = '.installed-by-skill-roblox-sem-personagem'
MARCAS_ACEITAS = (MARCA, '.installed-by-roblox-video-editor')
DO_USUARIO = {'roteiros.md'}  # o registro de roteiros de quem usa a skill


def ignorar(origem, dest):
    def filtro(pasta, nomes):
        fora = shutil.ignore_patterns('__pycache__', '*.pyc', 'config.local.json', 'personagem_extra.lua')(pasta, nomes)
        destino = dest / Path(pasta).relative_to(origem)
        return fora | {n for n in nomes if n in DO_USUARIO and (destino / n).exists()}
    return filtro


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--project', type=Path, help='Instala neste projeto em vez da pasta de skills do usuário')
    ap.add_argument('--skip-deps', action='store_true', help='Usa os pacotes Python já instalados')
    args = ap.parse_args()
    repo = Path(__file__).resolve().parent
    base = (args.project.resolve() if args.project else Path.home()) / '.claude' / 'skills'
    for nome in SKILLS:
        dest = base / nome
        if dest.exists() and not any((dest / m).exists() for m in MARCAS_ACEITAS):
            raise SystemExit(f'Já existe uma skill fora deste instalador: {dest}. Guarde uma cópia antes de instalar.')
    if not args.skip_deps:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', '-r',
                        str(repo / 'requirements.txt')], check=True)
    for nome in SKILLS:
        dest = base / nome
        shutil.copytree(repo / nome, dest, dirs_exist_ok=True, ignore=ignorar(repo / nome, dest))
        (dest / MARCA).write_text('Instalação portátil; atualizar preserva a configuração local.\n', encoding='utf-8')
    print(f'Skills instaladas em {base}: {", ".join(SKILLS)}')
    if not list((Path(os.environ.get('LOCALAPPDATA', '')) / 'Roblox' / 'Versions').glob('*/RobloxStudioBeta.exe')):
        print('Atenção: Roblox Studio não encontrado. Instale antes de produzir vídeos.')
    print('No Claude Code: /roblox-sem-personagem. No primeiro uso ela pergunta o canal e monta o protagonista com você.')


if __name__ == '__main__':
    main()
