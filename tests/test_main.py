import os, json, tempfile, subprocess, sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

def run(cmd):
    return subprocess.run([sys.executable] + cmd, cwd=PROJECT_DIR, capture_output=True, text=True)

def test_add_list_remove():
    # ensure clean file
    tf = PROJECT_DIR / "todos.json"
    if tf.exists():
        tf.unlink()
    r = run(["main.py", "add", "Test item", "--tags", "test,cli"])
    assert "Added todo" in r.stdout
    r = run(["main.py", "list", "--all"])
    assert "Test item" in r.stdout
    # remove
    r = run(["main.py", "remove", "1"])
    assert "Removed todo #1" in r.stdout
