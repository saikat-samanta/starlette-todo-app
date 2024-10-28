from pysondb import db


class DBClient:
    user_client: db.JsonDatabase = None
    todo_client: db.JsonDatabase = None

    def __init__(self):
        pass

    def connect(self, file1: str, file2: str):
        DBClient.user_client = db.getDb(filename=file1, log=True)
        DBClient.todo_client = db.getDb(filename=file2, log=True)
        print("DB connected.")

    def disconnect(self):
        DBClient.user_client = None
        DBClient.todo_client = None
        print("DB disconnected.")


DB = DBClient()
