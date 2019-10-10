from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

from flask_proxy import flask_proxy

auth = UsernamePasswordAuth("username", "password")
tamr = Client(auth, host="my_host")

passthru = flask_proxy(tamr)
app = Flask(__name__)


@app.route("/api/versioned/v1/projects")
def projects(*args, **kwargs):
    print("projects endpoint was called!")
    return passthru(*args, **kwargs)


# all other endpoints, passthru without doing anything special
app.route("/api/<path:path>", methods=["POST", "GET", "PUT", "DELETE"])(passthru)

if __name__ == "__main__":
    app.run(debug=True)
