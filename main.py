import os
import sys
from sys import platform
import time
from dotenv import load_dotenv
from pyfiglet import figlet_format
from termcolor import cprint
from colorama import init
from selenium import webdriver


init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected

cprint(figlet_format('codeRedeemerPy', font='smslant'), 'green')

if platform == "linux" or platform == "linux2":
    browser = webdriver.Chrome('./webdriver/chromedriver-linux')
elif platform == "darwin":
    browser = webdriver.Chrome('./webdriver/chromedriver-mac')
elif platform == "win32":
    browser = webdriver.Chrome('./webdriver/chromedriver.exe')

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")


def logic(code, char, occ):
    if occ == 1:
        for i in range(0, 10):
            output = code.replace(char, str(i), 1)
            print('Testing\t' + output)
            # Testing codes
            code_tester(output)
    elif occ == 2:
        for i in range(0, 10):
            for j in range(0, 10):
                output = code.replace(char, str(i), 1)
                output = output.replace(char, str(j), 1)
                print('Testing\t' + output)
                # Testing codes
                code_tester(output)
    elif occ == 3:
        for i in range(0, 10):
            for j in range(0, 10):
                for k in range(0, 10):
                    output = code.replace(char, str(i), 1)
                    output = output.replace(char, str(j), 1)
                    output = output.replace(char, str(k), 1)
                    print('Testing\t' + output)
                    # Testing codes
                    code_tester(output)


def browser_actions():
    browser.get(URL)
    steam_button = browser.find_elements_by_xpath(
        '//*[@id="header"]/div[2]/ul/li[14]/a')[0]
    steam_login_url = steam_button.get_attribute("href")
    browser.get(steam_login_url)
    username_input = browser.find_elements_by_xpath(
        '//*[@id="steamAccountName"]')[0]
    username_input.send_keys(USERNAME)
    password_input = browser.find_elements_by_xpath(
        '//*[@id="steamPassword"]')[0]
    password_input.send_keys(PASSWORD)
    sign_in_button = browser.find_elements_by_xpath(
        '//*[@id="imageLogin"]')[0]
    sign_in_button.click()
    if is_phone_guard_method:
        cprint('Preparing phone auth', 'yellow')
        steam_guard_code = input('Enter your Steam Guard code: ')
        steam_guard_code = steam_guard_code.upper()
        steam_guard_input = browser.find_elements_by_xpath(
            '//*[@id="twofactorcode_entry"]')[0]
        steam_guard_input.send_keys(steam_guard_code)
        steam_guard_submit = browser.find_elements_by_xpath(
            '//*[@id="login_twofactorauth_buttonset_entercode"]/div[1]')[0]
        steam_guard_submit.click()
        time.sleep(3)
    else:
        cprint('Preparing mail auth', 'yellow')
        steam_guard_code = input('Enter your Steam Guard code: ')
        steam_guard_code = steam_guard_code.upper()
        steam_guard_input = browser.find_elements_by_xpath(
            '//*[@id="authcode"]')[0]
        steam_guard_input.send_keys(steam_guard_code)
        steam_guard_submit = browser.find_elements_by_xpath(
            '//*[@id="auth_buttonset_entercode"]/div[1]')[0]
        steam_guard_submit.click()
        time.sleep(3)
        steam_guard_proceed_button = browser.find_elements_by_xpath(
            '//*[@id="success_continue_btn"]')[0]
        steam_guard_proceed_button.click()
    balance_button = browser.find_elements_by_xpath(
        '//*[@id="addbalance"]')[0]
    balance_button.click()


def code_tester(code):
    promocode_input = browser.find_elements_by_xpath(
        '//*[@id="payment_modal"]/div/div/div[1]/div[2]/div[2]/div[1]/div/input')[0]
    promocode_input.send_keys(code)
    promocode_use_button = browser.find_elements_by_xpath(
        '//*[@id="payment_modal"]/div/div/div[1]/div[2]/div[2]/div[1]/div/a')[0]
    promocode_use_button.click()


multiple_codes = True
first_time = True
is_phone_guard_method = None

while(multiple_codes):
    # borrow_args()
    code = input('Enter the encrypted code: ')
    special_char = input('Enter the encryption special character: ')
    special_char_occurrences = code.count(special_char)
    cprint('There are ' + str(special_char_occurrences) + ' occurrences', 'yellow')
    multiple_codes = input(
        'Are you going to enter another code later? (Y/n): ')
    if multiple_codes == 'Y' or multiple_codes == 'y' or multiple_codes == '':
        multiple_codes = True
    else:
        multiple_codes = False
    if first_time:
        is_phone_guard_method = input(
            'Are you using Steam Guard with your phone? (Y/n): ')
        if is_phone_guard_method == 'Y' or is_phone_guard_method == 'y' or is_phone_guard_method == '':
            is_phone_guard_method = True
        else:
            is_phone_guard_method = False
    if first_time:
        browser_actions()
    logic(code, special_char, special_char_occurrences)
    first_time = False

cprint('Bye!', 'yellow')
