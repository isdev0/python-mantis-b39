from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.3.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    @staticmethod
    def convert_projects_to_model(projects):
        def convert(project):
            new_project = Project(
                id=str(project.id),
                name=project.name,
                status=project.status.name,
                enabled=project.enabled,
                view_state=project.view_state.name,
                description=project.description
            )
            return new_project
        return list(map(convert, projects))

    def get_all_projects(self, username, password):
        client = Client("http://localhost/mantisbt-1.3.20/api/soap/mantisconnect.php?wsdl")
        try:
            return self.convert_projects_to_model(client.service.mc_projects_get_user_accessible(username, password))
        except WebFault:
            return []
