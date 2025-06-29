import os

from dotenv import load_dotenv

class EnvironmentParser:
    db_uri: str
    database_name: str

    def __init__(self):
        load_dotenv()
        self.db_uri = os.getenv("DB_URI")
        self.database_name = os.getenv("DATABASE_NAME")