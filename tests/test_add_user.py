import allure
import pytest

from configs.common_parsing import username, password, group_name, \
    new_username, new_password, admin_link
from configs.database_parsing import user_name
from pages.Database_page import DataBasePage
from pages.Group_page import GroupsPage
from pages.Login_page import LoginPage
from pages.User_add_page import User_add_page


class TestAddUser():
    db = DataBasePage()

    @allure.feature('UI tests')
    @allure.story('Login in positive')
    @pytest.mark.positive
    def test_user(self, login_page, browser):
        with allure.step('Admin Authorization Steps'):
            login_user = LoginPage(browser)
            login_user.fill_username_field(username)
            login_user.fill_password_field(password)
            login_user.click_login_field()
        with allure.step('Checking the transition to the page in the admin page'):
            assert login_user.current_url() == admin_link

    @allure.feature('UI tests')
    @allure.story('Checking on the UI of the created group in the database')
    @pytest.mark.positive
    def test_group_from_ui(self, login_page, browser):
        with allure.step('Steps to connect to the database and compare with the UI'):
            self.db.add_group(group_name)
            groups = GroupsPage(browser)
            groups.open_group_page()
        with allure.step('Checking the created group on the UI'):
            assert groups.check_group_exist(group_name)

    @allure.feature('UI and DB tests')
    @allure.story('Checking in the database of the created user in the group')
    @pytest.mark.positive
    def test_user_add(self, login_page, browser):
        with allure.step(
                'Connecting to the DB and Steps to create a user with a group in the UI'):
            new_user = User_add_page(browser)
            new_user.open_add_user_page()
            new_user.fill_username_field(new_username)
            new_user.fill_password_field(new_password)
            new_user.fill_confirm_passwd_field(new_password)
            new_user.click_save_field()
            new_user.click_staff_field()
            new_user.click_add_to_group_field()
            new_user.click_save_field()

        with allure.step('Checking for the creation in the database of a user in a group'):
            assert self.db.user_from_group(user_name, group_name)
