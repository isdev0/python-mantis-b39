from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        pass

    def create(self, project):
        wd = self.app.wd
        self.app.open_external_page(self.app.base_url + "/manage_proj_create_page.php")

        self.fill_field("name", project.name)
        self.fill_selector("status", str(project.status.value))
        self.check_box("inherit_global", project.inherit_global)
        self.fill_selector("view_state", str(project.view_state.value))
        self.fill_field("description", project.description)

        wd.find_element(By.CSS_SELECTOR, "span.submit-button input.button").click()
        self.open_projects_page()

    def read_by_id(self, id):
        pass

    def update_by_id(self, id):
        pass

    def delete_by_id(self, id):
        wd = self.app.wd
        self.app.open_external_page(self.app.base_url + "/manage_proj_edit_page.php?project_id=%s" % str(id))
        wd.find_element(By.CSS_SELECTOR, "div[id='project-delete-div'] input.button[type='submit']").click()
        wd.find_element(By.CSS_SELECTOR, "div.confirm-msg input.button[type='submit']").click()

    def get_all(self):
        return []

    def fill_field(self, field_name, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element(By.NAME, field_name).click()
            wd.find_element(By.NAME, field_name).clear()
            wd.find_element(By.NAME, field_name).send_keys(value)

    def fill_selector(self, field_name, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element(By.NAME, field_name).click()
            Select(wd.find_element(By.NAME, field_name)).select_by_value(value)
            wd.find_element(By.CSS_SELECTOR, "select[name='" + field_name + "'] > option[value='" + value + "']").click()

    def check_box(self, check_box_name, check_it):
        wd = self.app.wd
        if check_it is not None:
            check_box = wd.find_element(By.NAME, check_box_name)
            is_checked = check_box.get_attribute("checked")
            if (not is_checked and check_it) or (is_checked and not check_it):
                check_box.click()
