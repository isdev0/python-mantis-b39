import random
from model.project import Project


def test_delete_random_project(app, db):
    app.session.do_login("administrator", "secret")

    if len(db.get_all_projects()) == 0:
        app.project.create(Project(name="TestForDeleting", status="stable", view_state="public", inherit_global=False, description="TestForDeleting Description"))

    old_projects = db.get_all_projects()
    project = random.choice(old_projects)

    print("\nRandom project: [%s] %s" % (str(project.id), project.name))
    app.project.delete_by_id(project.id)

    new_projects = db.get_all_projects()
    assert len(old_projects) - 1 == len(new_projects)

    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
