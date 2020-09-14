from getpass import getpass

import tamr_client as tc

username = input("Tamr Username:")
password = getpass("Tamr Password:")

auth = tc.UsernamePasswordAuth(username, password)
session = tc.session.from_auth(auth)

protocol = "http"
host = "localhost"
port = 9100

instance = tc.Instance(protocol=protocol, host=host, port=port)

print(tc.version(session, instance))
