

def test_signup_new_account(app):
    username = "user1"
    password = "test"
    app.email.ensure_user_exists(username, password)