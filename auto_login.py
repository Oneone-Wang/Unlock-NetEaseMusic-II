# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "004CEF78FCB27224504D0FB3FB35ACD700E34D6DDB3AD5DB3933D19FFC8707C3C6A97E6455B496F3F49EC3C617D29F86E25D326A02C00C81C69E950DCE6764AA5FB193A0FA9B114D59AF9AD22BEF2038847EED82C782D9CA97F61516F951624DB388ACEB2B8C2B8BEBFC924B61F589D6A30F30CC9118D85205E3ED6CE7CB1958F680EBC44FE34F087EAD1726F5195A7ABB933D7C374E22EF1A4B65E93E824D7E998F7093B063F5F231A7077A15C8703EA7B8A0A11392489626DB61D89A2F4ADE2BC1E3A205045CF5CC62AE190C3E04F0AB1FF63F59D5069AEE1D0B174DBC0C1B38A193E65A3CE32CCDC0DA1BB016FCC297C9A5C365AC8EC83320A8F9FDC02BAF9A02494319BAE93CB8006C0EC55B01BE5E4CD969014B945A3196DF93769A398A70E7BF45515AB9F29A482340155E8FD4DB936A65C224EAB3A716EEF525CCB7FA7599F333CC20E84BC9D557E626D3F02DD29162208350212A60DC893000DA13F450"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
