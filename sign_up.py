# sign_up.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import timedelta, datetime
import time

'''
List of members to sign-up
'''
active_members = {"Jeffrey Shum": "06:00", "Samphors Phal": "06:00",
                  "Phaline Taing": "06:00", "Sereyamrith Bun": "06:00",
                  "Juanita Delvasto": "06:00", "Nikhil Mani": "05:15",
                  "Venus Hoy": "05:15"}
# Add or remove names of members to enable/disable sign-up for that member
    # dependency: having the members' matching name, login info, and 'Person ID' in data.txt
    # inactives: 

'''
Creating date variables
'''
today = datetime.today()
seven_days_from_today = today + timedelta(days=7)
date_string = seven_days_from_today.strftime("%A %B %e") #'%e' is the day number with a space instead of a leading zero
class_time = "6:00 AM - 6:45 AM"
year = str(seven_days_from_today.year)
month = str(seven_days_from_today.month)
day = str(seven_days_from_today.day)
weekday = today.weekday()
day_var = weekday + 3 #this is used to compose the xpath to the sign-up link depending on what day of the week it is

'''
Creating a dict of users' login data
'''
with open("/Users/jeff/Dev/python-dev/web-sign-up-automation-cfamatak/data.txt") as file:
    lines = file.readlines()
    lst = []
    for line in lines:
        line = line.strip().split(',')
        lst.append(line)
    member_data = { item[0]: [item[1], item[2], item[3]] for item in lst}

'''
Fetching urls
'''
with open("/Users/jeff/Dev/python-dev/web-sign-up-automation-cfamatak/urls.txt") as file:
    urls = file.readlines()
    lst = []
    for url in urls:
        url = url.strip()
        lst.append(url)
    login_url = lst[0]
    calendar_url = lst[1] + f"{year}-{month}-{day}&calendarType=PERSON:"
    logout_url = lst[2]
        
'''
Setting up xpath and Chrome webdriver
'''
PATH = "/Users/jeff/chromedriver"
driver = webdriver.Chrome(PATH)
xpaths = {'05:15': f'/html/body/div/table/tbody/tr/td[2]/table[2]/tbody/tr/td[{day_var}]/div/div[1]',
          '06:00': f'/html/body/div/table/tbody/tr/td[2]/table[2]/tbody/tr/td[{day_var}]/div/div[2]',
          '07:00': f'/html/body/div/table/tbody/tr/td[2]/table[2]/tbody/tr/td[{day_var}]/div/div[3]'}
          
def login(login_url, email_address, password):   
    driver.get(login_url)
    elem = driver.find_element_by_id("idUsername")
    elem.send_keys(email_address) 
    elem = driver.find_element_by_id("idPassword")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

def sign_up(calendar_url, xpath, member_name, member_id):
    calendar_url = calendar_url + member_id
    driver.get(calendar_url)
    try:
        elem = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable((By.XPATH, xpath))
        )
        elem.click()

        try:
            elem = WebDriverWait(driver, 5).until(
                expected_conditions.element_to_be_clickable((By.ID, "reserve_1"))
            )
            time.sleep(5)
            elem.click()
            print(f"{member_name} was successfully registered for {active_members[member_name]} Bootcamp class on {date_string}.")
        except:
            print(f"Failed to register {member_name}, manually check whether he/she is signed up for the class.")
    except:
        print(f"Something went wrong while registering {member_name}, ensure they have an active membership.")
    finally:
        driver.get(logout_url)


def main():
    for member_name, class_desired in active_members.items():
        email_address = member_data[member_name][0]
        password = member_data[member_name][1]
        member_id = member_data[member_name][2]
        xpath = xpaths[class_desired]
        login(login_url, email_address, password,)
        sign_up(calendar_url, xpath, member_name, member_id)

if __name__ == "__main__":
    main()
