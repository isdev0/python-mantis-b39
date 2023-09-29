from model.project import Project


testdata = [
    Project(name="Test Project 1", description="Description Project 1", status="release", view_state="public"),
    Project(name="Test Project 2", description="Description Project 2", status="stable", view_state="private"),
    Project(name="Test Project 3", description="Description Project 3", status="obsolete", view_state="private", inherit_global=False)
]
