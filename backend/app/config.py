import os

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "dev_security_key",
)
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
EXPIRE_TIME_MINUTES = os.environ.get("EXPIRE_TIME_MINUTES", 15)
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")


GIT_INFO = ''
if os.path.exists("git.info"):
    with open("git.info") as f:
        GIT_INFO = f.read()
        GIT_INFO = GIT_INFO.replace("\n", "<br>").replace("=", "&nbsp;")