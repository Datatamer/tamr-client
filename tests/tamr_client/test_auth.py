import tamr_client as tc


def test_auth_hidden_password():
    username = "username"
    password = "secure_password"
    auth = tc.UsernamePasswordAuth(username, password)

    assert password not in repr(auth)
    assert password not in str(auth)


def test_auth_hidden_jwt():
    jwt_token = "secure_token"
    auth = tc.JwtTokenAuth(jwt_token)

    assert jwt_token not in repr(auth)
    assert jwt_token not in str(auth)
