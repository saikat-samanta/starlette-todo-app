from typing import Sequence

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import BaseRoute, Route, Mount, Router, Host
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

import settings
from database import DB
from middlewares import AuthMiddleware, RequestParserMiddleware
from app import auth, todo


def index(_request: Request):
    return PlainTextResponse("Server is up and running")


static_app = StaticFiles(directory="static")
api_routes = [
    Route("/", index, methods=["GET"]),
    Mount("/auth", routes=auth.routes, name="auth"),
    Mount(
        "/todo",
        routes=todo.routes,
        name="todo",
        middleware=[Middleware(AuthMiddleware)],
    ),
    Mount("/static", app=static_app, name="static"),
]
api = Router(routes=api_routes)

front_end = Router(
    routes=[
        Mount(
            "/",
            app=StaticFiles(directory="./../frontend/build", html=True),
            name="frontend",
        ),
    ]
)


middlewares: Sequence[Middleware] = [
    Middleware(CORSMiddleware),
    Middleware(RequestParserMiddleware),
]
routes: Sequence[BaseRoute] = [
    Host(host=f"api.{settings.HOST}", app=api, name="apis"),
    Host(host=settings.HOST, app=front_end, name="main_site"),
]


def startup():
    DB.connect("db/users.json", "db/todo.json")


def shutdown():
    DB.disconnect()


app = Starlette(
    debug=True,
    routes=routes,
    middleware=middlewares,
    on_startup=[startup],
    on_shutdown=[shutdown],
)
