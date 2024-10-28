from starlette.requests import Request
from starlette.responses import JSONResponse
from database import DB
import datetime


def get_all_todos(request: Request):
    todos = DB.todo_client.reSearch(key="user_id", _re=request["user"]["id"])
    return JSONResponse(todos)


def add_todo(request: Request):
    if not request["body"]:
        return JSONResponse({"message": "empty body"}, status_code=400)
    if not request["body"].get("name"):
        return JSONResponse({"message": "Name is missing"}, status_code=400)

    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    _id = DB.todo_client.add(
        {
            **request["body"],
            **{
                "created_at": created_at,
                "updated_at": created_at,
                "completed": False,
                "user_id": request["user"]["id"],
            },
        }
    )

    return JSONResponse({"message": "todo added", "id": _id})


def get_todo(request: Request):
    todo = None
    try:
        todo = DB.todo_client.getById(request["path_params"]["id"])
        if todo["user_id"] != request["user"]["id"]:
            todo = None
    except Exception:
        return JSONResponse({"message": "todo not found"}, status_code=404)
    if not todo:
        return JSONResponse({"message": "todo not found"}, status_code=404)
    return JSONResponse(todo)
