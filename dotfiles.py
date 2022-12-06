import json
import os
import shutil
import sys
from pathlib import Path
from difflib import unified_diff

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

def diff(name, src, dest):
    with open(dest) as d:
        with open(src) as s:
            d_lines = d.readlines()
            s_lines = s.readlines()

            print(f'[INFO] Diffing dotfile {name}:')
            for diff in unified_diff(d_lines, s_lines, fromfile='dest (onboarded to dotfiles)', tofile='src (in your computer)'):
                print(diff)

def get_cmd():
    try:
        cmd = sys.argv[1]
    except IndexError:
        return ''
    return cmd

command_map = {
    'onboard': onboard,
    'release': release,
    'diff': diff,
}

def get_operation():
    cmd = get_cmd()
    operation = command_map.get(cmd)

    return operation

def validate(dotfiles):
    src_set = { file['src'] for file in dotfiles }
    dest_set = { file['dest'] for file in dotfiles }
    if len(src_set) != len(dotfiles):
        return 'There are duplicate "src" fields'
    if len(dest_set) != len(dotfiles):
        return 'There are duplicate "dest" fields'

if __name__ == '__main__':
    operate = get_operation()
    if operate is None:
        print(f'Usage: python3 dotfiles.py ({" | ".join(command_map.keys())})')
        exit(1)

    home_dir = os.environ['HOME']
    script_path = os.path.dirname(__file__)
    dotfiles_json_path = os.path.join(script_path, './dotfiles.json')
    dotfiles_dir_path = os.path.join(script_path, './dotfiles')

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
