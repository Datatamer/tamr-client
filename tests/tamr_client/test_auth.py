import tamr_client as tc


def test_auth_hidden_password():
    username = "username"
    password = "secure_password"
    auth = tc.UsernamePasswordAuth(username, password)

    assert password not in repr(auth)
    assert password not in str(auth)
