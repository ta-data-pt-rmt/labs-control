"""OLD- NOT USE. Scrapes IH Student Portal and returns"""
# pylint: disable=consider-using-enumerate
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import logging
import pathlib
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from settings import  TEACHING_EMAIL
from bs4 import BeautifulSoup

def get_students_table(
    teacher_password : str,
    teacher_email : str = TEACHING_EMAIL
    )-> pd.DataFrame():
    """Creates driver connection to ironhack campus tools
    and inserts ta account credentials to log in.
    
    Args:
        -teacher_password (str) : password which will be parsed 
            when running main script.
        -teacher_email (str) : TA's teaching email

    Returns:
        -labs_overall (pd.DataFrame) : table containing all info
            of students submissions for all labs.
    """

    # creates driver instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    time.sleep(9.5)
    # open the website
    driver.get('https://campus-tools.ironhack.com/#/cohorts/618138e279542a002c897068/show/course_progress/assignments')
    time.sleep(4)
    # e-mail box
    email_box = driver.find_element(By.ID, "identifierId")
    email_box.clear()
    email_box.send_keys(teacher_email)
    time.sleep(3)

    # advance button
    advance_1 = driver.find_element(By.ID, "identifierNext")
    advance_1.click()
    time.sleep(3.5)

    # password box
    pass_box = driver.find_element(By.NAME, "password")
    time.sleep(0.5)
    pass_box.clear()
    time.sleep(1.5)
    pass_box.send_keys(teacher_password)
    time.sleep(4)

    # advance button
    advance_2 = driver.find_element(By.ID, "passwordNext")
    time.sleep(1.5)
    advance_2.click()
    time.sleep(4.5)

    # get student portal link again because sometimes the previous page gets stuck
    driver.get('https://campus-tools.ironhack.com/#/cohorts/618138e279542a002c897068/show/course_progress/assignments')
    time.sleep(3.5)
    logger.info("Sucessfully accessed campus tools website!")

    # find all rows of weeks separators and store in variable
    weeks_table = driver.find_elements(By.CSS_SELECTOR,"tr[class^='MuiTableRow-root']")

    # DataFrame where we'll store our students labs info
    labs_overall = pd.DataFrame( columns= ["week", "lab_name", "student_name", "lab_status", "delivery_date"])

    # iterate through all weeks, start at 1 because, index 0 corresponds to the header
    for week_number in range(len(weeks_table)):
        if week_number < 1:
            pass
        else: 
            try:

                # drop-down weeks separator to see the labs
                drop_down_weeks = weeks_table[week_number].find_element(
                    By.CSS_SELECTOR,
                    "div[class^='MuiButtonBase-root']")
                drop_down_weeks.click()
                time.sleep(3)

                # get week number string
                week = weeks_table[week_number].find_element(
                    By.CSS_SELECTOR, 
                    "td[class^='MuiTableCell-root MuiTableCell-body column-display_name']"
                    ).text

                # get the html content inside the week in search
                labs_table =   driver.find_elements(
                    By.CSS_SELECTOR,
                    "td[class^='MuiTableCell-root MuiTableCell-body MuiTableCell-sizeSmall']")

                # get lab name and directions of dropdown of labs
                lab_names = labs_table[0].find_elements(By.CLASS_NAME, "MuiBadge-root")
                print(lab_names)
                drop_down_labs = labs_table[0].find_elements(
                    By.CSS_SELECTOR,
                    "div[class^='MuiButtonBase-root']")

                # go for each lab inside the respective week
                for index in range(len(lab_names)):
                    each_lab_name = lab_names[index].text
                    logger.info(f"Start collecting info for {each_lab_name}, {week}")

                    # check lab info table (ex drop down on Lab Strings)
                    # drop-down inside the lab to see students statuses
                    drop_down_labs[index].click()
                    time.sleep(4)

                    # get number of students
                    n_students = len(labs_table[0].find_elements(
                        By.CSS_SELECTOR, 
                        "td[class^='MuiTableCell-root MuiTableCell-body column-first_name']")
                        )

                    logger.info("Found %s students", n_students)

                    for i in range(n_students):

                        # find name, status and delivery date of each student
                        # empty list
                        student_lab = []

                        student_name = (
                            labs_table[0].find_elements(
                                By.CSS_SELECTOR,
                                "td[class^='MuiTableCell-root MuiTableCell-body column-first_name']")[i]
                            .text
                        )

                        lab_status = (
                            labs_table[0]
                            .find_elements(
                                By.CSS_SELECTOR,
                                "td[class^='MuiTableCell-root MuiTableCell-body column-status']")[i]
                            .text
                        )

                        delivery_date = (
                            labs_table[0]
                            .find_elements(
                                By.CSS_SELECTOR,
                                "td[class^='MuiTableCell-root MuiTableCell-body column-submit_date']")[i]
                            .text
                        )

                    # append elements into a full row of student info
                        student_lab.extend([week, each_lab_name, student_name, lab_status, delivery_date])

                        labs_overall = ( labs_overall.append(pd.Series(
                            student_lab,
                            index = labs_overall.columns),
                            ignore_index=True)
                            )
                    logger.info(f"finished collecting students info for lab {each_lab_name} of {week}")

                    time.sleep(3)
                    drop_down_labs[index].click()
                    time.sleep(3)
                
                drop_down_weeks.click()
                time.sleep(2)
            
            except:
                logger.info(
                    f"""Got an error.
                    Last variables found were : {student_lab}""")

    return labs_overall


def clean_labs_table(labs_overall : pd.DataFrame)-> pd.DataFrame:
    """Cleans the table got from scraping campus tools."""

    # create a column with week number as numeric type
    labs_overall["week_num"] = labs_overall["week"].apply(lambda x: int(x.split()[1]))

    # clean the lab_name column to remove "\nRequired"
    labs_overall["lab_name"] = labs_overall["lab_name"].apply(lambda x: x.split("\n")[0])

    return labs_overall

####