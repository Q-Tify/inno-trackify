import os

SECRET_KEY = os.environ.get("SECRET_KEY", '2346f0f4c6aa953b93f70a6cf63b809d25e0514l799f94fbc6ca7321t78e8d3e7') 
ALGORITHM =os.environ.get("ALGORITHM", 'HS256') 
EXPIRE_TIME_MINUTES = os.environ.get("EXPIRE_TIME_MINUTES", 15) 