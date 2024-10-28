from starlette.routing import Route
from starlette.middleware import Middleware

from middlewares import AuthMiddleware
from .utils import register, login, user

routes = [
    Route("/register", register, methods=["POST"]),
    Route("/login", login, methods=["POST"]),
    Route("/user", user, name="user", middleware=[Middleware(AuthMiddleware)]),
]
