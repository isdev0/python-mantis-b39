import pymysql
from model.project import Project


class DbFixture:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password, autocommit=True)

    def get_all_projects(self):
        sql_query = "SELECT id, name, status, enabled, view_state, description, inherit_global FROM mantis_project_table"
        cursor = self.connection.cursor()
        records = []
        try:
            cursor.execute(sql_query)
            for row in cursor:
                (id, name, status, enabled, view_state, description, inherit_global) = row
                records.append(Project(id=str(id), name=name, status=status, view_state=view_state, description=description, inherit_global=inherit_global, enabled=enabled))
        finally:
            cursor.close()
        return records

    def destroy(self):
        self.connection.close()
