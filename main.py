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
    print("Version 0.1\n")
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
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://replit.com/login")
    print("Choosing Github Login Strategy")
    login(driver, config)
    time.sleep(1)
    print('Locating/creating notouch.txt')
    driver.get(url=config['replitURL'])
    time.sleep(2)
    notif_deny_btn = driver.find_element(by=By.XPATH, value='/html/body/reach-portal/div[2]/div/div/div['
                                                            '2]/div/div/div/div/div/button[1]')
    notif_deny_btn.click()
    time.sleep(0.7)
    for file in driver.find_elements(by=By.XPATH, value='//*[@id="sidebar-section-content-files"]/div/div/div/div/div'
                                                        '/div/div/*'):
        if file.get_attribute('title'):
            print(file.get_attribute('title'))
        else:
            file_name = file.find_element(by=By.XPATH, value='.//div/div[1]/div[2]/span')
            print(file_name.text)

    time.sleep(500)


if __name__ == '__main__':
    configureSelenium()
