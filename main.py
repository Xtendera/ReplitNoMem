from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def configureSelenium():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


if __name__ == '__main__':
    configureSelenium()
