import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


BOT_TOKEN = os.environ['DEVALLOY_BOT_TOKEN']
CHAT_ID = os.environ['DEVALLOY_CHAT_ID']
CASE_ID = os.environ['FUEHRERSCHEIN_CASE_ID']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    return response

def lambda_handler(event, context):
    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(
        executable_path="/opt/chromedriver",
        options=options
    )
    driver.get('https://www17.muenchen.de/Fuehrerschein/FueController')

    try:
        # Находим поле ввода
        input_field = driver.find_element(By.NAME, 'nummer')
    
        # Вводим строку
        input_field.send_keys(CASE_ID)
    
        # Находим и нажимаем кнопку отправки
        submit_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Auskunft"]')
        submit_button.click()
    
        # Ждем загрузки результата (может понадобиться явное ожидание)
        # wait = WebDriverWait(driver, 100)
        # body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
        # Читаем текст результата
        body_text = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table/tbody/tr[13]/td/font').text
        # 
        if "Ihr Antrag wird bearbeitet, bitte haben Sie Geduld." in body_text:
            result_message = "Еще ждем :/\n" + body_text
        else:
            result_message = "УРА!!! " + body_text
            
        send_telegram_message(result_message)
    
    finally:
        # Закрываем браузер
        driver.quit()