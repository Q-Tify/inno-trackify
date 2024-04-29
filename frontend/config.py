import os

GIT_INFO = ""
if os.path.exists("git.info"):
    with open("git.info") as f:
        GIT_INFO = f.read()
        GIT_INFO = GIT_INFO.replace("=", "&nbsp;")