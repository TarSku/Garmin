import time
import os
import inquirer

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from progress.bar import Bar
from getpass import getpass

def import_files():
    browser = webdriver.Chrome()
    browser.get("https://www.strava.com/upload/select")

    if my_password_str is not "":
        id_name = browser.find_element_by_id('email')
        id_name.send_keys(my_username)

        id_password = browser.find_element_by_name('password')
        id_password.send_keys(my_password_str)

        id_checkbox = browser.find_element_by_id('login-button')
        id_checkbox.click()

    send_message = 0
    while browser.current_url != "https://www.strava.com/upload/select":

        if send_message == 0:
            print('Please fil in credentials and log in')
            send_message = 1
        time.sleep(3)

    text_file = open("Output.txt", "r")
    activity = text_file.read().split(',')
    del activity[-1]

    uploaded = 0
    duplicated = 0
    failed = 0
    bar = Bar('Uploading', max=len(activity))

    for i in activity:
        browser.get("https://www.strava.com/upload/select")
        try:
            print(os.getcwd()+i)
            browser.find_element_by_name("files[]").send_keys(os.getcwd()+i)
            time.sleep(10)
            try:
                error = browser.find_element_by_xpath("//div[@class='error-message']")
                if error.text.split('_')[0] == 'activity':
                    duplicated = duplicated + 1
                    print(error.text)
                else:
                    uploaded = uploaded + 1
                    print(i, 'was uploaded')
            except:
                failed = failed + 1
                print(i, 'was not uploaded')
        except:
            failed = failed + 1
            print(i, 'was not uploaded')
        print('---------')
        bar.next()
    bar.finish()
    verify = duplicated + uploaded + failed
    print('--Finished--')
    print('Verify:',verify, "=",len(activity))
    print('Uploaded files:',uploaded)
    print('Duplicates files:',duplicated)
    print('Failed files:',failed)


def export_files():
    browser = webdriver.Chrome()
    browser.get("https://connect.garmin.com/modern/activities")
    time.sleep(3)

    driver = browser
    iframe = browser.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)

    text_file = open("Output.txt", "w")
    text_file.close()

    if my_password_gar is not "":
        id_name = driver.find_element_by_id('username')
        id_name.send_keys(my_username)

        id_password = driver.find_element_by_name('password')
        id_password.send_keys(my_password_gar)

        id_checkbox = driver.find_element_by_id('login-btn-signin')
        id_checkbox.click()

    send_message = 0
    while browser.current_url != "https://connect.garmin.com/modern/activities":
        if send_message == 0:
            print('Please fil in credentials and log in')
            send_message = 1
        time.sleep(3)

    time.sleep(4)

    activity = browser.find_elements_by_class_name('inline-edit-target ')
    print(activity)
    browser.get(activity[4].get_attribute("href"))

    counter = 0
    exceptions = 0
    activity = []

    while counter < int(tot_files):
        try:
            menu = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-trigger page-navigation-action' and @aria-label='More...']")))
            browser.execute_script("arguments[0].scrollIntoView();", menu)
            menu.click()

            export = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@id='btn-export-tcx']")))
            browser.execute_script("arguments[0].scrollIntoView();", export)
            export.click()

            text_file = open("Output.txt", "a")
            text_file.write("/activity_" + browser.current_url.split('/')[5] + '.tcx' + ',')
            text_file.close()

            counter = counter + 1
            print(browser.current_url)
            print('Activities exported so far: ', counter)

            #next activity
            nextpage = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='page-previous page-navigation-action']")))
            browser.execute_script("arguments[0].scrollIntoView();", nextpage)
            nextpage.click()

            exceptions = 0
        except:
            time.sleep(4)
            exceptions = exceptions + 1
        if exceptions > 3:
            exported_files = counter
            counter = int(tot_files)

    print('Export done. Activities exported:',exported_files)


reply = 0
while reply < 1:
    answers = input("What do you want to do? [T] = Transfer, [E] = Export only , [I] = Import only \n")

    if answers == 'T' or answers == 't':
        my_username = input('Write your email: ')
        my_password_gar = getpass('Write your Garmin Connect password: ')
        my_password_str = getpass('Write your Strava password: ')
        tot_files = input('How many files do you want to export? ')
        export_files()
        import_files()
        reply = 1
    elif answers == 'E' or answers == 'e':
        my_username = input('Write your email: ')
        my_password_gar = getpass('Write your Garmin Connect password: ')
        tot_files = input('How many files do you want to export? ')
        export_files()
        reply = 1
    elif answers == 'I' or answers == 'i':
        my_username = input('Write your email: ')
        my_password_str = getpass('Write your Strava password: ')
        import_files()
        reply = 1
    else:
        print('Write the first letter only')



input('Press enter to close')
