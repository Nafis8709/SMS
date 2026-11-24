import os


class Config:
    """All settings come from environment variables, with safe defaults."""

    def __init__(self, overrides=None):
        self.APP_ENV = os.environ.get("APP_ENV", "development")
        self.LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
        self.DATABASE_PATH = os.environ.get("DATABASE_PATH", "sms.db")

        # Tests pass overrides, e.g. a temporary database file
        if overrides:
            for key, value in overrides.items():
                setattr(self, key, value)
