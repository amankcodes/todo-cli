# Todo CLI — Mini Project
A small, full-featured terminal Todo list application in Python.

## Features
- Add, list, complete, delete, edit todos
- Tagging and filtering by tag / status
- Due dates support (YYYY-MM-DD)
- Persistent storage in `todos.json`
- Simple unit tests
- Easy to run

## Run
Requires Python 3.8+.
```bash
python main.py --help
```

## Examples
```bash
python main.py add "Buy groceries" --tags shopping,errands --due 2025-12-20
python main.py list --all
python main.py done 1
python main.py edit 2 --title "New title"
python main.py remove 3
```
