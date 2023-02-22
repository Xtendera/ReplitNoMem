from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from art import tprint
import time
import base64
import json
from pathlib import Path
from loginStrategy.github import login


def configureSelenium():
    tprint("ReplitNoMem")
    print("Version 1.2\n")
    time.sleep(2)
    path = Path('./config.json')
    if not path.is_file():
        print('Config file not found, starting first-time setup')
        time.sleep(1)
        username = input('Username: ')
        password = input('Password: ')
        url = input('Replit URL: ')
        username_bytes = username.encode('ascii')
        password_bytes = password.encode('ascii')

        username_base64_bytes = base64.b64encode(username_bytes)
        password_base64_bytes = base64.b64encode(password_bytes)
        username_base64 = username_base64_bytes.decode('ascii')
        password_base64 = password_base64_bytes.decode('ascii')
        config_object = {
            'username': username_base64,
            'password': password_base64,
            'replitURL': url
        }
        config_write = open('./config.json', 'w')
        config_write.write(json.dumps(config_object))
        config_write.close()
        print('Written config')
        time.sleep(1)

    config = json.loads(open('./config.json', 'r').read())
    username_decode = config['username']
    password_decode = config['password']
    config['username'] = (base64.b64decode(username_decode.encode("ascii"))).decode()
    config['password'] = (base64.b64decode(password_decode.encode("ascii"))).decode()

    print("Starting chromedriver...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get("https://replit.com/login")
    print("Choosing Github Login Strategy")
    login(driver, config)
    time.sleep(1)
    print('Locating notouch.txt')
    driver.get(url=config['replitURL'])
    time.sleep(2)
    notif_deny_btn = driver.find_elements(by=By.XPATH, value='/html/body/reach-portal/div[2]/div/div/div['
                                                            '2]/div/div/div/div/div/button[1]')
    if len(notif_deny_btn) > 0:
        notif_deny_btn[0].click()
    time.sleep(0.7)
    found_file = False
    for file in driver.find_elements(by=By.XPATH, value='//*[@id="sidebar-section-content-files"]/div/div/div/div/div'
                                                        '/div/div/*'):
        if file.get_attribute('title'):
            continue
        else:
            file_name = file.find_element(by=By.XPATH, value='.//div/div[1]/div[2]/span').text
            if file_name == 'notouch.txt':
                file.click()
                found_file = True

    if not found_file:
        raise Exception("notouch.txt was not found in the replit")

    time.sleep(1)
    print('Inputting random values...')
    random_text = ''
    text_field = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div[2]/div/div[9]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div')
    x = 0
    while x < 100:
        if len(random_text) > 54:
            random_text = ''
        else:
            random_text += 'donttouch'

        driver.execute_script("arguments[0].innerText = '{}'".format(random_text), text_field, random_text)
        x += 1
        time.sleep(0.7)
    driver.quit()
    configureSelenium()

if __name__ == '__main__':
    configureSelenium()
