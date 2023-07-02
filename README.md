# Dotfile Chief

## dotfiles.json

```json5
[{
    "name": "Dotfile Name",
    "src": "path/to/dotfile/in/computer",
    "dest": "path/to/dotfile/relative/to/dotfiles/directory",
    "note": "Some note about this file",  // optional
    "resources": [                        // optional
        "a list of resources related to this file"
    ],
    "ignore": false                       // optional, ignores the dotfile for onboarding and release (default = false)
}]
```

## dotfiles.py

Onboard files from your computer to dotfiles:

```bash
python3 dotfiles.py onboard
```

Release files from dotfiles to your computer:

```bash
python3 dotfiles.py release
```

Find the differences between onboarded dotfiles and those in your computer:

```bash
python3 dotfiles.py diff
```

## Inspiration:

- https://dev.to/awais/comment/1boc8

## Alternative Tools

- [GNU Stow](https://www.gnu.org/software/stow/)
