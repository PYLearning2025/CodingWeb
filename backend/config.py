import sys
import os
import secrets

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    def __init__(self):
        self.load_environment_variables()
        self.check_required_variables()

    def load_environment_variables(self):
        self.MONGODB_URL = os.getenv("MONGODB_URL")
        self.PASETO_SECRET_KEY = secrets.token_hex(32)

    def check_required_variables(self):
        required_variables = ["MONGODB_URL", "PASETO_SECRET_KEY"]

        missing_variables = [var for var in required_variables if not getattr(self, var)]

        if missing_variables:
            print(f"Error: Missing required environment variables: {', '.join(missing_variables)}")
            sys.exit(1)

config = Config()