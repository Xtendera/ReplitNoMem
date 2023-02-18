from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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
        username_bytes = username.encode('ascii')
        password_bytes = password.encode('ascii')

        username_base64_bytes = base64.b64encode(username_bytes)
        password_base64_bytes = base64.b64encode(password_bytes)
        username_base64 = username_base64_bytes.decode('ascii')
        password_base64 = password_base64_bytes.decode('ascii')
        configObject = {
            'username': username_base64,
            'password': password_base64
        }
        configWrite = open('./config.json', 'w')
        configWrite.write(json.dumps(configObject))
        configWrite.close()
        print('Written config')
        time.sleep(1)

    config = json.loads(open('./config.json', 'r').read())
    username_todecode = config['username']
    password_todecode = config['password']
    config['username'] = (base64.b64decode(username_todecode.encode("ascii"))).decode()
    config['password'] = (base64.b64decode(password_todecode.encode("ascii"))).decode()

    print("Starting chromedriver...")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://replit.com/login")
    print("Choosing Github Login Strategy...")
    login(driver, config)


if __name__ == '__main__':
    configureSelenium()
