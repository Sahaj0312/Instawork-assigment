from time import sleep
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from . views import TeamMemberList, TeamMemberCreate, TeamMemberDelete, TeamMemberUpdate
from . models import TeamMember
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# Unit tests

class TestUrls(SimpleTestCase):

    # testing that the correct class-based view is called
    def testMembersList(self):
        url = reverse('members')
        self.assertEquals(resolve(url).func.view_class, TeamMemberList)

    # testing that the correct class-based view is called
    def testMemberAdd(self):
        url = reverse('member-add')
        self.assertEquals(resolve(url).func.view_class, TeamMemberCreate)

    # testing that the correct class-based view is called
    def testMemberUpdate(self):
        url = reverse('member-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, TeamMemberUpdate)

    # testing that the correct class-based view is called
    def testMemberDelete(self):
        url = reverse('member-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, TeamMemberDelete)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        TeamMember.objects.create(
            firstName="Jane",
            lastName="Doe",
            email="jane@email.com",
            phoneNumber="0123456789",
            admin=True
        )

    # testing that the correct template (view) is returned
    def test_memberList_GET(self):
        response = self.client.get(reverse('members'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'base/teammember_list.html')

    # testing that the correct template (view) is returned
    def test_memberCreate_GET(self):
        response = self.client.get(reverse('member-add'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'base/teammember_form.html')

    # testing that the correct template (view) is returned
    def test_memberUpdate_GET(self):
        response = self.client.get(reverse('member-update', args=['1']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'base/teammember_form.html')

    # testing that the correct template (view) is returned
    def test_memberDelete_GET(self):
        response = self.client.get(reverse('member-delete', args=['1']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'base/teammember_confirm_delete.html')

# Functional tests


class TestCRUD(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('base/chromedriver')

    def tearDown(self):
        self.browser.close()

    # Function that adds an arbitrary team member to the model
    def addMember(self):
        self.browser.find_element(By.ID, "plus").click()
        self.browser.find_element(By.ID, "id_firstName").send_keys("Jane")
        self.browser.find_element(By.ID, "id_lastName").send_keys("Doe")
        self.browser.find_element(
            By.ID, "id_email").send_keys("janedoe@email.com")
        self.browser.find_element(
            By.ID, "id_phoneNumber").send_keys("0123456789")
        self.browser.find_element(By.ID, "id_admin").click()
        self.browser.find_element(By.TAG_NAME, "form").submit()

    # The app should initially have no members
    def test_no_members(self):
        self.browser.get(self.live_server_url)

        members = self.browser.find_element(
            By.XPATH, "(//div[@class='container']//following-sibling::h3)[1]")
        self.assertEquals(members.text, "You have 0 team members")

    # Testing the apps create and read functionality
    def test_addMember(self):
        self.browser.get(self.live_server_url)
        self.addMember()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('members'))
        members = self.browser.find_element(
            By.XPATH, "(//div[@class='container']//following-sibling::h3)[1]")
        self.assertEquals(members.text, "You have 1 team member")
        name = self.browser.find_element(
            By.XPATH, "(//div[@class='container']//following-sibling::p//following-sibling::b)")
        self.assertEquals(name.text, "Jane Doe")

    # Testing the apps update and read functionality
    def test_editMember(self):
        self.browser.get(self.live_server_url)
        self.addMember()
        self.browser.find_element(By.LINK_TEXT, "edit").click()
        self.browser.find_element(By.ID, "id_firstName").clear()
        self.browser.find_element(By.ID, "id_firstName").send_keys("Jim")
        self.browser.find_element(By.TAG_NAME, "form").submit()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('members'))
        members = self.browser.find_element(
            By.XPATH, "(//div[@class='container']//following-sibling::h3)[1]")
        self.assertEquals(members.text, "You have 1 team member")
        name = self.browser.find_element(
            By.XPATH, "(//div[@class='container']//following-sibling::p//following-sibling::b)")
        self.assertEquals(name.text, "Jim Doe")

    # Testing the apps delete and read functionality
    def test_deleteMember(self):
        self.browser.get(self.live_server_url)
        self.addMember()
        self.browser.find_element(By.LINK_TEXT, "delete").click()
        self.browser.find_element(By.CSS_SELECTOR, "form").submit()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('members'))
        members = self.browser.find_element(
            By.XPATH, "(//div[@class='container']//following-sibling::h3)[1]")
        self.assertEquals(members.text, "You have 0 team members")
