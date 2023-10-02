from model.project import Project


def test_add_project(app, data_projects):
    username = app.config["web"]["username"]
    password = app.config["web"]["password"]
    app.session.do_login(username, password)

    old_projects = app.soap.get_all_projects()
    app.project.create(data_projects)

    new_projects = app.soap.get_all_projects()
    old_projects.append(data_projects)

    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
