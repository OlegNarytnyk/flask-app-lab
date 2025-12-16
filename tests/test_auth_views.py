def test_register_page_loads(client):
    resp = client.get("/register")
    assert resp.status_code == 200
    assert b"Register" in resp.data or b"Sign up" in resp.data


def test_login_page_loads(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data