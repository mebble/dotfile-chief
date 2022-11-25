import json
import os
import shutil
import sys
from pathlib import Path

home_dir = os.environ['HOME']
commands = ['onboard', 'release']
script_path = os.path.dirname(__file__)
dotfiles_json_path = os.path.join(script_path, './dotfiles.json')
dotfiles_dir_path = os.path.join(script_path, './dotfiles')

def touch(path):
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    Path(path).touch()

def onboard(name, src, dest):
    touch(dest)
    try:
        shutil.copy2(src, dest)
        print(f'[DONE] dotfile {name} onboarded to {dest}')
    except FileNotFoundError:
        print(f'[FAIL] dotfile {name} not found at {src}')

def release(name, src, dest):
    touch(src)
    try:
        shutil.copy2(dest, src)
        print(f'[DONE] dotfile {name} released to {src}')
    except FileNotFoundError:
        print(f'[FAIL] dotfile {name} not found at {dest}')

def get_cmd():
    try:
        cmd = sys.argv[1]
    except IndexError:
        return ''
    return cmd

def validate(dotfiles):
    src_set = { file['src'] for file in dotfiles }
    dest_set = { file['dest'] for file in dotfiles }
    if len(src_set) != len(dotfiles):
        return 'There are duplicate "src" fields'
    if len(dest_set) != len(dotfiles):
        return 'There are duplicate "dest" fields'

cmd = get_cmd()
if cmd not in commands:
    print('Usage: python3 dotfiles.py (onboard | release)')
    exit(1)

if cmd == 'onboard':
    operate = onboard
elif cmd == 'release':
    operate = release

with open(dotfiles_json_path) as df:
    dotfiles = json.load(df)

    err = validate(dotfiles)
    if err:
        print(f'[FAIL] dotfiles.json has a problem: {err}')
        exit(1)

    for file in dotfiles:
        name = file['name']

        if file.get('ignore', False):
            print(f'[IGNORE] dotfile {name} is ignored')
            continue

        src = file['src'].replace('~', home_dir)
        dest = os.path.join(dotfiles_dir_path, file['dest'])

        operate(name, src, dest)
