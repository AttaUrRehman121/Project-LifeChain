import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase

class AuthFlowTest(LiveServerTestCase):
    results = []

    def setUp(self):
        chrome_path = r"chromedriver.exe"
        self.driver = webdriver.Chrome(service=Service(chrome_path))
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = self.live_server_url

    def record_result(self, test_name, passed):
        self.results.append({'Test Case': test_name, 'Status': 'Passed' if passed else 'Failed'})

    def test_1_donor_signup_and_login_flow(self):
        try:
            # Donor Signup
            self.driver.get(self.base_url + "/registration/")
            self.driver.find_element(By.NAME, 'username').send_keys('testuserD')
            self.driver.find_element(By.NAME, 'email').send_keys('testD@example.com')
            self.driver.find_element(By.NAME, 'nationality').send_keys('Pakistani')
            self.driver.find_element(By.NAME, 'role').send_keys('donor')
            self.driver.find_element(By.NAME, 'contact').send_keys('03123456789')
            self.driver.find_element(By.NAME, 'address').send_keys('Someaddress')
            self.driver.find_element(By.NAME, 'password').send_keys('TestD@1234')
            self.driver.find_element(By.NAME, 'password2').send_keys('TestD@1234')
            self.driver.find_element(By.ID, 'signup-btn').click()

            self.wait.until(EC.url_contains('login'))
            self.assertIn('login', self.driver.current_url)
            self.assertIn("Please log in", self.driver.page_source)
            self.record_result('Signup Donor Flow', True)

            # Donor Login
            self.driver.get(self.base_url + "/registration/login/")
            self.driver.find_element(By.NAME, 'username').send_keys('testuserD')
            self.driver.find_element(By.NAME, 'password').send_keys('TestD@1234')
            self.driver.find_element(By.ID, 'login-btn').click()

            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'logout-btn')))
            self.driver.find_element(By.CLASS_NAME, 'logout-btn').click()

            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            current_url = self.driver.current_url
            if current_url.rstrip('/') == self.base_url.rstrip('/'):
                self.record_result('Login Donor Flow', True)
            else:
                self.record_result('Login Donor Flow', False)
                raise Exception("Logout did not redirect to home page")

        except Exception:
            self.record_result('Login Donor Flow', False)
            print("Donor Flow Error Page Source:", self.driver.page_source[:500])
            raise

    def test_2_recipient_signup_and_login_flow(self):
        try:
            # Recipient Signup
            self.driver.get(self.base_url + "/registration/")
            self.driver.find_element(By.NAME, 'username').send_keys('testuserR')
            self.driver.find_element(By.NAME, 'email').send_keys('testR@example.com')
            self.driver.find_element(By.NAME, 'nationality').send_keys('Pakistani')
            self.driver.find_element(By.NAME, 'role').send_keys('recipient')
            self.driver.find_element(By.NAME, 'contact').send_keys('03123456789')
            self.driver.find_element(By.NAME, 'address').send_keys('Someaddress')
            self.driver.find_element(By.NAME, 'password').send_keys('TestR@1234')
            self.driver.find_element(By.NAME, 'password2').send_keys('TestR@1234')
            self.driver.find_element(By.ID, 'signup-btn').click()

            self.wait.until(EC.url_contains('login'))
            self.assertIn('login', self.driver.current_url)
            self.assertIn("Please log in", self.driver.page_source)
            self.record_result('Signup Recipient Flow', True)

            # Recipient Login
            self.driver.get(self.base_url + "/registration/login/")
            self.driver.find_element(By.NAME, 'username').send_keys('testuserR')
            self.driver.find_element(By.NAME, 'password').send_keys('TestR@1234')
            self.driver.find_element(By.ID, 'login-btn').click()

            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'logout-btn')))
            self.driver.find_element(By.CLASS_NAME, 'logout-btn').click()

            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            current_url = self.driver.current_url
            if current_url.rstrip('/') == self.base_url.rstrip('/'):
                self.record_result('Login Recipient Flow', True)
            else:
                self.record_result('Login Recipient Flow', False)
                raise Exception("Logout did not redirect to home page")

        except Exception:
            self.record_result('Login Recipient Flow', False)
            print("Recipient Flow Error Page Source:", self.driver.page_source[:500])
            raise

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\n\n=== Test Summary ===")
        print("{:<30} {:<10}".format("Test Case", "Status"))
        print("-" * 42)
        for result in cls.results:
            print("{:<30} {:<10}".format(result['Test Case'], result['Status']))
        print("=" * 42)
if __name__ == "__main__":  
    unittest.main()



