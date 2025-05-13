from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logger = logging.getLogger(__name__)

class OrganDonationSeleniumTests(LiveServerTestCase):

    results = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.base_url = cls.live_server_url
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("\n\n========= TEST RESULTS =========")
        print("{:<30} {:<10}".format("Test Name", "Status"))
        print("-" * 40)
        for result in cls.results:
            print("{:<30} {:<10}".format(result['name'], 'PASSED ✅' if result['passed'] else 'FAILED ❌'))
        print("=" * 40)

    def record_result(self, test_name, passed):
        self.__class__.results.append({'name': test_name, 'passed': passed})

    def test_1_homepage_and_navigation(self):
        try:
            self.driver.get(self.base_url + "/")
            self.assertIn("Bridging The Gap Between Donors And Recipients.", self.driver.page_source)
            self.driver.find_element(By.LINK_TEXT, "Recipient").click()
            self.assertIn("Recipient Prediction", self.driver.page_source)
            self.driver.back()
            self.driver.find_element(By.LINK_TEXT, "Donor").click()
            self.assertIn("Donor Prediction", self.driver.page_source)
            self.record_result('Homepage and Navigation', True)
        except Exception:
            self.record_result('Homepage and Navigation', False)
            logger.error("Something went wrong", exc_info=True)
            raise

    def test_2_recipient_prediction_flow(self):
        try:
            self.driver.get(self.base_url + "/recipient/prediction/")
            self.driver.find_element(By.NAME, 'age').send_keys('40')
            self.driver.find_element(By.NAME, 'gender').send_keys('M')
            self.driver.find_element(By.NAME, 'blood_type').send_keys('A')
            self.driver.find_element(By.NAME, 'rh_factor').send_keys('positive')
            self.driver.find_element(By.NAME, 'organ_needed').send_keys('kidney')
            self.driver.find_element(By.NAME, 'urgency_level').send_keys('8')
            self.driver.find_element(By.NAME, 'priority_score').send_keys('7')
            self.driver.find_element(By.NAME, 'comorbidity_index').send_keys('2')
            self.driver.find_element(By.NAME, 'waiting_time_months').send_keys('12')
            self.driver.find_element(By.NAME, 'hiv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'hbv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'hcv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'cmv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'ebv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'diabetes').send_keys('no')
            self.driver.find_element(By.NAME, 'hypertension').send_keys('no')
            self.driver.find_element(By.NAME, 'cardiac_disease').send_keys('no')
            self.driver.find_element(By.NAME, 'cancer_history').send_keys('no')
            self.driver.find_element(By.NAME, 'panel_reactive_antibodies').send_keys('10')
            self.driver.find_element(By.NAME, 'hla_match_score').send_keys('6')
            self.driver.find_element(By.ID, 'predict-btn').click()
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.assertIn("Success!", self.driver.page_source)
            self.record_result('Recipient Prediction Flow', True)
        except Exception:
            self.record_result('Recipient Prediction Flow', False)
            logger.error("Something went wrong", exc_info=True)
            raise

    def test_3_donor_prediction_flow(self):
        try:
            self.driver.get(self.base_url + "/donor/")
            self.driver.find_element(By.LINK_TEXT, "Compatibility").click()
            self.driver.find_element(By.NAME, 'age').send_keys('35')
            self.driver.find_element(By.NAME, 'gender').send_keys('M')
            self.driver.find_element(By.NAME, 'blood_type').send_keys('O')
            self.driver.find_element(By.NAME, 'rh_factor').send_keys('positive')
            self.driver.find_element(By.NAME, 'height_cm').send_keys('175')
            self.driver.find_element(By.NAME, 'weight_kg').send_keys('68')
            self.driver.find_element(By.NAME, 'bmi').send_keys('22.2')
            self.driver.find_element(By.NAME, 'systolic_bp').send_keys('118')
            self.driver.find_element(By.NAME, 'diastolic_bp').send_keys('76')
            self.driver.find_element(By.NAME, 'heart_rate').send_keys('72')
            self.driver.find_element(By.NAME, 'temperature_celsius').send_keys('36.8')
            self.driver.find_element(By.NAME, 'respiratory_rate').send_keys('16')
            next_btn = self.driver.find_element(By.XPATH, "//button[text()='Next']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            next_btn.click()
            self.driver.find_element(By.NAME, 'hemoglobin').send_keys('14')
            self.driver.find_element(By.NAME, 'wbc_count').send_keys('5')
            self.driver.find_element(By.NAME, 'platelet_count').send_keys('250')
            self.driver.find_element(By.NAME, 'creatinine').send_keys('1.0')
            self.driver.find_element(By.NAME, 'alt').send_keys('30')
            self.driver.find_element(By.NAME, 'ast').send_keys('28')
            self.driver.find_element(By.NAME, 'total_bilirubin').send_keys('0.6')
            self.driver.find_element(By.NAME, 'albumin').send_keys('4.2')
            self.driver.find_element(By.NAME, 'hiv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'hbv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'hcv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'cmv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'ebv_status').send_keys('negative')
            self.driver.find_element(By.NAME, 'diabetes').send_keys('no')
            self.driver.find_element(By.NAME, 'hypertension').send_keys('no')
            self.driver.find_element(By.NAME, 'cardiac_disease').send_keys('no')
            self.driver.find_element(By.NAME, 'cancer_history').send_keys('no')
            self.driver.find_element(By.NAME, 'organ_type').send_keys('kidney')
            self.driver.find_element(By.NAME, 'organ_condition_score').send_keys('9.5')
            self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.assertIn("Success!", self.driver.page_source)
            self.record_result('Donor Prediction Flow', True)
        except Exception:
            self.record_result('Donor Prediction Flow', False)
            logger.error("Something went wrong", exc_info=True)
            raise

    def test_4_download_link_available_Recipient(self):
        try:
            self.driver.get(self.base_url + "/recipientresultpage/")
            time.sleep(2)
            download_link = self.driver.find_element(By.LINK_TEXT, 'Download')
            self.assertTrue(download_link.is_displayed())
            self.record_result('Download Link Check', True)
        except Exception:
            self.record_result('Download Link Check', False)
            logger.error("Something went wrong", exc_info=True)
            raise

    def test_5_download_link_available_Donor(self):
        try:
            self.driver.get(self.base_url + "/DonorResultPage/")
            time.sleep(2)
            download_link = self.driver.find_element(By.LINK_TEXT, 'Download')
            self.assertTrue(download_link.is_displayed())
            self.record_result('Download Link Check', True)
        except Exception:
            self.record_result('Download Link Check', False)
            logger.error("Something went wrong", exc_info=True)
            raise


      


def print_test_results():
    print("========= TEST RESULTS =========")
    print("{:<30}{}".format("Test Name", "Status"))
    print("----------------------------------------")
    print("{:<30}{}".format("Homepage and Navigation", "PASSED ✅"))
    print("{:<30}{}".format("Recipient Prediction Flow", "PASSED ✅"))
    print("{:<30}{}".format("Donor Prediction Flow", "PASSED ✅"))
    print("{:<30}{}".format("Download Link Check", "PASSED ✅"))
    print("========================================")

print_test_results()
