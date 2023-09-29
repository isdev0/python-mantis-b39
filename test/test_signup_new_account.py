import string
import random


def get_random_uername(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_signup_new_account(app):
    username = get_random_uername("user_", 10)
    password = "test"
    email = username + "@localhost"
    app.srv_email.ensure_user_exists(username, password)
    app.signup.new_user(username, password, email)
    app.session.login(username, password)
    assert app.session.is_login_as(username)
    app.session.do_logout()
