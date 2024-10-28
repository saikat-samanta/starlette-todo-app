from starlette.requests import Request
from starlette.responses import JSONResponse
from utils import check_password, hash_password, jwt_encode

from database import DB


def register(request: Request):
    if not request["body"]:
        return JSONResponse({"message": "empty body"}, status_code=400)
    if not request["body"].get("username"):
        return JSONResponse({"message": "username is required"}, status_code=400)
    if not request["body"].get("password"):
        return JSONResponse({"message": "password is required"}, status_code=400)

    user_data = DB.user_client.getByQuery({"username": request["body"]["username"]})
    if user_data:
        return JSONResponse({"message": "user already exists"}, status_code=409)

    hashed_password = hash_password(request["body"]["password"])
    DB.user_client.add(
        {
            "username": request["body"]["username"],
            "password": hashed_password,
        }
    )
    return JSONResponse({"message": "register"})


def login(request: Request):
    if not request["body"]:
        return JSONResponse({"message": "empty body"}, status_code=400)
    if not request["body"].get("username"):
        return JSONResponse({"message": "username is required"}, status_code=400)
    if not request["body"].get("password"):
        return JSONResponse({"message": "password is required"}, status_code=400)

    user_data = DB.user_client.getByQuery({"username": request["body"]["username"]})
    if not user_data:
        return JSONResponse({"message": "user not found"}, status_code=404)

    is_valid = check_password(request["body"]["password"], user_data[0]["password"])
    if not is_valid:
        return JSONResponse(
            {"message": "invalid username or password"}, status_code=401
        )

    user_details = user_data[0].copy()
    del user_details["password"]

    token = jwt_encode(user_details)
    return JSONResponse(
        {
            "message": "user logged in",
            "token": token,
            "username": user_details["username"],
        }
    )


def user(request: Request):
    return JSONResponse({"user": request["user"]})
