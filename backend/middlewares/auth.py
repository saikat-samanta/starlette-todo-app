from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.requests import Request
from starlette.responses import JSONResponse
from utils import jwt_decode
from database import DB


class AuthMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope, receive, send)
        if scope["path"] != "/":
            token = request.headers.get("authorization")
            if not token:
                return await JSONResponse(
                    {"message": "Authorization header not found"}, status_code=401
                )(scope, receive, send)

            token = token.replace("Bearer ", "")
            try:
                payload = jwt_decode(token)
            except Exception:
                return await JSONResponse(
                    {"message": "Unable to authenticate you"}, status_code=401
                )(scope, receive, send)

            if not payload.get("id"):
                return await JSONResponse(
                    {"message": "Invalid token"}, status_code=401
                )(scope, receive, send)

            user = DB.user_client.getById(payload["id"])

            if not user:
                return await JSONResponse(
                    {"message": "Invalid token"}, status_code=401
                )(scope, receive, send)

            del user["password"]

            scope["user"] = user

        await self.app(scope, receive, send)
