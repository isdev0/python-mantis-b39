import random
from model.project import Project


def test_delete_random_project(app, db):
    username = app.config["web"]["username"]
    password = app.config["web"]["password"]
    app.session.do_login(username, password)

    if len(db.get_all_projects()) == 0:
        app.project.create(Project(name="TestForDeleting", status="stable", view_state="public", inherit_global=False, description="TestForDeleting Description"))

    old_projects = app.soap.get_all_projects(username, password)
    project = random.choice(old_projects)

    print("\nRandom project: [%s] %s" % (str(project.id), project.name))
    app.project.delete_by_id(project.id)

    new_projects = app.soap.get_all_projects(username, password)
    assert len(old_projects) - 1 == len(new_projects)

    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
