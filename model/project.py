from sys import maxsize
from enum import Enum


class Project:

    def __init__(self, id=None, name=None, status=None, enabled=None, inherit_global=None, view_state=None, description=None):
        self.id = id
        self.name = name
        if type(status) is str: self.status = Status[status]
        elif type(status) is int: self.status = Status(status)
        self.enabled = enabled
        self.inherit_global = inherit_global
        if type(view_state) is str: self.view_state = ViewState[view_state]
        elif type(view_state) is int: self.view_state = ViewState(view_state)
        self.description = description

    # representation redefinition
    def __repr__(self):
        return "%s:%s" % (self.id, self.name)

    # equality redefinition
    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize


# $g_project_status_enum_string = '10:development,30:release,50:stable,70:obsolete';
class Status(Enum):
    development = 10
    release = 30
    stable = 50
    obsolete = 70


# $g_project_view_state_enum_string = '10:public,50:private';
class ViewState(Enum):
    public = 10
    private = 50
