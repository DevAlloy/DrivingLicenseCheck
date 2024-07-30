import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


BOT_TOKEN = os.environ['DEVALLOY_BOT_TOKEN']
CHAT_ID = os.environ['DEVALLOY_CHAT_ID']
CASE_ID = os.environ['FUEHRERSCHEIN_CASE_ID']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    return response

chrome_options = Options()
chrome_options.binary_location = '/usr/bin/chromium-browser'
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

chromium_version = '127.0.6533.72'
chrome_service = ChromeService(executable_path=ChromeDriverManager(version=chromium_version).install())

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get('https://www17.muenchen.de/Fuehrerschein/FueController')

try:
    input_field = driver.find_element(By.NAME, 'nummer')

    input_field.send_keys(CASE_ID)

    submit_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Auskunft"]')
    submit_button.click()

    body_text = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table/tbody/tr[13]/td/font').text
    
    if "Ihr Antrag wird bearbeitet, bitte haben Sie Geduld." in body_text:
        result_message = "Still waiting :/\n" + body_text
    else:
        result_message = "Hooray!!! " + body_text
        
    send_telegram_message(result_message)

finally:
    driver.quit()
