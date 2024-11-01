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


def update_todo(request: Request):
    if not request["body"]:
        return JSONResponse({"message": "empty body"}, status_code=400)
    todo_id = request["path_params"]["id"]
    if not todo_id:
        return JSONResponse({"message": "Bad request"}, status_code=404)
    todo = None
    try:
        todo = DB.todo_client.getById(todo_id)
    except Exception:
        return JSONResponse({"message": "todo not found"}, status_code=404)

    if not todo:
        return JSONResponse({"message": "Todo not found"}, status_code=404)
    try:
        updated_data = {**todo, **request["body"]}
        DB.todo_client.updateById(todo_id, updated_data)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

    return JSONResponse(updated_data)


def delete_todo(request: Request):
    todo_id = request["path_params"]["id"]
    if not todo_id:
        return JSONResponse({"message": "Bad request"}, status_code=404)

    is_deleted = False
    try:
        is_deleted = DB.todo_client.deleteById(todo_id)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=404)

    if not is_deleted:
        return JSONResponse({"message": "Unable to delete item"}, status_code=404)

    return JSONResponse({"message": "Item deleted", "id": todo_id})
