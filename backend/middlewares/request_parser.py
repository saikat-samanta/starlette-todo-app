from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.requests import Request


class RequestParserMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope, receive, send)
        try:
            body = await request.json()
            scope["body"] = body
        except Exception:
            scope["body"] = None
        await self.app(scope, receive, send)
