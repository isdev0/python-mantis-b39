from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app
        self.soap_connect = app.config["web"]["base_url"] + "/api/soap/mantisconnect.php?wsdl"

    def can_login(self, username, password):
        client = Client(self.soap_connect)
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

    def get_all_projects(self):
        client = Client(self.soap_connect)
        try:
            return self.convert_projects_to_model(client.service.mc_projects_get_user_accessible(self.app.config["web"]["username"], self.app.config["web"]["password"]))
        except WebFault:
            return []
