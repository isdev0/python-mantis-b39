from model.project import Project


def test_add_project(app, db, data_projects):
    app.session.do_login("administrator", "secret")

    old_projects = db.get_all_projects()
    app.project.create(data_projects)

    new_projects = db.get_all_projects()
    old_projects.append(data_projects)

    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
