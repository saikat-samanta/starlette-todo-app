from starlette.routing import Route
from .utils import get_all_todos, add_todo, get_todo

routes = [
    Route("/get", get_all_todos, methods=["GET"]),
    Route("/add", add_todo, methods=["POST"]),
    Route("/get/{id}", get_todo, methods=["GET"]),
    # Route("/update/{id}", update_todo, methods=["PATCH"]),
    # Route("/delete/{id}", remove_todo, methods=["DELETE"]),
]
