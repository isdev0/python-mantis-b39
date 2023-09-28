

def test_login(app):
    app.session.login("administrator", "secret")
    assert app.session.is_login_as("administrator")
