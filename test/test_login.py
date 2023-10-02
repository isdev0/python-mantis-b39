

def test_login(app):
    app.session.login(app.config["web"]["username"], app.config["web"]["password"])
    assert app.session.is_login_as("administrator")
