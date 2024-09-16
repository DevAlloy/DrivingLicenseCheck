import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


BOT_TOKEN = os.environ['DEVALLOY_BOT_TOKEN']
CHAT_ID = os.environ['DEVALLOY_CHAT_ID']
CASE_ID = os.environ['FUEHRERSCHEIN_CASE_ID']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    return response

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://www17.muenchen.de/Fuehrerschein/FueController')

try:
    input_field = driver.find_element(By.NAME, 'nummer')

    input_field.send_keys(CASE_ID)

    submit_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Auskunft"]')
    submit_button.click()

    body_text = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table/tbody/tr[13]/td/font').text
    
    if "Fahrschule" not in body_text:
        result_message = "Still waiting :/\n" + body_text
    else:
        result_message = "Hooray!!! " + body_text
        
    send_telegram_message(result_message)

finally:
    driver.quit()
