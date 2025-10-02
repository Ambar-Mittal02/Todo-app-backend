import os
from dotenv import load_dotenv

env = os.environ
load_dotenv()


POSTGRES_DB = env.get("POSTGRES_DB", "todo_app")
POSTGRES_USER = env.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = env.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = env.get("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = env.get("POSTGRES_PORT", "5432")


