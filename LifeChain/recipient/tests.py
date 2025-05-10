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
        
    def Recipient_1_PredictionForm(self):
            # Recipient Signup
            self.driver.get(self.base_url + "/Recipient/")
            self.drives.find_element(By.ID, 'RecipinetPrictionButton').Click()
            self.wait.until(EC.url_contains('RecipientPredictionForm'))
            self.assertIn('RecipientPredictionForm', self.driver.current_url)
    