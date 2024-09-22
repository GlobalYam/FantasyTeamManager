from flask import Flask
from os import getenv

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY").replace("://", "ql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace(
    "://", "ql://", 1
)

import routes
