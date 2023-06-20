from decouple import config


DB_HOST: str = config("DB_HOST")
DB_PORT: int = config("DB_PORT")
DB_NAME: str = config("DB_NAME")
DB_USER: str = config("DB_USER")
DB_PASS: str = config("DB_PASS")
