from typing import Any
from copy import deepcopy

_NOTES:list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "First steps Django Framework",
        "body": "View get request and return response",
        "tag": "Django",
        "category": "backend"
    },
    {
        "id": 2,
        "title": "Introduction to Flask",
        "body": "Create simple route and return JSON",
        "tag": "Flask",
        "category": "backend"
    },
    {
        "id": 3,
        "title": "Working with PostgreSQL",
        "body": "Connect database and execute queries",
        "tag": "Database",
        "category": "backend"
    },
    {
        "id": 4,
        "title": "REST API Basics",
        "body": "Learn CRUD operations in REST",
        "tag": "API",
        "category": "backend"
    },
    {
        "id": 5,
        "title": "Introduction to Docker",
        "body": "Create Dockerfile and run container",
        "tag": "DevOps",
        "category": "infrastructure"
    }
]

_next_id: int = 6

def list_notes()-> list[dict[str, Any]]:
    return deepcopy(_NOTES)


def get_note(note_id: int) -> dict[str, Any]|None:
    for note in _NOTES:
        if note['id'] == note_id:
            return deepcopy(note)
    return None


def create_note(*, title:str, body:str, tag:str, category:str) -> dict[str, Any]:
    global _next_id
    note = {
        "id": _next_id,
        "title": title.strip(),
        "body": body.strip(),
        "tag": tag.strip(),
        "category": category.strip()
    }
    _NOTES.append(note)
    _next_id += 1
    return deepcopy(note)


def update_note(
        note_id: int,
        *,
        title:str,
        body:str,
        tag:str,
        category:str

) -> dict[str, Any] | None:

    for note in _NOTES:
        if note['id'] == note_id:
            note['title'] = title.strip()
            note['body'] = body.strip()
            note['tag'] = tag.strip()
            note['category'] = category.strip()
            return deepcopy(note)
    return None


def delete_note(note_id: int) -> bool:
    global _NOTES
    before = len(_NOTES)
    _NOTES = [n for n in _NOTES if n["id"] != note_id]
    return len(_NOTES) != before