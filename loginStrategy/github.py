import time

from selenium.webdriver.common.by import By
# import time


def login(driver, config):
    original_tab = driver.current_window_handle
    login_btn = driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[2]/main/div/div/div[8]/div/div[2]/button')
    login_btn.click()
    handlers = driver.window_handles
    for handle in handlers:
        if original_tab != handle:
            driver.switch_to.window(handle)
    driver.implicitly_wait(4)
    time.sleep(0.8)
    username_field = driver.find_element(by=By.ID, value='login_field')
    password_field = driver.find_element(by=By.ID, value='password')
    username_field.send_keys(config['username'])
    time.sleep(1)
    password_field.send_keys(config['password'])
    time.sleep(1)
    signin_btn = driver.find_element(by=By.XPATH, value='//*[@id="login"]/div[3]/form/div/input[11]')
    signin_btn.click()
    time.sleep(2)
    reauth_btn = driver.find_elements(by=By.XPATH, value='//*[@id="js-oauth-authorize-btn"]')
    if len(reauth_btn) > 0:
        reauth_btn[0].click()
        time.sleep(1.4)
    driver.switch_to.window(original_tab)
    print('Successfully logged in')
