import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from progress.bar import Bar

import inquirer

def import_files():
    browser = webdriver.Chrome()
    browser.get("https://www.strava.com/upload/select")

    c = 0
    while browser.current_url != "https://www.strava.com/upload/select":
        if c == 0:
            print('Please fil in credentials and log in')
            c = 1
        time.sleep(3)

    text_file = open("Output.txt", "r")
    activity = text_file.read().split(',')

    uploaded = 0
    duplicated = 0
    failed = -1
    bar = Bar('Uploading', max=len(activity)-1)

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
            print('ok')
        print('---------')
        bar.next()
    bar.finish()
    verify = duplicated + uploaded + failed
    print('--Finished--')
    print('Verify:',verify, "=",len(activity)-1)
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

    c = 0
    while browser.current_url != "https://connect.garmin.com/modern/activities":
        if c == 0:
            print('Please fil in credentials and log in')
            c = 1
        time.sleep(3)

    time.sleep(4)

    activity = browser.find_elements_by_class_name('inline-edit-target ')
    print(activity)
    browser.get(activity[4].get_attribute("href"))

    counter = 0
    b = 0
    activity = []

    while b < 25:
        browser.current_url
        #time.sleep(4)
        menu = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-trigger page-navigation-action' and @aria-label='More...']")))
        browser.execute_script("arguments[0].scrollIntoView();", menu)
        menu.click()

        export = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@id='btn-export-tcx']")))
        browser.execute_script("arguments[0].scrollIntoView();", export)
        export.click()

        text_file = open("Output.txt", "a")
        text_file.write("/activity_" + browser.current_url.split('/')[5] + '.tcx' + ',')
        text_file.close()

        print (browser.current_url)
        counter = counter + 1

        #next activity
        try:
            nextpage = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='page-previous page-navigation-action']")))
            browser.execute_script("arguments[0].scrollIntoView();", nextpage)
            nextpage.click()
            b = b + 1
        except:
            b = 1

    print('Activities exported:',counter)

v = 0
while v < 1:
    answers = input("What do you want to do? [T] = Transfer, [E] = Export only , [I] = Import only")
    print(answers)
    if answers == 'T':
        export_files()
        import_files()
        v = 1
    elif answers == 'E':
        export_files()
        v = 1
    elif answers == 'I':
        import_files()
        v = 1
    else:
        print('Write the first letter only')

input('Press enter to close')
