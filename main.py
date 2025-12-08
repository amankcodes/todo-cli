#!/usr/bin/env python3
"""
Todo CLI - main script
Usage: python main.py <command> [options]
Commands: add, list, done, remove, edit, clear, stats
"""

import argparse
import json
import os
import sys
from datetime import datetime
from dateutil import parser as dateparser
from typing import List

DATA_FILE = os.path.join(os.path.dirname(__file__), "todos.json")


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)


def add_todo(title: str, tags: List[str] = None, due: str = None):
    todos = load_todos()
    todo = {
        "id": (max([t["id"] for t in todos]) + 1) if todos else 1,
        "title": title,
        "done": False,
        "tags": tags or [],
        "created_at": datetime.utcnow().isoformat(),
        "due": None,
    }
    if due:
        try:
            todo["due"] = dateparser.parse(due).date().isoformat()
        except Exception:
            print("Warning: could not parse due date, ignoring.")
    todos.append(todo)
    save_todos(todos)
    print(f"Added todo #{todo['id']}: {todo['title']}")


def list_todos(show_all=False, tag=None, pending=False, due_before=None):
    todos = load_todos()
    if not show_all:
        todos = [t for t in todos if not t["done"]]
    if tag:
        todos = [t for t in todos if tag in t.get("tags", [])]
    if pending:
        todos = [t for t in todos if not t["done"]]
    if due_before:
        try:
            db = dateparser.parse(due_before).date()
            todos = [
                t
                for t in todos
                if t.get("due") and dateparser.parse(t["due"]).date() <= db
            ]
        except Exception:
            pass
    if not todos:
        print("No todos found.")
        return
    print(f"{'ID':<4} {'Done':<6} {'Due':<12} {'Tags':<20} Title")
    print("-" * 70)
    for t in todos:
        due = t.get("due") or "-"
        tags = ",".join(t.get("tags", [])) or "-"
        done = "Yes" if t.get("done") else "No"
        print(f"{t['id']:<4} {done:<6} {due:<12} {tags:<20} {t['title']}")


def mark_done(todo_id: int):
    todos = load_todos()
    for t in todos:
        if t["id"] == todo_id:
            if t["done"]:
                print(f"Todo #{todo_id} is already done.")
            else:
                t["done"] = True
                save_todos(todos)
                print(f"Marked todo #{todo_id} as done.")
            return
    print(f"Todo #{todo_id} not found.")


def remove_todo(todo_id: int):
    todos = load_todos()
    new = [t for t in todos if t["id"] != todo_id]
    if len(new) == len(todos):
        print(f"Todo #{todo_id} not found.")
    else:
        save_todos(new)
        print(f"Removed todo #{todo_id}.")


def edit_todo(todo_id: int, title=None, tags=None, due=None):
    todos = load_todos()
    for t in todos:
        if t["id"] == todo_id:
            if title:
                t["title"] = title
            if tags is not None:
                t["tags"] = tags
            if due is not None:
                try:
                    t["due"] = dateparser.parse(due).date().isoformat()
                except Exception:
                    print("Warning: could not parse due date, ignoring.")
            save_todos(todos)
            print(f"Edited todo #{todo_id}.")
            return
    print(f"Todo #{todo_id} not found.")


def clear_done():
    todos = load_todos()
    new = [t for t in todos if not t["done"]]
    save_todos(new)
    print(f"Cleared done todos. ({len(todos)-len(new)} removed)")


def stats():
    todos = load_todos()
    total = len(todos)
    done = sum(1 for t in todos if t["done"])
    pending = total - done
    print(f"Total: {total} | Done: {done} | Pending: {pending}")


def parse_args():
    p = argparse.ArgumentParser(prog="todo", description="Simple Todo CLI")
    sp = p.add_subparsers(dest="cmd")
    # add
    a = sp.add_parser("add", help="Add a todo")
    a.add_argument("title", type=str, help="Title in quotes")
    a.add_argument("--tags", type=str, help="Comma separated tags", default="")
    a.add_argument("--due", type=str, help="Due date YYYY-MM-DD", default=None)
    # list
    l = sp.add_parser("list", help="List todos")
    l.add_argument("--all", action="store_true", dest="all", help="Show all todos")
    l.add_argument("--tag", type=str, help="Filter by tag", default=None)
    l.add_argument("--pending", action="store_true", help="Show only pending", default=False)
    l.add_argument("--due-before", type=str, help="Show todos due before date", default=None)
    # done
    d = sp.add_parser("done", help="Mark todo done")
    d.add_argument("id", type=int)
    # remove
    r = sp.add_parser("remove", help="Remove todo by id")
    r.add_argument("id", type=int)
    # edit
    e = sp.add_parser("edit", help="Edit todo")
    e.add_argument("id", type=int)
    e.add_argument("--title", type=str, default=None)
    e.add_argument("--tags", type=str, default=None)
    e.add_argument("--due", type=str, default=None)
    # clear
    c = sp.add_parser("clear", help="Clear done todos")
    # stats
    s = sp.add_parser("stats", help="Show stats")
    return p.parse_args()


def main():
    args = parse_args()
    if args.cmd == "add":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        tags = [t for t in tags if t]
        add_todo(args.title, tags=tags, due=args.due)
    elif args.cmd == "list":
        list_todos(show_all=args.all, tag=args.tag, pending=args.pending, due_before=args.due_before)
    elif args.cmd == "done":
        mark_done(args.id)
    elif args.cmd == "remove":
        remove_todo(args.id)
    elif args.cmd == "edit":
        tags = None
        if args.tags is not None:
            tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        edit_todo(args.id, title=args.title, tags=tags, due=args.due)
    elif args.cmd == "clear":
        clear_done()
    elif args.cmd == "stats":
        stats()
    else:
        print("No command provided. Use --help to see commands.")


if __name__ == "__main__":
    main()