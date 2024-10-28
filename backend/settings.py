from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

HOST = config("HOST")
SALT = config("SALT", cast=Secret)
SECRET = config("SECRET", cast=Secret)
