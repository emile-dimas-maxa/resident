import os

from dotenv import load_dotenv


def get_env() -> dict:
	load_dotenv(".env/.env")
	return {
		"database": os.getenv("DB_NAME"),
		"username": os.getenv("DB_USER"),
		"password": os.getenv("DB_PASSWORD"),
		"host": os.getenv("DB_HOST"),
		"port": int(os.getenv("DB_PORT")),
	}
